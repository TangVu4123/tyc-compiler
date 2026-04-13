"""
AST Generation test cases for TyC compiler.
TODO: Implement 100 test cases for AST generation
"""

import pytest
from tests.utils import ASTGenerator
from src.utils.nodes import *

def test_ast_gen_placeholder():
    """Placeholder test - replace with actual test cases"""
    source = """void main() {
}"""
    # TODO: Add actual test assertions
    # Example:
    # expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    # assert str(ASTGenerator(source).generate()) == expected
    assert True

"""
AST Generation test cases for TyC compiler.

Bộ test này được tổ chức theo các nhóm:
  1.  Program & top-level declarations (struct, func)
  2.  Types (primitive, struct, void, auto)
  3.  Variable declarations
  4.  Control flow — if/else
  5.  Control flow — while / for
  6.  Control flow — switch/case/default
  7.  Jump statements — break / continue / return
  8.  Expressions — binary operators & precedence
  9.  Expressions — unary (prefix / postfix)
  10. Expressions — assignment (simple & chained, rhs is expr)
  11. Expressions — member access (single & nested)
  12. Expressions — function calls
  13. Expressions — struct literals
  14. Literals — int / float / string edge cases
  15. Parenthesized expressions (unwrapping)
  16. Interleaved / complex / compound cases
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def gen(source: str) -> str:
    """Generate AST string from TyC source code."""
    return str(ASTGenerator(source).generate())


# ===========================================================================
# 1. Program & Top-level Declarations
# ===========================================================================
 
def test_001_empty_program():
    """Program rỗng không có khai báo nào."""
    expected = Program([])
    assert gen("") == str(expected)
 
 
def test_002_func_void_no_params_empty_body():
    """Hàm đơn giản nhất: void, không tham số, thân rỗng."""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([]))
    ])
    assert gen("void main() {}") == str(expected)
 
 
def test_003_func_int_return_type():
    expected = Program([FuncDecl(IntType(), "f", [], BlockStmt([]))])
    assert gen("int f() {}") == str(expected)
 
 
def test_004_func_float_return_type():
    expected = Program([FuncDecl(FloatType(), "f", [], BlockStmt([]))])
    assert gen("float f() {}") == str(expected)
 
 
def test_005_func_string_return_type():
    expected = Program([FuncDecl(StringType(), "f", [], BlockStmt([]))])
    assert gen("string f() {}") == str(expected)
 
 
def test_006_func_struct_return_type():
    """Hàm trả về struct type."""
    expected = Program([
        FuncDecl(StructType("Point"), "makePoint", [], BlockStmt([]))
    ])
    assert gen("Point makePoint() {}") == str(expected)
 
 
def test_007_func_auto_return_type():
    """Hàm không khai báo kiểu trả về → auto (return_type = None)."""
    expected = Program([
        FuncDecl(None, "compute", [], BlockStmt([ReturnStmt(IntLiteral(1))]))
    ])
    assert gen("compute() { return 1; }") == str(expected)
 
 
def test_008_func_single_int_param():
    expected = Program([
        FuncDecl(VoidType(), "f", [Param(IntType(), "x")], BlockStmt([]))
    ])
    assert gen("void f(int x) {}") == str(expected)
 
 
def test_009_func_multiple_params():
    expected = Program([
        FuncDecl(
            VoidType(), "f",
            [Param(IntType(), "a"), Param(FloatType(), "b"), Param(StringType(), "c")],
            BlockStmt([])
        )
    ])
    assert gen("void f(int a, float b, string c) {}") == str(expected)
 
 
def test_010_func_struct_param():
    expected = Program([
        FuncDecl(VoidType(), "f", [Param(StructType("Point"), "p")], BlockStmt([]))
    ])
    assert gen("void f(Point p) {}") == str(expected)
 
 
def test_011_struct_empty():
    expected = Program([StructDecl("Empty", [])])
    assert gen("struct Empty {};") == str(expected)
 
 
def test_012_struct_primitive_members():
    expected = Program([
        StructDecl("S", [
            MemberDecl(IntType(), "a"),
            MemberDecl(FloatType(), "b"),
            MemberDecl(StringType(), "c"),
        ])
    ])
    assert gen("struct S { int a; float b; string c; };") == str(expected)
 
 
def test_013_struct_nested_type_member():
    """Member có kiểu là struct khác → StructType."""
    expected = Program([
        StructDecl("Line", [
            MemberDecl(StructType("Point"), "p1"),
            MemberDecl(StructType("Point"), "p2"),
        ])
    ])
    assert gen("struct Line { Point p1; Point p2; };") == str(expected)
 
 
def test_014_program_preserves_decl_order():
    """Program giữ đúng thứ tự khai báo."""
    src = "struct P { int x; }; void f() {} int g() { return 1; }"
    expected = Program([
        StructDecl("P", [MemberDecl(IntType(), "x")]),
        FuncDecl(VoidType(), "f", [], BlockStmt([])),
        FuncDecl(IntType(), "g", [], BlockStmt([ReturnStmt(IntLiteral(1))])),
    ])
    assert gen(src) == str(expected)
 
 
# ===========================================================================
# 2. Variable Declarations
# ===========================================================================
 
def test_015_vardecl_int_no_init():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([VarDecl(IntType(), "x")]))
    ])
    assert gen("void f() { int x; }") == str(expected)
 
 
def test_016_vardecl_float_with_init():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(FloatType(), "pi", FloatLiteral(3.14))
        ]))
    ])
    assert gen("void f() { float pi = 3.14; }") == str(expected)
 
 
def test_017_vardecl_auto_with_int():
    """auto x = 5 → var_type = None."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([VarDecl(None, "x", IntLiteral(5))]))
    ])
    assert gen("void f() { auto x = 5; }") == str(expected)
 
 
