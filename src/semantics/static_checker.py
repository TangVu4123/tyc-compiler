"""
Static Semantic Checker for TyC Programming Language
=====================================================

Kiến trúc: Single-pass với pre-scan symbol collection THEO ĐÚNG THỨ TỰ KHAI BÁO.

Cụ thể:
  - Struct được đăng ký và kiểm tra member THEO THỨ TỰ xuất hiện trong source.
    => Struct dùng trước khi khai báo → UndeclaredStruct (test_047).
    => Struct member dùng struct khai báo sau → UndeclaredStruct (test_048, test_052).

  - Function được đăng ký THEO THỨ TỰ.
    => Gọi hàm trước khai báo → UndeclaredFunction (test_037).

  Đây là SINGLE-PASS: duyệt node.decls một lần duy nhất, mỗi decl được
  đăng ký ngay rồi kiểm tra đầy đủ trước khi sang decl tiếp theo.

Quy tắc quan trọng từ spec:
  - TypeMismatchInStatement: gán sai kiểu ở STATEMENT LEVEL (ExprStmt với AssignExpr).
  - TypeMismatchInExpression: sai kiểu trong EXPRESSION (bao gồm assignment expr
    dùng trong context expression như `int y = (x = "bad") + 1`).
  - Phân biệt bằng cờ `in_stmt_assign`: True khi AssignExpr là TOP-LEVEL của ExprStmt.
"""

from typing import Dict, List, Set, Optional, Any, Tuple

from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode, Program, StructDecl, MemberDecl, FuncDecl, Param, VarDecl,
    IfStmt, WhileStmt, ForStmt, BreakStmt, ContinueStmt, ReturnStmt,
    BlockStmt, SwitchStmt, CaseStmt, DefaultStmt, Type, IntType,
    FloatType, StringType, VoidType, StructType, BinaryOp, PrefixOp,
    PostfixOp, AssignExpr, MemberAccess, FuncCall, Identifier,
    StructLiteral, IntLiteral, FloatLiteral, StringLiteral, ExprStmt,
    Expr, Stmt, Decl,
)
from .static_error import (
    StaticError, Redeclared, UndeclaredIdentifier, UndeclaredFunction,
    UndeclaredStruct, TypeCannotBeInferred, TypeMismatchInStatement,
    TypeMismatchInExpression, MustInLoop,
)


# =============================================================================
# Helpers
# =============================================================================

def _types_equal(a: Type, b: Type) -> bool:
    """Structural equality cho TyC types."""
    if type(a) is not type(b):
        return False
    if isinstance(a, StructType):
        return a.struct_name == b.struct_name
    return True


def _is_numeric(t: Optional[Type]) -> bool:
    return isinstance(t, (IntType, FloatType))


def _is_lvalue(expr: Expr) -> bool:
    """Chỉ Identifier và MemberAccess là lvalue hợp lệ."""
    return isinstance(expr, (Identifier, MemberAccess))


def _unpack(o: Any) -> Tuple[Dict, Optional[Type], bool]:
    """
    Unpack `o` thành (env, expected, in_stmt_assign).
    - Expression visitors nhận o = (env, expected, in_stmt_assign).
    - Statement visitors nhận o = env dict trực tiếp.
    """
    if isinstance(o, tuple) and len(o) == 3:
        return o[0], o[1], o[2]
    if isinstance(o, tuple) and len(o) == 2:
        return o[0], o[1], False
    return o, None, False


# =============================================================================
# StaticChecker
# =============================================================================

