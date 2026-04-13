"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *


class ASTGeneration(TyCVisitor):
    """AST Generation visitor for TyC language."""

    # =========================================================================
    # Program
    # =========================================================================

    def visitProgram(self, ctx: TyCParser.ProgramContext):
        """
        program: (structDecl | funcDecl)* EOF
        Returns: Program
        """
        decls = []
        for child in ctx.children or []:
            if isinstance(child, TyCParser.StructDeclContext) or isinstance(child, TyCParser.FuncDeclContext):
                decls.append(self.visit(child))
        return Program(decls)
    # =========================================================================
    # Declarations
    # =========================================================================

    def visitStructDecl(self, ctx):
        """
        structDecl: STRUCT ID LB structMember* RB SEMI
        Returns: StructDecl
        """
        return StructDecl(ctx.ID().getText(), [self.visit(m) for m in ctx.structMember()])

    def visitStructMember(self, ctx):
        """
        structMember: type ID SEMI
        Returns: MemberDecl
        """
        return MemberDecl(self.visit(ctx.type_()), ctx.ID().getText())

    def visitFuncDecl(self, ctx: TyCParser.FuncDeclContext):
        """
        funcDecl: (type | VOID)? ID LPAREN paramList? RPAREN block
        Returns: FuncDecl
        
        return_type is None when omitted (auto-inferred), VoidType when VOID,
        or a Type node when explicitly typed.
        """
        if ctx.VOID():
            return_type = VoidType()
        elif ctx.type_():
            return_type = self.visit(ctx.type_())
        else:
            return_type = None  # auto / omitted

        name = ctx.ID().getText()
        params = self.visit(ctx.paramList()) if ctx.paramList() else []
        body = self.visit(ctx.block())
        return FuncDecl(return_type, name, params, body)

    def visitParamList(self, ctx: TyCParser.ParamListContext):
        """
        paramList: param (COMMA param)*
        Returns: List[Param]
        """
        return [self.visit(p) for p in ctx.param()]

    def visitParam(self, ctx):
        """
        param: type ID
        Returns: Param
        """
        return Param(self.visit(ctx.type_()), ctx.ID().getText())

    # =========================================================================
    # Types
    # =========================================================================

    def visitType(self, ctx):
        """
        type: INT | FLOAT | STRING | ID
        Returns: IntType | FloatType | StringType | StructType
        """
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.STRING():
            return StringType()
        else:
            return StructType(ctx.ID().getText())


    # =========================================================================
    # Statements
    # =========================================================================

    def visitStatement(self, ctx: TyCParser.StatementContext):
        """
        statement: varDecl | block | ifStmt | whileStmt | forStmt
                 | switchStmt | breakStmt | continueStmt | returnStmt | exprStmt
        Delegates to the appropriate child visitor.
        """
        # ANTLR generates the child rule context directly; just visit the single child
        return self.visit(ctx.getChild(0))

    def visitBlock(self, ctx: TyCParser.BlockContext):
        """
        block: LBRACE (varDecl | statement)* RBRACE
        Returns: BlockStmt
        
        Must preserve order of varDecl and statement interleaved.
        We iterate ctx.children and skip terminal nodes (braces).
        """
        stmts = []
        for child in ctx.children or []:
            if isinstance(child, TyCParser.VarDeclContext) or isinstance(child, TyCParser.StatementContext):
                stmts.append(self.visit(child))
            # skip LBRACE, RBRACE terminal nodes
        return BlockStmt(stmts)

    def visitVarDecl(self, ctx: TyCParser.VarDeclContext):
        """
        varDecl: (AUTO | type) ID (ASSIGN expr)? SEMI
        Returns: VarDecl
        
        var_type = None means 'auto' (type inference).
        """
        if ctx.AUTO():
            var_type = None
        else:
            var_type = self.visit(ctx.type_())

        name = ctx.ID().getText()
        assign_value = self.visit(ctx.expr()) if ctx.expr() else None
        return VarDecl(var_type, name, assign_value)

    def visitIfStmt(self, ctx: TyCParser.IfStmtContext):
        """
        ifStmt: IF LPAREN expr RPAREN statement (ELSE statement)?
        Returns: IfStmt
        """
        condition = self.visit(ctx.expr())
        statements = ctx.statement()
        else_stmt = self.visit(statements[1]) if len(statements) > 1 else None
        return IfStmt(condition, self.visit(statements[0]), else_stmt)

    def visitWhileStmt(self, ctx: TyCParser.WhileStmtContext):
        """
        whileStmt: WHILE LPAREN expr RPAREN statement
        Returns: WhileStmt
        """
        condition = self.visit(ctx.expr())
        body = self.visit(ctx.statement())
        return WhileStmt(condition, body)

    def visitForStmt(self, ctx):
        """
        forStmt: FOR LP (varDeclStmt | exprStmt | SEMI) expr? SEMI expr? RP stmt
 
        ctx.SEMI() chỉ đếm SEMI trực tiếp thuộc forStmt (không tính SEMI
        bên trong varDeclStmt/exprStmt vì chúng là sub-rule riêng):
          - init = varDeclStmt/exprStmt → ctx.SEMI() có 1 SEMI
          - init = bare SEMI            → ctx.SEMI() có 2 SEMI
 
        Trong cả hai trường hợp, SEMI phân cách condition/update
        luôn là ctx.SEMI()[-1].
 
        condition có mặt khi số expr > (1 nếu update có mặt),
        tức là: condition rỗng ⟺ có 2 SEMI liên tiếp trong children.
        Cách đơn giản nhất: condition rỗng ⟺ len(ctx.SEMI()) == len(ctx.expr()) + 2
        Không — cách trực tiếp nhất: dùng tokenIndex của SEMI[-1] làm mốc,
        expr nào có tokenIndex nhỏ hơn → condition, lớn hơn → update.
        """
        # --- init ---
        if ctx.varDecl():
            init = self.visit(ctx.varDecl())
        elif ctx.exprStmt():
            init = self.visit(ctx.exprStmt())
        else:
            init = None
 
        # SEMI phân cách condition/update luôn là SEMI cuối trong ctx
        sep_token_index = ctx.SEMI()[-1].symbol.tokenIndex
 
        # Phân loại expr dựa vào vị trí so với SEMI phân cách
        condition = None
        update = None
        for expr_ctx in ctx.expr():
            if expr_ctx.start.tokenIndex < sep_token_index:
                condition = self.visit(expr_ctx)
            else:
                update = self.visit(expr_ctx)
 
        return ForStmt(init, condition, update, self.visit(ctx.statement()))

    def visitSwitchStmt(self, ctx: TyCParser.SwitchStmtContext):
        """
        switchStmt: SWITCH LPAREN expr RPAREN LBRACE (caseStmt | defaultStmt)* RBRACE
        Returns: SwitchStmt
        """
        expr = self.visit(ctx.expr())
        cases = [self.visit(c) for c in ctx.caseStmt()]
        default_clauses = ctx.defaultStmt()
        default_case = self.visit(default_clauses[-1]) if default_clauses else None
        return SwitchStmt(expr, cases, default_case)

    def visitCaseStmt(self, ctx: TyCParser.CaseStmtContext):
        """
        caseStmt: CASE expr COLON (varDecl | statement)*
        Returns: CaseStmt
        
        Must preserve order of varDecl and statement.
        """
        stmts = []
        for child in ctx.children or []:
            if isinstance(child, TyCParser.VarDeclContext) or isinstance(child, TyCParser.StatementContext):
                stmts.append(self.visit(child))
        return CaseStmt(self.visit(ctx.expr()), stmts)

    def visitDefaultStmt(self, ctx: TyCParser.DefaultStmtContext):
        """
        defaultStmt: DEFAULT COLON (varDecl | statement)*
        Returns: DefaultStmt
        """
        stmts = []
        for child in ctx.children or []:
            if isinstance(child, TyCParser.VarDeclContext) or isinstance(child, TyCParser.StatementContext):
                stmts.append(self.visit(child))
        return DefaultStmt(stmts)

    def visitBreakStmt(self, ctx: TyCParser.BreakStmtContext):
        """
        breakStmt: BREAK SEMI
        Returns: BreakStmt
        """
        return BreakStmt()

    def visitContinueStmt(self, ctx: TyCParser.ContinueStmtContext):
        """
        continueStmt: CONTINUE SEMI
        Returns: ContinueStmt
        """
        return ContinueStmt()

    def visitReturnStmt(self, ctx: TyCParser.ReturnStmtContext):
        """
        returnStmt: RETURN expr? SEMI
        Returns: ReturnStmt
        """
        return ReturnStmt(self.visit(ctx.expr()) if ctx.expr() else None)

    def visitExprStmt(self, ctx: TyCParser.ExprStmtContext):
        """
        exprStmt: expr SEMI
        Returns: ExprStmt
        """
        return ExprStmt(self.visit(ctx.expr()))

    # =========================================================================
    # Expressions
    #
    # The grammar uses labeled alternatives (#labelName) for the expr rule.
    # ANTLR generates separate Context classes for each label:
    #   PrimaryExprContext, MemberAccessContext, PostfixExprContext,
    #   UnaryExprContext, BinaryExprContext, AssignExprContext
    # =========================================================================

    def visitPrimaryExpr(self, ctx: TyCParser.PrimaryExprContext):
        """
        expr: primary   #primaryExpr
        Delegates to visitPrimary.
        """
        return self.visit(ctx.primary())

    def visitMemberAccess(self, ctx: TyCParser.MemberAccessContext):
        """
        expr: expr DOT ID   #memberAccess
        Returns: 
        MemberAccess
        
        Left-recursive → ANTLR handles nesting automatically.
        e.g., a.b.c → MemberAccess(MemberAccess(Identifier(a), b), c)
        """
        return MemberAccess(self.visit(ctx.expr()), ctx.ID().getText())

    def visitPostfixExpr(self, ctx: TyCParser.PostfixExprContext):
        """
        expr: expr (INC | DEC | LPAREN argList? RPAREN)   #postfixExpr
        Returns: PostfixOp (for ++ / --) or FuncCall (for function call)
        
        Assumption: when LPAREN is present, expr must be an Identifier.
        We extract the function name from the left expr node.
        """
        left_expr = self.visit(ctx.expr())

        if ctx.INC():
            return PostfixOp('++', left_expr)
        elif ctx.DEC():
            return PostfixOp('--', left_expr)
        else:
            # Function call: expr LPAREN argList? RPAREN
            # The called expression should be a simple Identifier
            if isinstance(left_expr, Identifier):
                name = left_expr.name
            else:
                # Fallback: stringify — should not happen in valid TyC
                name = str(left_expr)
            args = self.visit(ctx.argList()) if ctx.argList() else []
            return FuncCall(name, args)

    def visitUnaryExpr(self, ctx: TyCParser.UnaryExprContext):
        """
        expr: (NOT | SUB | ADD | INC | DEC) expr   #unaryExpr
        Returns: PrefixOp
        """
        # The operator is the first child (a terminal node)
        return PrefixOp(ctx.getChild(0).getText(), self.visit(ctx.expr()))

    def visitBinaryExpr(self, ctx: TyCParser.BinaryExprContext):
        """
        expr: expr (MUL|DIV|MOD) expr   #binaryExpr
             | expr (ADD|SUB) expr      #binaryExpr
             | expr (LT|LTE|GT|GTE) expr #binaryExpr
             | expr (EQ|NEQ) expr       #binaryExpr
             | expr AND expr            #binaryExpr
             | expr OR expr             #binaryExpr
        Returns: BinaryOp
        
        The operator is always child(1) — the middle token.
        """
        left_expr = self.visit(ctx.expr(0))
        operator = ctx.getChild(1).getText()
        right_expr = self.visit(ctx.expr(1))
        return BinaryOp(left_expr, operator, right_expr)

    def visitAssignExpr(self, ctx: TyCParser.AssignExprContext):
        """
        expr: expr ASSIGN expr   #assignExpr   (<assoc=right>)
        Returns: AssignExpr
        
        lhs is Identifier or MemberAccess.
        Right-associativity is handled by ANTLR automatically.
        """
        return AssignExpr(self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitArgList(self, ctx: TyCParser.ArgListContext):
        """
        argList: expr (COMMA expr)*
        Returns: List[Expr]
        """
        return [self.visit(e) for e in ctx.expr()]

    # =========================================================================
    # Primary expressions
    # =========================================================================

    def visitPrimary(self, ctx: TyCParser.PrimaryContext):
        """
        primary: ID
               | INT_LIT
               | FLOAT_LIT
               | STRING_LIT
               | structLiteral
               | LPAREN expr RPAREN
        Returns: Identifier | IntLiteral | FloatLiteral | StringLiteral
                | StructLiteral | Expr (unwrapped parenthesized expr)
        """
        if ctx.ID():
            return Identifier(ctx.ID().getText())
        elif ctx.INT_LIT():
            return IntLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.STRING_LIT():
            # ANTLR's emit() already stripped the surrounding quotes
            return StringLiteral(ctx.STRING_LIT().getText())
        elif ctx.structLiteral():
            return self.visit(ctx.structLiteral())
        else:
            # LPAREN expr RPAREN — parenthesized expression; unwrap it
            return self.visit(ctx.expr())

    def visitStructLiteral(self, ctx: TyCParser.StructLiteralContext):
        """
        structLiteral: LBRACE argList? RBRACE
        Returns: StructLiteral
        """
        values = self.visit(ctx.argList()) if ctx.argList() else []
        return StructLiteral(values)