def test_018_vardecl_struct_type_no_init():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([VarDecl(StructType("Point"), "p")]))
    ])
    assert gen("void f() { Point p; }") == str(expected)
 
 
def test_019_vardecl_string_with_literal():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(StringType(), "s", StringLiteral("hello"))
        ]))
    ])
    assert gen('void f() { string s = "hello"; }') == str(expected)
 
 
def test_020_vardecl_auto_func_call():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(None, "r", FuncCall("foo", []))
        ]))
    ])
    assert gen("void f() { auto r = foo(); }") == str(expected)
 
 
def test_021_vardecl_order_preserved():
    """Nhiều khai báo biến giữ đúng thứ tự trong block."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(IntType(), "a"),
            VarDecl(FloatType(), "b"),
            VarDecl(StringType(), "c"),
        ]))
    ])
    assert gen("void f() { int a; float b; string c; }") == str(expected)
 
 
# ===========================================================================
# 3. Control flow — if/else
# ===========================================================================
 
def test_022_if_no_else():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            IfStmt(Identifier("x"), ReturnStmt())
        ]))
    ])
    assert gen("void f() { if (x) return; }") == str(expected)
 
 
def test_023_if_with_else():
    expected = Program([
        FuncDecl(IntType(), "f", [], BlockStmt([
            IfStmt(Identifier("x"), ReturnStmt(IntLiteral(1)), ReturnStmt(IntLiteral(0)))
        ]))
    ])
    assert gen("int f() { if (x) return 1; else return 0; }") == str(expected)
 
 
def test_024_if_block_body():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            IfStmt(Identifier("ok"), BlockStmt([ReturnStmt()]))
        ]))
    ])
    assert gen("void f() { if (ok) { return; } }") == str(expected)
 
 
def test_025_if_else_dangling():
    """Dangling-else: else gắn với if trong cùng — chỉ có đúng 1 else."""
    result = gen("void f() { if (a) if (b) return; else return; }")
    assert result.count(", else ") == 1
 
 
def test_026_if_condition_binary():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            IfStmt(
                BinaryOp(Identifier("x"), ">", IntLiteral(0)),
                ReturnStmt(Identifier("x"))
            )
        ]))
    ])
    assert gen("void f() { if (x > 0) return x; }") == str(expected)
 
 
# ===========================================================================
# 4. Control flow — while / for
# ===========================================================================
 
def test_027_while_basic():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            WhileStmt(
                BinaryOp(Identifier("x"), ">", IntLiteral(0)),
                ExprStmt(PostfixOp("--", Identifier("x")))
            )
        ]))
    ])
    assert gen("void f() { while (x > 0) x--; }") == str(expected)
 
 
def test_028_while_empty_body():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            WhileStmt(IntLiteral(1), BlockStmt([]))
        ]))
    ])
    assert gen("void f() { while (1) {} }") == str(expected)
 
 
def test_029_for_full():
    """For đầy đủ ba clause."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ForStmt(
                VarDecl(IntType(), "i", IntLiteral(0)),
                BinaryOp(Identifier("i"), "<", IntLiteral(10)),
                PostfixOp("++", Identifier("i")),
                BlockStmt([])
            )
        ]))
    ])
    assert gen("void f() { for (int i = 0; i < 10; i++) {} }") == str(expected)
 
 