class StaticChecker(ASTVisitor):
    """
    Static semantic checker cho TyC.
    Raise StaticError subclass ngay khi gặp lỗi đầu tiên.
    """

    def check_program(self, ast: ASTNode) -> None:
        """Entry point được gọi từ tests/utils.py."""
        self.visit(ast)

    # =========================================================================
    # Program
    # =========================================================================

    def visit_program(self, node: Program, o: Any = None) -> None:
        """
        SINGLE-PASS: duyệt decls theo thứ tự.
        Mỗi StructDecl: đăng ký vào structs, kiểm tra members ngay.
        Mỗi FuncDecl: đăng ký vào functions, kiểm tra body ngay.
        => Forward reference KHÔNG hợp lệ (phải khai báo trước khi dùng).
        """
        env: Dict = {
            "structs": {},
            "functions": {
                # Built-in functions
                "readInt":     FuncDecl(IntType(),    "readInt",     [], BlockStmt([])),
                "readFloat":   FuncDecl(FloatType(),  "readFloat",   [], BlockStmt([])),
                "readString":  FuncDecl(StringType(), "readString",  [], BlockStmt([])),
                "printInt":    FuncDecl(VoidType(),   "printInt",    [Param(IntType(),    "value")], BlockStmt([])),
                "printFloat":  FuncDecl(VoidType(),   "printFloat",  [Param(FloatType(), "value")], BlockStmt([])),
                "printString": FuncDecl(VoidType(),   "printString", [Param(StringType(), "value")], BlockStmt([])),
            },
            "scopes":          [],
            "param_names":     set(),
            "current_func":    None,
            "inferred_return": None,
            "in_loop":         False,
            "in_switch":       False,
        }

        for decl in node.decls:
            if isinstance(decl, StructDecl):
                # Đăng ký struct (kiểm tra Redeclared)
                if decl.name in env["structs"]:
                    raise Redeclared("Struct", decl.name)
                # Kiểm tra members (Redeclared Member, UndeclaredStruct)
                self._check_struct_members(decl, env)
                # Đăng ký SAU khi members đã được kiểm tra
                env["structs"][decl.name] = decl

            elif isinstance(decl, FuncDecl):
                # Đăng ký function (kiểm tra Redeclared)
                if decl.name in env["functions"]:
                    raise Redeclared("Function", decl.name)
                env["functions"][decl.name] = decl
                # Kiểm tra body ngay
                self.visit(decl, env)

    # =========================================================================
    # Struct
    # =========================================================================

    def _check_struct_members(self, node: StructDecl, env: Dict) -> None:
        """
        Kiểm tra struct members:
          - Tên member duy nhất → Redeclared("Member").
          - Kiểu member phải đã khai báo → UndeclaredStruct.
          - Không tự tham chiếu → UndeclaredStruct.
        """
        seen: Set[str] = set()
        for member in node.members:
            if member.name in seen:
                raise Redeclared("Member", member.name)
            seen.add(member.name)
            self._assert_type_declared(member.member_type, env, forbid_struct=node.name)

    def visit_struct_decl(self, node: StructDecl, o: Any) -> None:
        pass  # xử lý trong visit_program

    def visit_member_decl(self, node: MemberDecl, o: Any) -> None:
        pass

    # =========================================================================
    # Function
    # =========================================================================

    def visit_func_decl(self, node: FuncDecl, o: Any) -> None:
        """
        Kiểm tra function declaration:
          1. Kiểm tra kiểu return (nếu tường minh, phải là valid type).
          2. Kiểm tra kiểu param.
          3. Param names duy nhất.
          4. Duyệt body.
          5. Infer return type nếu cần.
        """
        # Kiểm tra return type nếu tường minh
        if node.return_type is not None:
            self._assert_type_declared(node.return_type, o)

        # Tạo môi trường hàm
        func_env: Dict = {
            **o,
            "scopes":          [],
            "param_names":     set(),
            "current_func":    node,
            "inferred_return": node.return_type,  # None = đang infer
            "in_loop":         False,
            "in_switch":       False,
        }

        # Xây param scope
        param_scope: Dict[str, Optional[Type]] = {}
        for param in node.params:
            # Kiểm tra kiểu param
            self._assert_type_declared(param.param_type, o)
            if param.name in param_scope:
                raise Redeclared("Parameter", param.name)
            param_scope[param.name] = param.param_type

        func_env["param_names"] = set(param_scope.keys())
        func_env["scopes"].append(param_scope)  # scope[0] = param scope

        # Duyệt body statements trực tiếp (không mở scope mới vì param scope đã là scope[0])
        self._visit_stmts(node.body.statements, func_env)

        # Xác định return type cuối cùng
        if func_env["inferred_return"] is None:
            func_env["inferred_return"] = VoidType()
        if node.return_type is None:
            node.return_type = func_env["inferred_return"]

    def visit_param(self, node: Param, o: Any) -> None:
        pass

    # =========================================================================
    # Type assertion
    # =========================================================================

    def _assert_type_declared(
        self,
        t: Type,
        env: Dict,
        forbid_struct: Optional[str] = None,
    ) -> None:
        """
        Kiểm tra t là kiểu hợp lệ:
          - StructType: phải có trong env["structs"], không được là forbid_struct.
          - Primitives: luôn hợp lệ.
        """
        if isinstance(t, StructType):
            if forbid_struct is not None and t.struct_name == forbid_struct:
                raise UndeclaredStruct(t.struct_name)
            if t.struct_name not in env["structs"]:
                raise UndeclaredStruct(t.struct_name)

    # =========================================================================
    # Scope management
    # =========================================================================

    def _push_scope(self, env: Dict) -> None:
        env["scopes"].append({})

    def _pop_scope(self, env: Dict) -> None:
        env["scopes"].pop()

    def _lookup(self, name: str, env: Dict) -> Tuple[bool, Optional[Type]]:
        """Tìm name từ scope trong cùng ra ngoài."""
        for scope in reversed(env["scopes"]):
            if name in scope:
                return True, scope[name]
        return False, None

    def _declare(self, name: str, var_type: Optional[Type], env: Dict) -> None:
        """
        Khai báo biến vào scope hiện tại.
        Raise Redeclared nếu tên đã có trong scope hiện tại,
        hoặc trùng với param của hàm đang xét (kể cả block lồng).
        """
        current = env["scopes"][-1]
        if name in current:
            raise Redeclared("Variable", name)
        # Kiểm tra shadow param: chỉ khi đang trong block con (len > 1)
        if name in env["param_names"] and len(env["scopes"]) > 1:
            raise Redeclared("Variable", name)
        current[name] = var_type

    def _fix_auto(self, name: str, inferred: Type, env: Dict) -> None:
        """Cập nhật auto placeholder (None) thành inferred."""
        for scope in reversed(env["scopes"]):
            if name in scope and scope[name] is None:
                scope[name] = inferred
                return

    def _check_scope_unresolved(self, scope: Dict, ctx: ASTNode) -> None:
        """Nếu scope còn auto chưa giải → TypeCannotBeInferred(ctx)."""
        if any(t is None for t in scope.values()):
            raise TypeCannotBeInferred(ctx)

    # =========================================================================
    # Type node visitors
    # =========================================================================

    def visit_int_type(self, node: IntType, o: Any = None) -> IntType:
        return node
    def visit_float_type(self, node: FloatType, o: Any = None) -> FloatType:
        return node
    def visit_string_type(self, node: StringType, o: Any = None) -> StringType:
        return node
    def visit_void_type(self, node: VoidType, o: Any = None) -> VoidType:
        return node
    def visit_struct_type(self, node: StructType, o: Any = None) -> StructType:
        return node

    # =========================================================================
    # Statement helpers
    # =========================================================================

    def _visit_stmts(self, stmts: List, env: Dict) -> None:
        """
        Duyệt list statement trong scope đang mở sẵn.
        Sau khi duyệt hết, kiểm tra auto placeholder còn None trong scope[-1].
        """
        for stmt in stmts:
            self.visit(stmt, env)
        if env["scopes"]:
            self._check_scope_unresolved(env["scopes"][-1], BlockStmt(stmts))

    def _visit_as_stmt(self, stmt: Stmt, env: Dict) -> None:
        """
        Visit một statement con (then/else/body of if/while/for).
        BlockStmt → tự quản lý scope.
        Các stmt khác → bọc trong scope tạm.
        """
        if isinstance(stmt, BlockStmt):
            self.visit(stmt, env)
        else:
            self._push_scope(env)
            self.visit(stmt, env)
            self._check_scope_unresolved(env["scopes"][-1], stmt)
            self._pop_scope(env)

    # =========================================================================
    # Statement visitors
    # =========================================================================

    def visit_block_stmt(self, node: BlockStmt, o: Any) -> None:
        self._push_scope(o)
        for stmt in node.statements:
            self.visit(stmt, o)
        self._check_scope_unresolved(o["scopes"][-1], node)
        self._pop_scope(o)

    def visit_var_decl(self, node: VarDecl, o: Any) -> None:
        """
        Khai báo biến.
        Init expression eval TRƯỚC khi tên biến vào scope
        (tên biến không nhìn thấy trong chính initializer của nó).
        """
        if node.var_type is None:
            # auto
            if node.init_value is not None:
                init_t = self._eval(node.init_value, o)
                if init_t is None:
                    raise TypeCannotBeInferred(node.init_value)
                self._declare(node.name, init_t, o)
            else:
                self._declare(node.name, None, o)
        else:
            # explicit type: kiểm tra type hợp lệ trước
            self._assert_type_declared(node.var_type, o)
            if node.init_value is not None:
                init_t = self._eval(node.init_value, o, expected=node.var_type)
                if init_t is None:
                    raise TypeCannotBeInferred(node.init_value)
                if not _types_equal(init_t, node.var_type):
                    raise TypeMismatchInStatement(node)
            self._declare(node.name, node.var_type, o)

    def visit_if_stmt(self, node: IfStmt, o: Any) -> None:
        cond_t = self._eval(node.condition, o)
        if not isinstance(cond_t, IntType):
            raise TypeMismatchInStatement(node)
        self._visit_as_stmt(node.then_stmt, o)
        if node.else_stmt is not None:
            self._visit_as_stmt(node.else_stmt, o)

    def visit_while_stmt(self, node: WhileStmt, o: Any) -> None:
        cond_t = self._eval(node.condition, o)
        if not isinstance(cond_t, IntType):
            raise TypeMismatchInStatement(node)
        loop_env = {**o, "in_loop": True}
        self._visit_as_stmt(node.body, loop_env)

    def visit_for_stmt(self, node: ForStmt, o: Any) -> None:
        # Init sống trong scope bao quanh (không mở scope mới cho for header)
        if node.init is not None:
            self.visit(node.init, o)
        if node.condition is not None:
            cond_t = self._eval(node.condition, o)
            if not isinstance(cond_t, IntType):
                raise TypeMismatchInStatement(node)
        if node.update is not None:
            self._eval(node.update, o)
        loop_env = {**o, "in_loop": True}
        self._visit_as_stmt(node.body, loop_env)

    def visit_switch_stmt(self, node: SwitchStmt, o: Any) -> None:
        expr_t = self._eval(node.expr, o)
        if not isinstance(expr_t, IntType):
            raise TypeMismatchInStatement(node)
        sw_env = {**o, "in_switch": True}
        for case in node.cases:
            self.visit(case, sw_env)
        if node.default_case is not None:
            self.visit(node.default_case, sw_env)

    def visit_case_stmt(self, node: CaseStmt, o: Any) -> None:
        case_t = self._eval(node.expr, o)
        if not isinstance(case_t, IntType):
            raise TypeMismatchInStatement(node)
        self._push_scope(o)
        self._visit_stmts(node.statements, o)
        self._pop_scope(o)

    def visit_default_stmt(self, node: DefaultStmt, o: Any) -> None:
        self._push_scope(o)
        self._visit_stmts(node.statements, o)
        self._pop_scope(o)

    def visit_break_stmt(self, node: BreakStmt, o: Any) -> None:
        """Break hợp lệ trong loop HOẶC switch."""
        if not (o["in_loop"] or o["in_switch"]):
            raise MustInLoop(node)

    def visit_continue_stmt(self, node: ContinueStmt, o: Any) -> None:
        """Continue chỉ hợp lệ trong loop (KHÔNG trong switch)."""
        if not o["in_loop"]:
            raise MustInLoop(node)

    def visit_return_stmt(self, node: ReturnStmt, o: Any) -> None:
        declared = o["inferred_return"]
        if node.expr is None:
            if declared is None:
                o["inferred_return"] = VoidType()
            elif not isinstance(declared, VoidType):
                raise TypeMismatchInStatement(node)
        else:
            expr_t = self._eval(node.expr, o)
            if expr_t is None:
                raise TypeCannotBeInferred(node)
            if declared is None:
                o["inferred_return"] = expr_t
            elif isinstance(declared, VoidType):
                raise TypeMismatchInStatement(node)
            elif not _types_equal(expr_t, declared):
                raise TypeMismatchInStatement(node)

    def visit_expr_stmt(self, node: ExprStmt, o: Any) -> None:
        """
        Expression statement.
        Nếu expr là AssignExpr → truyền in_stmt_assign=True để
        visit_assign_expr biết raise TypeMismatchInStatement (không phải Expression).
        """
        if isinstance(node.expr, AssignExpr):
            self._eval(node.expr, o, expected=None, in_stmt_assign=True)
        else:
            self._eval(node.expr, o)

    # =========================================================================
    # Expression evaluation entry point
    # =========================================================================

    def _eval(
        self,
        expr: Expr,
        env: Dict,
        expected: Optional[Type] = None,
        in_stmt_assign: bool = False,
    ) -> Optional[Type]:
        """
        Đánh giá kiểu của expr.
        expected: gợi ý kiểu context (struct literal, assignment rhs).
        in_stmt_assign: True khi AssignExpr là top-level của ExprStmt.
        """
        return self.visit(expr, (env, expected, in_stmt_assign))

    # =========================================================================
    # Literal visitors
    # =========================================================================

    def visit_int_literal(self, node: IntLiteral, o: Any = None) -> IntType:
        return IntType()

    def visit_float_literal(self, node: FloatLiteral, o: Any = None) -> FloatType:
        return FloatType()

    def visit_string_literal(self, node: StringLiteral, o: Any = None) -> StringType:
        return StringType()

    # =========================================================================
    # Expression visitors
    # =========================================================================

    def visit_identifier(self, node: Identifier, o: Any) -> Optional[Type]:
        env, _, _ = _unpack(o)
        found, var_type = self._lookup(node.name, env)
        if not found:
            raise UndeclaredIdentifier(node.name)
        return var_type  # None = auto placeholder chưa giải

    def visit_member_access(self, node: MemberAccess, o: Any) -> Type:
        env, _, _ = _unpack(o)
        obj_t = self._eval(node.obj, env)
        if obj_t is None:
            raise TypeCannotBeInferred(node)
        if not isinstance(obj_t, StructType):
            raise TypeMismatchInExpression(node)
        struct_decl = env["structs"].get(obj_t.struct_name)
        if struct_decl is None:
            raise UndeclaredStruct(obj_t.struct_name)
        for m in struct_decl.members:
            if m.name == node.member:
                return m.member_type
        raise TypeMismatchInExpression(node)

    def visit_func_call(self, node: FuncCall, o: Any) -> Type:
        env, _, _ = _unpack(o)
        func_decl = env["functions"].get(node.name)
        if func_decl is None:
            raise UndeclaredFunction(node.name)
        if len(node.args) != len(func_decl.params):
            raise TypeMismatchInExpression(node)
        for arg_expr, param in zip(node.args, func_decl.params):
            arg_t = self._eval(arg_expr, env, expected=param.param_type)
            # Lone Identifier auto → infer từ param type
            if arg_t is None and isinstance(arg_expr, Identifier):
                self._fix_auto(arg_expr.name, param.param_type, env)
                arg_t = param.param_type
            if arg_t is None:
                raise TypeCannotBeInferred(arg_expr)
            if not _types_equal(arg_t, param.param_type):
                raise TypeMismatchInExpression(node)
        return func_decl.return_type

    def visit_struct_literal(self, node: StructLiteral, o: Any) -> Optional[Type]:
        env, expected, _ = _unpack(o)
        
        # Nếu không có thông tin về kiểu mong đợi (ví dụ: auto chưa giải), trả về None để xử lý sau
        if expected is None:
            return None
            
        # Nếu đã có kiểu mong đợi nhưng KHÔNG PHẢI là StructType -> Lỗi Type Mismatch
        if not isinstance(expected, StructType):
            raise TypeMismatchInExpression(node)
            
        struct_decl = env["structs"].get(expected.struct_name)
        if struct_decl is None:
            raise UndeclaredStruct(expected.struct_name)
            
        # Kiểm tra số lượng thành viên (arity)
        if len(node.values) != len(struct_decl.members):
            raise TypeMismatchInExpression(node)
            
        # Kiểm tra kiểu của từng thành viên trong struct literal
        for val_expr, member in zip(node.values, struct_decl.members):
            val_t = self._eval(val_expr, env, expected=member.member_type)
            
            if val_t is None:
                raise TypeCannotBeInferred(val_expr)
                
            if not _types_equal(val_t, member.member_type):
                raise TypeMismatchInExpression(node)
                
        return expected

    def visit_binary_op(self, node: BinaryOp, o: Any) -> Type:
        env, _, _ = _unpack(o)
        op = node.operator

        left_t  = self._eval(node.left,  env)
        right_t = self._eval(node.right, env)

        # Giải auto placeholder nếu một bên đã biết
        left_t, right_t = self._resolve_binary_autos(
            node, op, node.left, left_t, node.right, right_t, env
        )

        if op in ('+', '-', '*', '/'):
            if not (_is_numeric(left_t) and _is_numeric(right_t)):
                raise TypeMismatchInExpression(node)
            if isinstance(left_t, FloatType) or isinstance(right_t, FloatType):
                return FloatType()
            return IntType()
        elif op == '%':
            if not (isinstance(left_t, IntType) and isinstance(right_t, IntType)):
                raise TypeMismatchInExpression(node)
            return IntType()
        elif op in ('==', '!=', '<', '<=', '>', '>='):
            if not (_is_numeric(left_t) and _is_numeric(right_t)):
                raise TypeMismatchInExpression(node)
            return IntType()
        elif op in ('&&', '||'):
            if not (isinstance(left_t, IntType) and isinstance(right_t, IntType)):
                raise TypeMismatchInExpression(node)
            return IntType()
        raise TypeMismatchInExpression(node)

    def _resolve_binary_autos(
        self,
        node:       BinaryOp,
        op:         str,
        left_expr:  Expr, left_t:  Optional[Type],
        right_expr: Expr, right_t: Optional[Type],
        env:        Dict,
    ) -> Tuple[Type, Type]:
        """
        Giải auto placeholder trong binary expression (spec §2.2.1).

        Quy tắc:
          - Cả hai None → TypeCannotBeInferred.
          - Một bên None:
              * Bên unknown PHẢI là lone Identifier (auto).
                Nếu là compound expr → TypeCannotBeInferred.
              * known_t không hợp lệ với operator:
                - Nếu known_t là string/struct cho arithmetic → TypeCannotBeInferred
                  (không thể infer vì string không có trong operator table của +,-,*,/).
                  => Ghi chú: spec nói TypeCannotBeInferred khi "không thể fix auto",
                  không phải TypeMismatchInExpression cho trường hợp này.
              * Tính inferred type.
        """
        if left_t is not None and right_t is not None:
            return left_t, right_t

        if left_t is None and right_t is None:
            raise TypeCannotBeInferred(node)

        infer_left   = (left_t is None)
        unknown_expr = left_expr  if infer_left else right_expr
        known_t      = right_t   if infer_left else left_t

        # Bên unknown phải là lone Identifier để có thể fix
        if not isinstance(unknown_expr, Identifier):
            raise TypeCannotBeInferred(node)

        # Tính inferred type theo operator + known_t
        if op in ('+', '-', '*', '/'):
            if not _is_numeric(known_t):
                # known là string/struct → không thể infer
                raise TypeCannotBeInferred(node)
            # Integer anchor: int→int, float→float
            inferred: Type = IntType() if isinstance(known_t, IntType) else FloatType()
        elif op == '%':
            if not isinstance(known_t, IntType):
                raise TypeCannotBeInferred(node)
            inferred = IntType()
        elif op in ('==', '!=', '<', '<=', '>', '>='):
            if not _is_numeric(known_t):
                raise TypeCannotBeInferred(node)
            inferred = known_t
        elif op in ('&&', '||'):
            if not isinstance(known_t, IntType):
                raise TypeCannotBeInferred(node)
            inferred = IntType()
        else:
            raise TypeCannotBeInferred(node)

        self._fix_auto(unknown_expr.name, inferred, env)

        if infer_left:
            return inferred, known_t
        return known_t, inferred

    def visit_prefix_op(self, node: PrefixOp, o: Any) -> Type:
        env, _, _ = _unpack(o)
        op = node.operator
        operand_t = self._eval(node.operand, env)

        if operand_t is None:
            raise TypeCannotBeInferred(node)

        if op in ('++', '--'):
            if not isinstance(operand_t, IntType):
                raise TypeMismatchInExpression(node)
            if not _is_lvalue(node.operand):
                raise TypeMismatchInExpression(node)
            return IntType()
        elif op in ('+', '-'):
            if not _is_numeric(operand_t):
                raise TypeMismatchInExpression(node)
            return operand_t
        elif op == '!':
            if not isinstance(operand_t, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()
        raise TypeMismatchInExpression(node)

    def visit_postfix_op(self, node: PostfixOp, o: Any) -> Type:
        env, _, _ = _unpack(o)
        operand_t = self._eval(node.operand, env)
        if operand_t is None:
            raise TypeCannotBeInferred(node)
        if not isinstance(operand_t, IntType):
            raise TypeMismatchInExpression(node)
        if not _is_lvalue(node.operand):
            raise TypeMismatchInExpression(node)
        return IntType()

    def visit_assign_expr(self, node: AssignExpr, o: Any) -> Type:
        """
        Assignment expression: lhs = rhs.

        Phân biệt lỗi theo context:
          - in_stmt_assign=True (top-level của ExprStmt):
            Sai kiểu → TypeMismatchInStatement (đây là "statement assignment").
          - in_stmt_assign=False (dùng trong expression):
            Sai kiểu → TypeMismatchInExpression.

        lhs phải là lvalue → luôn TypeMismatchInExpression (không phụ thuộc context).
        """
        env, _, in_stmt_assign = _unpack(o)

        if not _is_lvalue(node.lhs):
            raise TypeMismatchInExpression(node)

        lhs_t = self._eval(node.lhs, env)
        rhs_t = self._eval(node.rhs, env, expected=lhs_t)

        # lhs là auto placeholder → fix từ rhs
        if lhs_t is None:
            if rhs_t is None:
                raise TypeCannotBeInferred(node)
            if isinstance(node.lhs, Identifier):
                self._fix_auto(node.lhs.name, rhs_t, env)
            return rhs_t

        if rhs_t is None:
            raise TypeCannotBeInferred(node)

        if not _types_equal(lhs_t, rhs_t):
            # Statement context → TypeMismatchInStatement
            # Expression context → TypeMismatchInExpression
            if in_stmt_assign:
                raise TypeMismatchInStatement(node)
            else:
                raise TypeMismatchInExpression(node)

        return lhs_t