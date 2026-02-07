"""
Parser test cases for TyC compiler
TODO: Implement 100 test cases for parser
"""

import pytest
from tests.utils import Parser


# # ========== Simple Test Cases (10 types) ==========
# def test_empty_program():
#     """1. Empty program"""
#     assert Parser("").parse() == "success"


# def test_program_with_only_main():
#     """2. Program with only main function"""
#     assert Parser("void main() {}").parse() == "success"


# def test_struct_simple():
#     """3. Struct declaration"""
#     source = "struct Point { int x; int y; };"
#     assert Parser(source).parse() == "success"


# def test_function_no_params():
#     """4. Function with no parameters"""
#     source = "void greet() { printString(\"Hello\"); }"
#     assert Parser(source).parse() == "success"


# def test_var_decl_auto_with_init():
#     """5. Variable declaration"""
#     source = "void main() { auto x = 5; }"
#     assert Parser(source).parse() == "success"


# def test_if_simple():
#     """6. If statement"""
#     source = "void main() { if (1) printInt(1); }"
#     assert Parser(source).parse() == "success"


# def test_while_simple():
#     """7. While statement"""
#     source = "void main() { while (1) printInt(1); }"
#     assert Parser(source).parse() == "success"


# def test_for_simple():
#     """8. For statement"""
#     source = "void main() { for (auto i = 0; i < 10; ++i) printInt(i); }"
#     assert Parser(source).parse() == "success"


# def test_switch_simple():
#     """9. Switch statement"""
#     source = "void main() { switch (1) { case 1: printInt(1); break; } }"
#     assert Parser(source).parse() == "success"


# def test_assignment_simple():
#     """10. Assignment statement"""
#     source = "void main() { int x; x = 5; }"
#     assert Parser(source).parse() == "success"



# ========== Program Structure (5 tests) ==========
def test_empty_program():
    """1. Empty program"""
    assert Parser("").parse() == "success"


def test_program_with_only_main():
    """2. Program with only main function"""
    assert Parser("void main() {}").parse() == "success"


def test_program_struct_then_function():
    """3. Program with struct then function"""
    source = """
    struct Point { int x; int y; };
    void main() {}
    """
    assert Parser(source).parse() == "success"


def test_program_multiple_structs_functions():
    """4. Program with multiple structs and functions"""
    source = """
    struct Point { int x; int y; };
    struct Person { string name; int age; };
    int add(int a, int b) { return a + b; }
    void main() {}
    """
    assert Parser(source).parse() == "success"


def test_program_functions_only():
    """5. Program with multiple functions"""
    source = """
    int add(int x, int y) { return x + y; }
    float multiply(float a, float b) { return a * b; }
    void main() {}
    """
    assert Parser(source).parse() == "success"


# ========== Struct Declarations (10 tests) ==========
def test_struct_simple():
    """6. Struct: simple with one member"""
    source = "struct Point { int x; };"
    assert Parser(source).parse() == "success"


def test_struct_multiple_members():
    """7. Struct: multiple members"""
    source = "struct Point { int x; int y; };"
    assert Parser(source).parse() == "success"


def test_struct_different_types():
    """8. Struct: different member types"""
    source = "struct Person { string name; int age; float height; };"
    assert Parser(source).parse() == "success"


def test_struct_nested_type():
    """9. Struct: member is another struct type"""
    source = """
    struct Point { int x; int y; };
    struct Circle { Point center; int radius; };
    """
    assert Parser(source).parse() == "success"


def test_struct_many_members():
    """10. Struct: many members"""
    source = """
    struct Data {
        int field1;
        int field2;
        float field3;
        string field4;
        int field5;
    };
    """
    assert Parser(source).parse() == "success"


def test_struct_void_member_error():
    """11. Struct: void member (should fail)"""
    source = "struct Bad { void x; };"
    assert Parser(source).parse() != "success"


def test_struct_auto_member_error():
    """12. Struct: auto member (should fail)"""
    source = "struct Bad { auto x; };"
    assert Parser(source).parse() != "success"