def test_030_for_empty_init():
    """For với bare SEMI init → init = None."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ForStmt(
                None,
                BinaryOp(Identifier("i"), "<", IntLiteral(10)),
                PostfixOp("++", Identifier("i")),
                BlockStmt([])
            )
        ]))
    ])
    assert gen("void f() { for (; i < 10; i++) {} }") == str(expected)
 
 
def test_031_for_expr_init_condition_and_update():
    """For với exprStmt init — condition VÀ update đều phải có đủ."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ForStmt(
                ExprStmt(AssignExpr(Identifier("i"), IntLiteral(0))),
                BinaryOp(Identifier("i"), "<", IntLiteral(5)),
                PostfixOp("++", Identifier("i")),
                BlockStmt([])
            )
        ]))
    ])
    assert gen("void f() { for (i = 0; i < 5; i++) {} }") == str(expected)
 
 
def test_032_for_all_empty():
    """For(;;) — tất cả clause đều None."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ForStmt(None, None, None, BlockStmt([]))
        ]))
    ])
    assert gen("void f() { for (;;) {} }") == str(expected)
 
 
def test_033_for_empty_condition():
    """For với condition rỗng → condition = None."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ForStmt(
                VarDecl(IntType(), "i", IntLiteral(0)),
                None,
                PostfixOp("++", Identifier("i")),
                BlockStmt([])
            )
        ]))
    ])
    assert gen("void f() { for (int i = 0; ; i++) {} }") == str(expected)
 
 
# ===========================================================================
# 5. Control flow — switch/case/default
# ===========================================================================
 
def test_034_switch_no_cases():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            SwitchStmt(Identifier("x"), [])
        ]))
    ])
    assert gen("void f() { switch (x) {} }") == str(expected)
 
 
def test_035_switch_single_case_break():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            SwitchStmt(
                Identifier("x"),
                [CaseStmt(IntLiteral(1), [
                    ExprStmt(AssignExpr(Identifier("x"), IntLiteral(10))),
                    BreakStmt()
                ])]
            )
        ]))
    ])
    assert gen("void f() { switch (x) { case 1: x = 10; break; } }") == str(expected)
 
 
def test_036_switch_default_only():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            SwitchStmt(Identifier("x"), [], DefaultStmt([BreakStmt()]))
        ]))
    ])
    assert gen("void f() { switch (x) { default: break; } }") == str(expected)
 
 
def test_037_switch_cases_and_default():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            SwitchStmt(
                Identifier("x"),
                [
                    CaseStmt(IntLiteral(0), [BreakStmt()]),
                    CaseStmt(IntLiteral(1), [
                        ExprStmt(AssignExpr(Identifier("x"), IntLiteral(1))),
                        BreakStmt()
                    ]),
                ],
                DefaultStmt([ExprStmt(AssignExpr(Identifier("x"), PrefixOp("-", IntLiteral(1))))])
            )
        ]))
    ])
    assert gen("void f() { switch (x) { case 0: break; case 1: x = 1; break; default: x = -1; } }") == str(expected)
 
 
def test_038_switch_case_fallthrough():
    """Case không có break — statement list rỗng."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            SwitchStmt(
                Identifier("x"),
                [
                    CaseStmt(IntLiteral(1), []),
                    CaseStmt(IntLiteral(2), [BreakStmt()]),
                ]
            )
        ]))
    ])
    assert gen("void f() { switch (x) { case 1: case 2: break; } }") == str(expected)
 
 
def test_039_switch_case_with_vardecl():
    """Case body có thể chứa VarDecl."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            SwitchStmt(
                Identifier("x"),
                [CaseStmt(IntLiteral(1), [VarDecl(IntType(), "y", IntLiteral(5)), BreakStmt()])]
            )
        ]))
    ])
    assert gen("void f() { switch (x) { case 1: int y = 5; break; } }") == str(expected)
 
 
# ===========================================================================
# 6. Jump statements
# ===========================================================================
 
def test_040_return_void():
    expected = Program([FuncDecl(VoidType(), "f", [], BlockStmt([ReturnStmt()]))])
    assert gen("void f() { return; }") == str(expected)
 
 
def test_041_return_int_literal():
    expected = Program([FuncDecl(IntType(), "f", [], BlockStmt([ReturnStmt(IntLiteral(42))]))])
    assert gen("int f() { return 42; }") == str(expected)
 
 
def test_042_return_expression():
    expected = Program([
        FuncDecl(IntType(), "f", [], BlockStmt([
            ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
        ]))
    ])
    assert gen("int f() { return a + b; }") == str(expected)
 
 
def test_043_break_stmt():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            WhileStmt(IntLiteral(1), BlockStmt([BreakStmt()]))
        ]))
    ])
    assert gen("void f() { while (1) { break; } }") == str(expected)
 
 
def test_044_continue_stmt():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            WhileStmt(IntLiteral(1), BlockStmt([ContinueStmt()]))
        ]))
    ])
    assert gen("void f() { while (1) { continue; } }") == str(expected)
 
 
# ===========================================================================
# 7. Binary operators & precedence
# ===========================================================================
 
def test_045_binary_add():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(IntType(), "r", BinaryOp(Identifier("a"), "+", Identifier("b")))
        ]))
    ])
    assert gen("void f() { int r = a + b; }") == str(expected)
 
 
def test_046_binary_all_arithmetic():
    """Tất cả phép toán số học."""
    for op in ["+", "-", "*", "/", "%"]:
        result = gen(f"void f() {{ int r = a {op} b; }}")
        assert str(BinaryOp(Identifier("a"), op, Identifier("b"))) in result
 
 
def test_047_binary_all_comparison():
    """Tất cả phép so sánh."""
    for op in ["<", ">", "<=", ">=", "==", "!="]:
        result = gen(f"void f() {{ int r = a {op} b; }}")
        assert str(BinaryOp(Identifier("a"), op, Identifier("b"))) in result
 
 
def test_048_precedence_mul_over_add():
    """* ưu tiên hơn +: 1 + 2 * 3 → ADD(1, MUL(2,3))."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(IntType(), "r",
                BinaryOp(IntLiteral(1), "+", BinaryOp(IntLiteral(2), "*", IntLiteral(3)))
            )
        ]))
    ])
    assert gen("void f() { int r = 1 + 2 * 3; }") == str(expected)
 
 
def test_049_precedence_cmp_over_logical():
    """So sánh ưu tiên hơn &&: a<b && c>d → AND(LT(a,b), GT(c,d))."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(IntType(), "r",
                BinaryOp(
                    BinaryOp(Identifier("a"), "<", Identifier("b")),
                    "&&",
                    BinaryOp(Identifier("c"), ">", Identifier("d"))
                )
            )
        ]))
    ])
    assert gen("void f() { int r = a < b && c > d; }") == str(expected)
 
 