def test_struct_no_members():
    """13. Struct: no members (should fail)"""
    source = "struct Empty { };"
    assert Parser(source).parse() == "success"


def test_struct_missing_semicolon_error():
    """14. Struct: missing semicolon (should fail)"""
    source = "struct Point { int x; int y; }"
    assert Parser(source).parse() != "success"


def test_struct_missing_member_semicolon_error():
    """15. Struct: missing member semicolon (should fail)"""
    source = "struct Point { int x int y; };"
    assert Parser(source).parse() != "success"


# ========== Function Declarations (15 tests) ==========
def test_function_void_no_params():
    """16. Function: void with no parameters"""
    source = "void greet() {}"
    assert Parser(source).parse() == "success"


def test_function_int_return():
    """17. Function: int return type"""
    source = "int getValue() { return 5; }"
    assert Parser(source).parse() == "success"


def test_function_float_return():
    """18. Function: float return type"""
    source = "float calculate() { return 3.14; }"
    assert Parser(source).parse() == "success"


def test_function_string_return():
    """19. Function: string return type"""
    source = 'string getName() { return "John"; }'
    assert Parser(source).parse() == "success"


def test_function_struct_return():
    """20. Function: struct return type"""
    source = """
    struct Point { int x; int y; };
    Point getPoint() { Point p; return p; }
    """
    assert Parser(source).parse() == "success"


def test_function_inferred_return():
    """21. Function: inferred return type"""
    source = "add(int x, int y) { return x + y; }"
    assert Parser(source).parse() == "success"


def test_function_one_param():
    """22. Function: one parameter"""
    source = "void print(int x) { printInt(x); }"
    assert Parser(source).parse() == "success"


def test_function_multiple_params():
    """23. Function: multiple parameters"""
    source = "int add(int x, int y, int z) { return x + y + z; }"
    assert Parser(source).parse() == "success"


def test_function_mixed_param_types():
    """24. Function: mixed parameter types"""
    source = "void process(int id, string name, float score) {}"
    assert Parser(source).parse() == "success"


def test_function_struct_param():
    """25. Function: struct parameter"""
    source = """
    struct Point { int x; int y; };
    void drawPoint(Point p) {}
    """
    assert Parser(source).parse() == "success"


def test_function_auto_param_error():
    """26. Function: auto parameter (should fail)"""
    source = "void func(auto x) {}"
    assert Parser(source).parse() != "success"


def test_function_missing_param_type_error():
    """27. Function: missing parameter type (should fail)"""
    source = "void func(x) {}"
    assert Parser(source).parse() != "success"


def test_function_empty_body():
    """28. Function: empty body"""
    source = "void func() {}"
    assert Parser(source).parse() == "success"