def test_050_left_associativity():
    """a - b - c → BinaryOp(BinaryOp(a,-,b), -, c)."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(IntType(), "r",
                BinaryOp(BinaryOp(Identifier("a"), "-", Identifier("b")), "-", Identifier("c"))
            )
        ]))
    ])
    assert gen("void f() { int r = a - b - c; }") == str(expected)
 
 
def test_051_logical_and_over_or():
    """&& ưu tiên hơn ||: a && b || c → OR(AND(a,b), c)."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(IntType(), "r",
                BinaryOp(
                    BinaryOp(Identifier("a"), "&&", Identifier("b")),
                    "||",
                    Identifier("c")
                )
            )
        ]))
    ])
    assert gen("void f() { int r = a && b || c; }") == str(expected)
 
 
# ===========================================================================
# 8. Unary operators (prefix / postfix)
# ===========================================================================
 
def test_052_prefix_increment():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([ExprStmt(PrefixOp("++", Identifier("x")))]))
    ])
    assert gen("void f() { ++x; }") == str(expected)
 
 
def test_053_prefix_decrement():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([ExprStmt(PrefixOp("--", Identifier("x")))]))
    ])
    assert gen("void f() { --x; }") == str(expected)
 
 
def test_054_prefix_negate():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([ExprStmt(PrefixOp("-", Identifier("x")))]))
    ])
    assert gen("void f() { -x; }") == str(expected)
 
 
def test_055_prefix_not():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([ExprStmt(PrefixOp("!", Identifier("flag")))]))
    ])
    assert gen("void f() { !flag; }") == str(expected)
 
 
def test_056_postfix_increment():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([ExprStmt(PostfixOp("++", Identifier("x")))]))
    ])
    assert gen("void f() { x++; }") == str(expected)
 
 
def test_057_postfix_decrement():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([ExprStmt(PostfixOp("--", Identifier("x")))]))
    ])
    assert gen("void f() { x--; }") == str(expected)
 
 
def test_058_prefix_vs_postfix_distinct():
    """++x và x++ tạo node khác nhau."""
    pre  = gen("void f() { ++x; }")
    post = gen("void f() { x++; }")
    assert str(PrefixOp("++", Identifier("x")))  in pre   and str(PostfixOp("++", Identifier("x"))) not in pre
    assert str(PostfixOp("++", Identifier("x"))) in post  and str(PrefixOp("++", Identifier("x")))  not in post
 
 
def test_059_prefix_on_member():
    """++p.x — prefix trên member access."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(PrefixOp("++", MemberAccess(Identifier("p"), "x")))
        ]))
    ])
    assert gen("void f() { ++p.x; }") == str(expected)
 
 
def test_060_postfix_on_member():
    """p.x++ — postfix trên member access."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(PostfixOp("++", MemberAccess(Identifier("p"), "x")))
        ]))
    ])
    assert gen("void f() { p.x++; }") == str(expected)
 
 
# ===========================================================================
# 9. Assignment expressions
# ===========================================================================
 
def test_061_assign_simple():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("x"), IntLiteral(5)))
        ]))
    ])
    assert gen("void f() { x = 5; }") == str(expected)
 
 
def test_062_assign_right_associative():
    """a = b = 5 → AssignExpr(a, AssignExpr(b, 5))."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("a"), AssignExpr(Identifier("b"), IntLiteral(5))))
        ]))
    ])
    assert gen("void f() { a = b = 5; }") == str(expected)
 
 
def test_063_assign_triple_chain():
    """a = b = c = 0 — triple right-assoc."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(
                AssignExpr(
                    Identifier("a"),
                    AssignExpr(Identifier("b"), AssignExpr(Identifier("c"), IntLiteral(0)))
                )
            )
        ]))
    ])
    assert gen("void f() { a = b = c = 0; }") == str(expected)
 
 
def test_064_assign_to_member():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(AssignExpr(MemberAccess(Identifier("p"), "x"), IntLiteral(10)))
        ]))
    ])
    assert gen("void f() { p.x = 10; }") == str(expected)
 
 
def test_065_assign_complex_rhs():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(
                AssignExpr(
                    Identifier("x"),
                    BinaryOp(Identifier("a"), "+", BinaryOp(Identifier("b"), "*", Identifier("c")))
                )
            )
        ]))
    ])
    assert gen("void f() { x = a + b * c; }") == str(expected)
 
 
# ===========================================================================
# 10. Member access
# ===========================================================================
 
def test_066_member_access_single():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(MemberAccess(Identifier("p"), "x"))
        ]))
    ])
    assert gen("void f() { p.x; }") == str(expected)
 
 
def test_067_member_access_double():
    """a.b.c → MemberAccess(MemberAccess(a,b), c)."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(MemberAccess(MemberAccess(Identifier("a"), "b"), "c"))
        ]))
    ])
    assert gen("void f() { a.b.c; }") == str(expected)
 
 
def test_068_member_access_triple():
    """a.b.c.d — ba tầng lồng."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(MemberAccess(MemberAccess(MemberAccess(Identifier("a"), "b"), "c"), "d"))
        ]))
    ])
    assert gen("void f() { a.b.c.d; }") == str(expected)
 
 
def test_069_member_access_in_condition():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            IfStmt(MemberAccess(Identifier("s"), "ok"), ReturnStmt())
        ]))
    ])
    assert gen("void f() { if (s.ok) return; }") == str(expected)
 
 
# ===========================================================================
# 11. Function calls
# ===========================================================================
 
def test_070_funcCall_no_args():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([ExprStmt(FuncCall("foo", []))]))
    ])
    assert gen("void f() { foo(); }") == str(expected)
 
 
def test_071_funcCall_one_arg():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(FuncCall("print", [Identifier("x")]))
        ]))
    ])
    assert gen("void f() { print(x); }") == str(expected)
 
 
def test_072_funcCall_multiple_args():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(FuncCall("add", [IntLiteral(1), FloatLiteral(2.0), StringLiteral("hi")]))
        ]))
    ])
    assert gen('void f() { add(1, 2.0, "hi"); }') == str(expected)
 
 
def test_073_funcCall_expr_arg():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(FuncCall("foo", [BinaryOp(Identifier("a"), "+", Identifier("b"))]))
        ]))
    ])
    assert gen("void f() { foo(a + b); }") == str(expected)
 
 
def test_074_funcCall_nested():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(FuncCall("outer", [FuncCall("inner", [Identifier("x")])]))
        ]))
    ])
    assert gen("void f() { outer(inner(x)); }") == str(expected)
 
 
def test_075_funcCall_result_assigned():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(None, "r", FuncCall("compute", [Identifier("a"), Identifier("b")]))
        ]))
    ])
    assert gen("void f() { auto r = compute(a, b); }") == str(expected)
 
 
def test_076_funcCall_in_condition():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            IfStmt(FuncCall("isValid", [Identifier("x")]), ReturnStmt())
        ]))
    ])
    assert gen("void f() { if (isValid(x)) return; }") == str(expected)
 
 
# ===========================================================================
# 12. Struct literals
# ===========================================================================
 
def test_077_struct_literal_empty():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([VarDecl(None, "p", StructLiteral([]))]))
    ])
    assert gen("void f() { auto p = {}; }") == str(expected)
 
 
def test_078_struct_literal_one_value():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(None, "p", StructLiteral([IntLiteral(1)]))
        ]))
    ])
    assert gen("void f() { auto p = {1}; }") == str(expected)
 
 
def test_079_struct_literal_multiple_values():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(None, "p", StructLiteral([IntLiteral(1), FloatLiteral(2.5), Identifier("x")]))
        ]))
    ])
    assert gen("void f() { auto p = {1, 2.5, x}; }") == str(expected)
 
 
def test_080_struct_literal_nested():
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(None, "t", StructLiteral([
                StructLiteral([IntLiteral(1), IntLiteral(2)]),
                StructLiteral([IntLiteral(3), IntLiteral(4)]),
            ]))
        ]))
    ])
    assert gen("void f() { auto t = {{1, 2}, {3, 4}}; }") == str(expected)
 
 
# ===========================================================================
# 13. Literals — edge cases
# ===========================================================================
 
def test_081_int_literal_zero():
    expected = Program([FuncDecl(VoidType(), "f", [], BlockStmt([VarDecl(IntType(), "x", IntLiteral(0))]))])
    assert gen("void f() { int x = 0; }") == str(expected)
 
 