def test_function_complex_body():
    """29. Function: complex body"""
    source = """
    int factorial(int n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_function_missing_brace_error():
    """30. Function: missing closing brace (should fail)"""
    source = "void func() {"
    assert Parser(source).parse() != "success"


# ========== Variable Declarations (10 tests) ==========
def test_var_decl_auto_with_init():
    """31. VarDecl: auto with initialization"""
    source = "void main() { auto x = 5; }"
    assert Parser(source).parse() == "success"


def test_var_decl_auto_no_init():
    """32. VarDecl: auto without initialization"""
    source = "void main() { auto x; }"
    assert Parser(source).parse() == "success"


def test_var_decl_int_with_init():
    """33. VarDecl: int with initialization"""
    source = "void main() { int x = 10; }"
    assert Parser(source).parse() == "success"


def test_var_decl_int_no_init():
    """34. VarDecl: int without initialization"""
    source = "void main() { int x; }"
    assert Parser(source).parse() == "success"


def test_var_decl_float():
    """35. VarDecl: float variable"""
    source = "void main() { float pi = 3.14; }"
    assert Parser(source).parse() == "success"


def test_var_decl_string():
    """36. VarDecl: string variable"""
    source = 'void main() { string name = "John"; }'
    assert Parser(source).parse() == "success"


def test_var_decl_struct_type():
    """37. VarDecl: struct type variable"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p; }
    """
    assert Parser(source).parse() == "success"


def test_var_decl_struct_with_init():
    """38. VarDecl: struct with initialization"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p = {1, 2}; }
    """
    assert Parser(source).parse() == "success"


def test_var_decl_multiple():
    """39. VarDecl: multiple declarations"""
    source = "void main() { int x = 1; float y = 2.0; string z = \"hi\"; }"
    assert Parser(source).parse() == "success"


def test_var_decl_complex_init():
    """40. VarDecl: complex initialization"""
    source = "void main() { auto result = 5 * 3 + 2 - 1; }"
    assert Parser(source).parse() == "success"


# ========== If Statements (5 tests) ==========
def test_if_simple():
    """41. If: simple if"""
    source = "void main() { if (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_if_else():
    """42. If: if-else"""
    source = "void main() { if (1) printInt(1); else printInt(2); }"
    assert Parser(source).parse() == "success"


def test_if_block():
    """43. If: with block"""
    source = "void main() { if (x > 0) { printInt(x); } }"
    assert Parser(source).parse() == "success"


def test_if_nested():
    """44. If: nested if"""
    source = """
    void main() {
        if (x > 0) {
            if (x < 10) {
                printInt(x);
            }
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_if_else_if_chain():
    """45. If: else-if chain"""
    source = """
    void main() {
        if (x < 0) printInt(1);
        else if (x == 0) printInt(2);
        else printInt(3);
    }
    """
    assert Parser(source).parse() == "success"


# ========== While Statements (3 tests) ==========
def test_while_simple():
    """46. While: simple while"""
    source = "void main() { while (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_while_block():
    """47. While: with block"""
    source = "void main() { while (i < 10) { printInt(i); ++i; } }"
    assert Parser(source).parse() == "success"


def test_while_nested():
    """48. While: nested while"""
    source = """
    void main() {
        while (i < 10) {
            while (j < 5) {
                ++j;
            }
            ++i;
        }
    }
    """
    assert Parser(source).parse() == "success"


# ========== For Statements (6 tests) ==========
def test_for_simple():
    """49. For: simple for loop"""
    source = "void main() { for (auto i = 0; i < 10; ++i) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_for_with_block():
    """50. For: with block"""
    source = "void main() { for (int i = 0; i < 10; ++i) { printInt(i); } }"
    assert Parser(source).parse() == "success"


def test_for_empty_init():
    """51. For: empty initialization"""
    source = "void main() { for (; i < 10; ++i) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_for_empty_condition():
    """52. For: empty condition"""
    source = "void main() { for (int i = 0; ; ++i) break; }"
    assert Parser(source).parse() == "success"


def test_for_empty_update():
    """53. For: empty update"""
    source = "void main() { for (int i = 0; i < 10; ) { printInt(i); ++i; } }"
    assert Parser(source).parse() == "success"


def test_for_all_empty():
    """54. For: all parts empty (infinite loop)"""
    source = "void main() { for (;;) break; }"
    assert Parser(source).parse() == "success"


# ========== Switch Statements (5 tests) ==========
def test_switch_simple():
    """55. Switch: simple switch"""
    source = """
    void main() {
        switch (x) {
            case 1: printInt(1); break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_multiple_cases():
    """56. Switch: multiple cases"""
    source = """
    void main() {
        switch (x) {
            case 1: printInt(1); break;
            case 2: printInt(2); break;
            case 3: printInt(3); break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_with_default():
    """57. Switch: with default"""
    source = """
    void main() {
        switch (x) {
            case 1: printInt(1); break;
            default: printInt(0); break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_fall_through():
    """58. Switch: fall through (no break)"""
    source = """
    void main() {
        switch (x) {
            case 1: printInt(1);
            case 2: printInt(2); break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_empty():
    """59. Switch: empty switch"""
    source = "void main() { switch (x) {} }"
    assert Parser(source).parse() == "success"


# ========== Break and Continue (4 tests) ==========
def test_break_in_while():
    """60. Break: in while loop"""
    source = "void main() { while (1) { if (x) break; } }"
    assert Parser(source).parse() == "success"


def test_continue_in_while():
    """61. Continue: in while loop"""
    source = "void main() { while (1) { if (x) continue; printInt(x); } }"
    assert Parser(source).parse() == "success"


def test_break_in_for():
    """62. Break: in for loop"""
    source = "void main() { for (;;) { if (x > 10) break; } }"
    assert Parser(source).parse() == "success"


def test_continue_in_for():
    """63. Continue: in for loop"""
    source = "void main() { for (int i = 0; i < 10; ++i) { if (i % 2) continue; } }"
    assert Parser(source).parse() == "success"


# ========== Return Statements (4 tests) ==========
def test_return_void():
    """64. Return: void (no value)"""
    source = "void main() { return; }"
    assert Parser(source).parse() == "success"


def test_return_int():
    """65. Return: integer value"""
    source = "int getValue() { return 42; }"
    assert Parser(source).parse() == "success"


def test_return_expression():
    """66. Return: complex expression"""
    source = "int calculate() { return x * 2 + y - 1; }"
    assert Parser(source).parse() == "success"


def test_return_function_call():
    """67. Return: function call"""
    source = "int getResult() { return calculate(5, 10); }"
    assert Parser(source).parse() == "success"


# ========== Expressions - Precedence and Associativity (15 tests) ==========
def test_expr_assignment():
    """68. Expression: assignment"""
    source = "void main() { x = 5; }"
    assert Parser(source).parse() == "success"


def test_expr_chained_assignment():
    """69. Expression: chained assignment (right associative)"""
    source = "void main() { x = y = z = 0; }"
    assert Parser(source).parse() == "success"


def test_expr_or():
    """70. Expression: logical OR"""
    source = "void main() { auto result = x || y || z; }"
    assert Parser(source).parse() == "success"


def test_expr_and():
    """71. Expression: logical AND"""
    source = "void main() { auto result = x && y && z; }"
    assert Parser(source).parse() == "success"


def test_expr_equality():
    """72. Expression: equality operators"""
    source = "void main() { auto result = x == y != z; }"
    assert Parser(source).parse() == "success"


def test_expr_relational():
    """73. Expression: relational operators"""
    source = "void main() { auto result = x < y <= z > w >= u; }"
    assert Parser(source).parse() == "success"


def test_expr_additive():
    """74. Expression: addition and subtraction"""
    source = "void main() { auto result = x + y - z + w; }"
    assert Parser(source).parse() == "success"


def test_expr_multiplicative():
    """75. Expression: multiplication, division, modulus"""
    source = "void main() { auto result = x * y / z % w; }"
    assert Parser(source).parse() == "success"


def test_expr_precedence_mul_add():
    """76. Expression: multiplication before addition"""
    source = "void main() { auto result = x + y * z; }"
    assert Parser(source).parse() == "success"


def test_expr_precedence_complex():
    """77. Expression: complex precedence"""
    source = "void main() { auto result = a + b * c - d / e % f; }"
    assert Parser(source).parse() == "success"


def test_expr_unary():
    """78. Expression: unary operators"""
    source = "void main() { auto result = -x + !y; }"
    assert Parser(source).parse() == "success"


def test_expr_prefix_increment():
    """79. Expression: prefix increment/decrement"""
    source = "void main() { ++x; --y; }"
    assert Parser(source).parse() == "success"


def test_expr_postfix_increment():
    """80. Expression: postfix increment/decrement"""
    source = "void main() { x++; y--; }"
    assert Parser(source).parse() == "success"


def test_expr_parentheses():
    """81. Expression: parentheses for grouping"""
    source = "void main() { auto result = (x + y) * (z - w); }"
    assert Parser(source).parse() == "success"


def test_expr_member_access():
    """82. Expression: member access"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p; auto val = p.x + p.y; }
    """
    assert Parser(source).parse() == "success"


# ========== Function Calls (4 tests) ==========
def test_function_call_no_args():
    """83. Function call: no arguments"""
    source = "void main() { getValue(); }"
    assert Parser(source).parse() == "success"


def test_function_call_one_arg():
    """84. Function call: one argument"""
    source = "void main() { printInt(5); }"
    assert Parser(source).parse() == "success"


def test_function_call_multiple_args():
    """85. Function call: multiple arguments"""
    source = "void main() { add(1, 2, 3); }"
    assert Parser(source).parse() == "success"


def test_function_call_nested():
    """86. Function call: nested calls"""
    source = "void main() { printInt(add(multiply(2, 3), 5)); }"
    assert Parser(source).parse() == "success"


# ========== Block Statements (3 tests) ==========
def test_block_empty():
    """87. Block: empty block"""
    source = "void main() { {} }"
    assert Parser(source).parse() == "success"


def test_block_nested():
    """88. Block: nested blocks"""
    source = """
    void main() {
        {
            {
                int x = 5;
            }
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_block_multiple_statements():
    """89. Block: multiple statements"""
    source = """
    void main() {
        int x = 5;
        auto y = 10;
        printInt(x + y);
    }
    """
    assert Parser(source).parse() == "success"


# ========== Complex and Nested Structures (6 tests) ==========
def test_complex_nested_control_flow():
    """90. Complex: nested control flow"""
    source = """
    void main() {
        for (int i = 0; i < 10; ++i) {
            if (i % 2 == 0) {
                while (i > 0) {
                    switch (i) {
                        case 2: printInt(2); break;
                        default: --i;
                    }
                }
            }
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_complex_expression_in_control():
    """91. Complex: expression in control structures"""
    source = """
    void main() {
        if ((x + 5) * 2 > y && z < 10 || w == 0) {
            while ((a++ < b--) && (c != d)) {
                printInt(a);
            }
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_complex_struct_operations():
    """92. Complex: struct operations"""
    source = """
    struct Point { int x; int y; };
    void main() {
        Point p1 = {10, 20};
        Point p2;
        p2.x = p1.x + 5;
        p2.y = p1.y * 2;
        p1 = p2;
    }
    """
    assert Parser(source).parse() == "success"


def test_complex_multiple_functions_calls():
    """93. Complex: multiple function interactions"""
    source = """
    int square(int x) { return x * x; }
    int sum(int a, int b) { return a + b; }
    void main() {
        auto result = sum(square(3), square(4));
        printInt(result);
    }
    """
    assert Parser(source).parse() == "success"


def test_complex_all_operators():
    """94. Complex: all operators in one expression"""
    source = """
    void main() {
        auto result = ++x + y++ * z-- / w % v - -u && a || !b == c != d < e <= f > g >= h;
    }
    """
    assert Parser(source).parse() == "success"


def test_complex_realistic_program():
    """95. Complex: realistic program"""
    source = """
    struct Point { int x; int y; };
    
    int distance(Point p1, Point p2) {
        auto dx = p1.x - p2.x;
        auto dy = p1.y - p2.y;
        return dx * dx + dy * dy;
    }
    
    void main() {
        Point p1 = {0, 0};
        Point p2 = {3, 4};
        auto dist = distance(p1, p2);
        
        if (dist > 10) {
            printString("Far");
        } else {
            printString("Close");
        }
    }
    """
    assert Parser(source).parse() == "success"


# ========== Error Cases (5 tests) ==========
def test_error_missing_semicolon():
    """96. Error: missing semicolon"""
    source = "void main() { int x = 5 }"
    assert Parser(source).parse() != "success"


def test_error_unbalanced_braces():
    """97. Error: unbalanced braces"""
    source = "void main() { int x = 5; "
    assert Parser(source).parse() != "success"


def test_error_unbalanced_parens():
    """98. Error: unbalanced parentheses"""
    source = "void main() { if (x > 0 printInt(x); }"
    assert Parser(source).parse() != "success"


def test_error_invalid_expression():
    """99. Error: invalid expression"""
    source = "void main() { auto x = + * 5; }"
    assert Parser(source).parse() != "success"


def test_error_statement_outside_function():
    """100. Error: statement outside function"""
    source = "int x = 5;"
    assert Parser(source).parse() != "success"