def test_082_int_literal_large():
    expected = Program([FuncDecl(VoidType(), "f", [], BlockStmt([VarDecl(IntType(), "x", IntLiteral(999999))]))])
    assert gen("void f() { int x = 999999; }") == str(expected)
 
 
def test_083_float_literal_decimal():
    expected = Program([FuncDecl(VoidType(), "f", [], BlockStmt([VarDecl(FloatType(), "x", FloatLiteral(3.14))]))])
    assert gen("void f() { float x = 3.14; }") == str(expected)
 
 
def test_084_float_literal_exponent():
    """1e5 → FloatLiteral(100000.0)."""
    expected = Program([FuncDecl(VoidType(), "f", [], BlockStmt([VarDecl(FloatType(), "x", FloatLiteral(1e5))]))])
    assert gen("void f() { float x = 1e5; }") == str(expected)
 
 
def test_085_float_literal_leading_dot():
    """.5 là float hợp lệ → FloatLiteral(0.5)."""
    expected = Program([FuncDecl(VoidType(), "f", [], BlockStmt([VarDecl(FloatType(), "x", FloatLiteral(0.5))]))])
    assert gen("void f() { float x = .5; }") == str(expected)
 
 
def test_086_string_literal_empty():
    expected = Program([FuncDecl(VoidType(), "f", [], BlockStmt([VarDecl(StringType(), "s", StringLiteral(""))]))])
    assert gen('void f() { string s = ""; }') == str(expected)
 
 
def test_087_string_literal_no_outer_quotes():
    """StringLiteral.value không bao gồm dấu ngoặc bao ngoài."""
    expected = Program([FuncDecl(VoidType(), "f", [], BlockStmt([VarDecl(StringType(), "s", StringLiteral("abc"))]))])
    result = gen('void f() { string s = "abc"; }')
    assert result == str(expected)
    assert "StringLiteral('abc')" in result
 
 
def test_088_string_literal_with_escape():
    """String với escape sequence — ít nhất phải parse được."""
    result = gen(r'void f() { string s = "hello\nworld"; }')
    assert "StringLiteral(" in result
    assert "hello" in result
 
 
# ===========================================================================
# 14. Parenthesized expressions
# ===========================================================================
 
def test_089_paren_unwrap():
    """(5) được unwrap — AST giống hệt không có ngoặc."""
    assert gen("void f() { int x = (5); }") == gen("void f() { int x = 5; }")
 
 
def test_090_paren_changes_precedence():
    """(1 + 2) * 3 → MUL(ADD(1,2), 3)."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(IntType(), "r",
                BinaryOp(BinaryOp(IntLiteral(1), "+", IntLiteral(2)), "*", IntLiteral(3))
            )
        ]))
    ])
    assert gen("void f() { int r = (1 + 2) * 3; }") == str(expected)
 
 
def test_091_paren_nested_double():
    """((a + b)) — hai tầng ngoặc đều unwrap."""
    assert gen("void f() { int r = ((a + b)); }") == gen("void f() { int r = a + b; }")
 
 
# ===========================================================================
# 15. Complex / compound cases
# ===========================================================================
 
def test_092_block_interleaved_order():
    """Block với VarDecl và stmt xen kẽ — thứ tự tuyệt đối."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(IntType(), "a", IntLiteral(1)),
            ExprStmt(AssignExpr(Identifier("a"), IntLiteral(2))),
            VarDecl(IntType(), "b", IntLiteral(3)),
            ExprStmt(AssignExpr(Identifier("b"), IntLiteral(4))),
        ]))
    ])
    assert gen("void f() { int a = 1; a = 2; int b = 3; b = 4; }") == str(expected)
 
 
def test_093_complex_precedence_chain():
    """!a && b || c → OR(AND(!a, b), c)."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            VarDecl(IntType(), "x",
                BinaryOp(
                    BinaryOp(PrefixOp("!", Identifier("a")), "&&", Identifier("b")),
                    "||",
                    Identifier("c")
                )
            )
        ]))
    ])
    assert gen("void f() { int x = !a && b || c; }") == str(expected)
 
 
def test_094_nested_control_flow():
    """For lồng trong while lồng trong if."""
    src = """
    void f() {
        if (x > 0) {
            while (y > 0) {
                for (int i = 0; i < y; i++) {
                    continue;
                }
            }
        }
    }
    """
    result = gen(src)
    assert "IfStmt(" in result
    assert "WhileStmt(" in result
    assert "ForStmt(" in result
    assert str(ContinueStmt()) in result
 
 
def test_095_func_call_in_for_update():
    """Update clause của for là function call."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ForStmt(
                VarDecl(IntType(), "i", IntLiteral(0)),
                BinaryOp(Identifier("i"), "<", IntLiteral(10)),
                FuncCall("next", [Identifier("i")]),
                BlockStmt([])
            )
        ]))
    ])
    assert gen("void f() { for (int i = 0; i < 10; next(i)) {} }") == str(expected)
 
 
def test_096_member_assign_in_for():
    """For với member access trong cả init, condition và update."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ForStmt(
                ExprStmt(AssignExpr(MemberAccess(Identifier("p"), "x"), IntLiteral(0))),
                BinaryOp(MemberAccess(Identifier("p"), "x"), "<", IntLiteral(10)),
                PostfixOp("++", MemberAccess(Identifier("p"), "x")),
                BlockStmt([])
            )
        ]))
    ])
    assert gen("void f() { for (p.x = 0; p.x < 10; p.x++) {} }") == str(expected)
 
 
def test_097_full_factorial():
    """Hàm tính giai thừa — tích hợp nhiều feature."""
    src = """
    int factorial(int n) {
        int result = 1;
        while (n > 1) {
            result = result * n;
            n = n - 1;
        }
        return result;
    }
    """
    expected = Program([
        FuncDecl(IntType(), "factorial", [Param(IntType(), "n")], BlockStmt([
            VarDecl(IntType(), "result", IntLiteral(1)),
            WhileStmt(
                BinaryOp(Identifier("n"), ">", IntLiteral(1)),
                BlockStmt([
                    ExprStmt(AssignExpr(Identifier("result"),
                        BinaryOp(Identifier("result"), "*", Identifier("n")))),
                    ExprStmt(AssignExpr(Identifier("n"),
                        BinaryOp(Identifier("n"), "-", IntLiteral(1)))),
                ])
            ),
            ReturnStmt(Identifier("result"))
        ]))
    ])
    assert gen(src) == str(expected)
 
 
def test_098_struct_member_as_func_args():
    """Member access làm đối số function call."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            ExprStmt(FuncCall("draw", [
                MemberAccess(Identifier("p"), "x"),
                MemberAccess(Identifier("p"), "y"),
            ]))
        ]))
    ])
    assert gen("void f() { draw(p.x, p.y); }") == str(expected)
 
 
def test_099_assign_in_while_condition():
    """Assignment expression làm condition của while."""
    expected = Program([
        FuncDecl(VoidType(), "f", [], BlockStmt([
            WhileStmt(
                AssignExpr(Identifier("x"), FuncCall("read", [])),
                BlockStmt([ExprStmt(FuncCall("process", [Identifier("x")]))])
            )
        ]))
    ])
    assert gen("void f() { while (x = read()) { process(x); } }") == str(expected)
 
 
def test_100_struct_and_func_together():
    """Program với struct và function sử dụng struct type."""
    src = """
    struct Point { int x; int y; };
    int sum(Point p) { return p.x + p.y; }
    """
    expected = Program([
        StructDecl("Point", [
            MemberDecl(IntType(), "x"),
            MemberDecl(IntType(), "y"),
        ]),
        FuncDecl(IntType(), "sum", [Param(StructType("Point"), "p")], BlockStmt([
            ReturnStmt(BinaryOp(
                MemberAccess(Identifier("p"), "x"),
                "+",
                MemberAccess(Identifier("p"), "y")
            ))
        ]))
    ])
    assert gen(src) == str(expected)


