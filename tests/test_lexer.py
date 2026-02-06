"""
Lexer test cases for TyC compiler
TODO: Implement 100 test cases for lexer
"""

import pytest
from tests.utils import Tokenizer


# # ========== Simple Test Cases (10 types) ==========
# def test_keyword_auto():
#     """1. Keyword"""
#     tokenizer = Tokenizer("auto")
#     assert tokenizer.get_tokens_as_string() == "auto,<EOF>"


# def test_operator_assign():
#     """2. Operator"""
#     tokenizer = Tokenizer("=")
#     assert tokenizer.get_tokens_as_string() == "=,<EOF>"


# def test_separator_semi():
#     """3. Separator"""
#     tokenizer = Tokenizer(";")
#     assert tokenizer.get_tokens_as_string() == ";,<EOF>"


# def test_integer_single_digit():
#     """4. Integer literal"""
#     tokenizer = Tokenizer("5")
#     assert tokenizer.get_tokens_as_string() == "5,<EOF>"


# def test_float_decimal():
#     """5. Float literal"""
#     tokenizer = Tokenizer("3.14")
#     assert tokenizer.get_tokens_as_string() == "3.14,<EOF>"


# def test_string_simple():
#     """6. String literal"""
#     tokenizer = Tokenizer('"hello"')
#     assert tokenizer.get_tokens_as_string() == "hello,<EOF>"


# def test_identifier_simple():
#     """7. Identifier"""
#     tokenizer = Tokenizer("x")
#     assert tokenizer.get_tokens_as_string() == "x,<EOF>"


# def test_line_comment():
#     """8. Line comment"""
#     tokenizer = Tokenizer("// This is a comment")
#     assert tokenizer.get_tokens_as_string() == "<EOF>"


# def test_integer_in_expression():
#     """9. Mixed: integers and operator"""
#     tokenizer = Tokenizer("5+10")
#     assert tokenizer.get_tokens_as_string() == "5,+,10,<EOF>"


# def test_complex_expression():
#     """10. Complex: variable declaration"""
#     tokenizer = Tokenizer("auto x = 5 + 3 * 2;")
#     assert tokenizer.get_tokens_as_string() == "auto,x,=,5,+,3,*,2,;,<EOF>"


# ========== Keywords (16 tests) ==========
def test_keyword_auto():
    """1. Keyword: auto"""
    tokenizer = Tokenizer("auto")
    assert tokenizer.get_tokens_as_string() == "auto,<EOF>"


def test_keyword_break():
    """2. Keyword: break"""
    tokenizer = Tokenizer("break")
    assert tokenizer.get_tokens_as_string() == "break,<EOF>"


def test_keyword_case():
    """3. Keyword: case"""
    tokenizer = Tokenizer("case")
    assert tokenizer.get_tokens_as_string() == "case,<EOF>"


def test_keyword_continue():
    """4. Keyword: continue"""
    tokenizer = Tokenizer("continue")
    assert tokenizer.get_tokens_as_string() == "continue,<EOF>"


def test_keyword_default():
    """5. Keyword: default"""
    tokenizer = Tokenizer("default")
    assert tokenizer.get_tokens_as_string() == "default,<EOF>"


def test_keyword_else():
    """6. Keyword: else"""
    tokenizer = Tokenizer("else")
    assert tokenizer.get_tokens_as_string() == "else,<EOF>"


def test_keyword_float():
    """7. Keyword: float"""
    tokenizer = Tokenizer("float")
    assert tokenizer.get_tokens_as_string() == "float,<EOF>"


def test_keyword_for():
    """8. Keyword: for"""
    tokenizer = Tokenizer("for")
    assert tokenizer.get_tokens_as_string() == "for,<EOF>"


def test_keyword_if():
    """9. Keyword: if"""
    tokenizer = Tokenizer("if")
    assert tokenizer.get_tokens_as_string() == "if,<EOF>"


def test_keyword_int():
    """10. Keyword: int"""
    tokenizer = Tokenizer("int")
    assert tokenizer.get_tokens_as_string() == "int,<EOF>"


def test_keyword_return():
    """11. Keyword: return"""
    tokenizer = Tokenizer("return")
    assert tokenizer.get_tokens_as_string() == "return,<EOF>"


def test_keyword_string():
    """12. Keyword: string"""
    tokenizer = Tokenizer("string")
    assert tokenizer.get_tokens_as_string() == "string,<EOF>"


def test_keyword_struct():
    """13. Keyword: struct"""
    tokenizer = Tokenizer("struct")
    assert tokenizer.get_tokens_as_string() == "struct,<EOF>"


def test_keyword_switch():
    """14. Keyword: switch"""
    tokenizer = Tokenizer("switch")
    assert tokenizer.get_tokens_as_string() == "switch,<EOF>"


def test_keyword_void():
    """15. Keyword: void"""
    tokenizer = Tokenizer("void")
    assert tokenizer.get_tokens_as_string() == "void,<EOF>"


def test_keyword_while():
    """16. Keyword: while"""
    tokenizer = Tokenizer("while")
    assert tokenizer.get_tokens_as_string() == "while,<EOF>"


# ========== Operators (18 tests) ==========
def test_operator_plus():
    """17. Operator: +"""
    tokenizer = Tokenizer("+")
    assert tokenizer.get_tokens_as_string() == "+,<EOF>"


def test_operator_minus():
    """18. Operator: -"""
    tokenizer = Tokenizer("-")
    assert tokenizer.get_tokens_as_string() == "-,<EOF>"


def test_operator_star():
    """19. Operator: *"""
    tokenizer = Tokenizer("*")
    assert tokenizer.get_tokens_as_string() == "*,<EOF>"


def test_operator_slash():
    """20. Operator: /"""
    tokenizer = Tokenizer("/")
    assert tokenizer.get_tokens_as_string() == "/,<EOF>"


def test_operator_percent():
    """21. Operator: %"""
    tokenizer = Tokenizer("%")
    assert tokenizer.get_tokens_as_string() == "%,<EOF>"


def test_operator_eq():
    """22. Operator: =="""
    tokenizer = Tokenizer("==")
    assert tokenizer.get_tokens_as_string() == "==,<EOF>"


def test_operator_neq():
    """23. Operator: !="""
    tokenizer = Tokenizer("!=")
    assert tokenizer.get_tokens_as_string() == "!=,<EOF>"


def test_operator_lt():
    """24. Operator: <"""
    tokenizer = Tokenizer("<")
    assert tokenizer.get_tokens_as_string() == "<,<EOF>"


def test_operator_gt():
    """25. Operator: >"""
    tokenizer = Tokenizer(">")
    assert tokenizer.get_tokens_as_string() == ">,<EOF>"


def test_operator_le():
    """26. Operator: <="""
    tokenizer = Tokenizer("<=")
    assert tokenizer.get_tokens_as_string() == "<=,<EOF>"


def test_operator_ge():
    """27. Operator: >="""
    tokenizer = Tokenizer(">=")
    assert tokenizer.get_tokens_as_string() == ">=,<EOF>"


def test_operator_or():
    """28. Operator: ||"""
    tokenizer = Tokenizer("||")
    assert tokenizer.get_tokens_as_string() == "||,<EOF>"


def test_operator_and():
    """29. Operator: &&"""
    tokenizer = Tokenizer("&&")
    assert tokenizer.get_tokens_as_string() == "&&,<EOF>"


def test_operator_not():
    """30. Operator: !"""
    tokenizer = Tokenizer("!")
    assert tokenizer.get_tokens_as_string() == "!,<EOF>"


def test_operator_incr():
    """31. Operator: ++"""
    tokenizer = Tokenizer("++")
    assert tokenizer.get_tokens_as_string() == "++,<EOF>"


def test_operator_decr():
    """32. Operator: --"""
    tokenizer = Tokenizer("--")
    assert tokenizer.get_tokens_as_string() == "--,<EOF>"


def test_operator_assign():
    """33. Operator: ="""
    tokenizer = Tokenizer("=")
    assert tokenizer.get_tokens_as_string() == "=,<EOF>"


def test_operator_dot():
    """34. Operator: ."""
    tokenizer = Tokenizer(".")
    assert tokenizer.get_tokens_as_string() == ".,<EOF>"


# ========== Separators (7 tests) ==========
def test_separator_lbrace():
    """35. Separator: {"""
    tokenizer = Tokenizer("{")
    assert tokenizer.get_tokens_as_string() == "{,<EOF>"


def test_separator_rbrace():
    """36. Separator: }"""
    tokenizer = Tokenizer("}")
    assert tokenizer.get_tokens_as_string() == "},<EOF>"


def test_separator_lparen():
    """37. Separator: ("""
    tokenizer = Tokenizer("(")
    assert tokenizer.get_tokens_as_string() == "(,<EOF>"


def test_separator_rparen():
    """38. Separator: )"""
    tokenizer = Tokenizer(")")
    assert tokenizer.get_tokens_as_string() == "),<EOF>"


def test_separator_semi():
    """39. Separator: ;"""
    tokenizer = Tokenizer(";")
    assert tokenizer.get_tokens_as_string() == ";,<EOF>"


def test_separator_comma():
    """40. Separator: ,"""
    tokenizer = Tokenizer(",")
    assert tokenizer.get_tokens_as_string() == ",,<EOF>"


def test_separator_colon():
    """41. Separator: :"""
    tokenizer = Tokenizer(":")
    assert tokenizer.get_tokens_as_string() == ":,<EOF>"


# ========== Integer Literals (10 tests) ==========
def test_integer_zero():
    """42. Integer: zero"""
    tokenizer = Tokenizer("0")
    assert tokenizer.get_tokens_as_string() == "0,<EOF>"


def test_integer_single_digit():
    """43. Integer: single digit"""
    tokenizer = Tokenizer("5")
    assert tokenizer.get_tokens_as_string() == "5,<EOF>"


def test_integer_multi_digit():
    """44. Integer: multiple digits"""
    tokenizer = Tokenizer("12345")
    assert tokenizer.get_tokens_as_string() == "12345,<EOF>"


def test_integer_negative():
    """45. Integer: negative"""
    tokenizer = Tokenizer("-123")
    assert tokenizer.get_tokens_as_string() == "-,123,<EOF>"


def test_integer_large():
    """46. Integer: large number"""
    tokenizer = Tokenizer("2147483647")
    assert tokenizer.get_tokens_as_string() == "2147483647,<EOF>"


def test_integer_negative_zero():
    """47. Integer: negative zero"""
    tokenizer = Tokenizer("-0")
    assert tokenizer.get_tokens_as_string() == "-,0,<EOF>"


def test_integer_in_expression():
    """48. Integer: in expression"""
    tokenizer = Tokenizer("5+10-3")
    assert tokenizer.get_tokens_as_string() == "5,+,10,-,3,<EOF>"


def test_integer_with_spaces():
    """49. Integer: with spaces"""
    tokenizer = Tokenizer("  123  ")
    assert tokenizer.get_tokens_as_string() == "123,<EOF>"


def test_integer_multiple():
    """50. Integer: multiple integers"""
    tokenizer = Tokenizer("1 2 3 4 5")
    assert tokenizer.get_tokens_as_string() == "1,2,3,4,5,<EOF>"


def test_integer_leading_zeros():
    """51. Integer: with leading zeros"""
    tokenizer = Tokenizer("00123")
    assert tokenizer.get_tokens_as_string() == "00123,<EOF>"


# ========== Float Literals (12 tests) ==========
def test_float_simple_decimal():
    """52. Float: simple decimal"""
    tokenizer = Tokenizer("3.14")
    assert tokenizer.get_tokens_as_string() == "3.14,<EOF>"


def test_float_zero_decimal():
    """53. Float: zero decimal"""
    tokenizer = Tokenizer("0.0")
    assert tokenizer.get_tokens_as_string() == "0.0,<EOF>"


def test_float_no_integer_part():
    """54. Float: no integer part"""
    tokenizer = Tokenizer(".5")
    assert tokenizer.get_tokens_as_string() == ".5,<EOF>"


def test_float_no_decimal_part():
    """55. Float: no decimal part"""
    tokenizer = Tokenizer("5.")
    assert tokenizer.get_tokens_as_string() == "5.,<EOF>"


def test_float_with_exponent_positive():
    """56. Float: with positive exponent"""
    tokenizer = Tokenizer("1.23e4")
    assert tokenizer.get_tokens_as_string() == "1.23e4,<EOF>"


def test_float_with_exponent_negative():
    """57. Float: with negative exponent"""
    tokenizer = Tokenizer("5.67E-2")
    assert tokenizer.get_tokens_as_string() == "5.67E-2,<EOF>"


def test_float_exponent_only():
    """58. Float: exponent only (no decimal)"""
    tokenizer = Tokenizer("1e4")
    assert tokenizer.get_tokens_as_string() == "1e4,<EOF>"


def test_float_negative():
    """59. Float: negative"""
    tokenizer = Tokenizer("-3.14")
    assert tokenizer.get_tokens_as_string() == "-,3.14,<EOF>"


def test_float_negative_exponent():
    """60. Float: negative with exponent"""
    tokenizer = Tokenizer("-2E-3")
    assert tokenizer.get_tokens_as_string() == "-,2E-3,<EOF>"


def test_float_exponent_plus():
    """61. Float: exponent with explicit plus"""
    tokenizer = Tokenizer("1.5e+10")
    assert tokenizer.get_tokens_as_string() == "1.5e+10,<EOF>"


def test_float_multiple():
    """62. Float: multiple floats"""
    tokenizer = Tokenizer("1.0 2.5 3.14")
    assert tokenizer.get_tokens_as_string() == "1.0,2.5,3.14,<EOF>"


def test_float_in_expression():
    """63. Float: in expression"""
    tokenizer = Tokenizer("3.14*2.0+1.5")
    assert tokenizer.get_tokens_as_string() == "3.14,*,2.0,+,1.5,<EOF>"


# ========== String Literals (15 tests) ==========
def test_string_empty():
    """64. String: empty string"""
    tokenizer = Tokenizer('""')
    assert tokenizer.get_tokens_as_string() == ",<EOF>"


def test_string_simple():
    """65. String: simple string"""
    tokenizer = Tokenizer('"hello"')
    assert tokenizer.get_tokens_as_string() == "hello,<EOF>"


def test_string_with_spaces():
    """66. String: with spaces"""
    tokenizer = Tokenizer('"hello world"')
    assert tokenizer.get_tokens_as_string() == "hello world,<EOF>"


def test_string_escape_newline():
    """67. String: escape newline"""
    tokenizer = Tokenizer('"line1\\nline2"')
    assert tokenizer.get_tokens_as_string() == "line1\nline2,<EOF>"


def test_string_escape_tab():
    """68. String: escape tab"""
    tokenizer = Tokenizer('"col1\\tcol2"')
    assert tokenizer.get_tokens_as_string() == "col1\tcol2,<EOF>"


def test_string_escape_backslash():
    """69. String: escape backslash"""
    tokenizer = Tokenizer('"path\\\\file"')
    assert tokenizer.get_tokens_as_string() == "path\\file,<EOF>"


def test_string_escape_quote():
    """70. String: escape quote"""
    tokenizer = Tokenizer('"say \\"hello\\""')
    assert tokenizer.get_tokens_as_string() == 'say "hello",<EOF>'


def test_string_escape_backspace():
    """71. String: escape backspace"""
    tokenizer = Tokenizer('"text\\bmore"')
    assert tokenizer.get_tokens_as_string() == "text\bmore,<EOF>"


def test_string_escape_formfeed():
    """72. String: escape formfeed"""
    tokenizer = Tokenizer('"page1\\fpage2"')
    assert tokenizer.get_tokens_as_string() == "page1\fpage2,<EOF>"


def test_string_escape_carriage_return():
    """73. String: escape carriage return"""
    tokenizer = Tokenizer('"line\\rmore"')
    assert tokenizer.get_tokens_as_string() == "line\rmore,<EOF>"


def test_string_all_escapes():
    """74. String: all escape sequences"""
    tokenizer = Tokenizer('"\\b\\f\\r\\n\\t\\"\\\\"')
    assert tokenizer.get_tokens_as_string() == '\b\f\r\n\t"\\,<EOF>'


def test_string_multiple():
    """75. String: multiple strings"""
    tokenizer = Tokenizer('"hello" "world"')
    assert tokenizer.get_tokens_as_string() == "hello,world,<EOF>"


def test_string_with_numbers():
    """76. String: with numbers"""
    tokenizer = Tokenizer('"test123"')
    assert tokenizer.get_tokens_as_string() == "test123,<EOF>"


def test_string_with_special_chars():
    """77. String: with special characters"""
    tokenizer = Tokenizer('"!@#$%^&*()"')
    assert tokenizer.get_tokens_as_string() == "!@#$%^&*(),<EOF>"


def test_string_in_statement():
    """78. String: in print statement"""
    tokenizer = Tokenizer('printString("Hello");')
    assert tokenizer.get_tokens_as_string() == "printString,(,Hello,),;,<EOF>"


# ========== Identifiers (8 tests) ==========
def test_identifier_single_letter():
    """79. Identifier: single letter"""
    tokenizer = Tokenizer("x")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"


def test_identifier_multiple_letters():
    """80. Identifier: multiple letters"""
    tokenizer = Tokenizer("myVar")
    assert tokenizer.get_tokens_as_string() == "myVar,<EOF>"


def test_identifier_with_underscore():
    """81. Identifier: with underscore"""
    tokenizer = Tokenizer("_variable")
    assert tokenizer.get_tokens_as_string() == "_variable,<EOF>"


def test_identifier_with_numbers():
    """82. Identifier: with numbers"""
    tokenizer = Tokenizer("var123")
    assert tokenizer.get_tokens_as_string() == "var123,<EOF>"


def test_identifier_all_underscore():
    """83. Identifier: all underscores"""
    tokenizer = Tokenizer("___")
    assert tokenizer.get_tokens_as_string() == "___,<EOF>"


def test_identifier_long():
    """84. Identifier: long name"""
    tokenizer = Tokenizer("thisIsAVeryLongIdentifierName123")
    assert tokenizer.get_tokens_as_string() == "thisIsAVeryLongIdentifierName123,<EOF>"


def test_identifier_case_sensitive():
    """85. Identifier: case sensitive"""
    tokenizer = Tokenizer("MyVar myvar MYVAR")
    assert tokenizer.get_tokens_as_string() == "MyVar,myvar,MYVAR,<EOF>"


def test_identifier_vs_keyword():
    """86. Identifier: similar to keyword"""
    tokenizer = Tokenizer("integer floatValue strings")
    assert tokenizer.get_tokens_as_string() == "integer,floatValue,strings,<EOF>"


# ========== Comments (4 tests) ==========
def test_line_comment_simple():
    """87. Comment: line comment"""
    tokenizer = Tokenizer("// This is a comment")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_line_comment_after_code():
    """88. Comment: line comment after code"""
    tokenizer = Tokenizer("int x = 5; // assign value")
    assert tokenizer.get_tokens_as_string() == "int,x,=,5,;,<EOF>"


def test_block_comment_single_line():
    """89. Comment: block comment single line"""
    tokenizer = Tokenizer("/* comment */")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_block_comment_multiline():
    """90. Comment: block comment multiline"""
    tokenizer = Tokenizer("/* line1\nline2\nline3 */")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


# ========== Error Cases (10 tests) ==========
def test_error_unrecognized_char():
    """91. Error: unrecognized character"""
    tokenizer = Tokenizer("@")
    with pytest.raises(Exception):
        tokenizer.get_tokens_as_string()


def test_error_invalid_symbol():
    """92. Error: invalid symbol"""
    tokenizer = Tokenizer("#")
    with pytest.raises(Exception):
        tokenizer.get_tokens_as_string()


def test_error_unclosed_string():
    """93. Error: unclosed string"""
    tokenizer = Tokenizer('"hello')
    with pytest.raises(Exception):
        tokenizer.get_tokens_as_string()


def test_error_unclosed_string_newline():
    """94. Error: unclosed string with newline"""
    tokenizer = Tokenizer('"hello\n')
    with pytest.raises(Exception):
        tokenizer.get_tokens_as_string()


def test_error_illegal_escape():
    """95. Error: illegal escape sequence"""
    tokenizer = Tokenizer('"hello\\x"')
    with pytest.raises(Exception):
        tokenizer.get_tokens_as_string()


def test_error_illegal_escape_digit():
    """96. Error: illegal escape with digit"""
    tokenizer = Tokenizer('"text\\1"')
    with pytest.raises(Exception):
        tokenizer.get_tokens_as_string()


def test_error_illegal_escape_char():
    """97. Error: illegal escape with char"""
    tokenizer = Tokenizer('"test\\a"')
    with pytest.raises(Exception):
        tokenizer.get_tokens_as_string()


def test_error_backslash_at_end():
    """98. Error: backslash at string end"""
    tokenizer = Tokenizer('"text\\"')
    with pytest.raises(Exception):
        tokenizer.get_tokens_as_string()


def test_error_multiple_invalid_chars():
    """99. Error: multiple invalid characters"""
    tokenizer = Tokenizer("int x @ y #")
    with pytest.raises(Exception):
        tokenizer.get_tokens_as_string()


def test_error_unicode_char():
    """100. Error: unicode character (outside ASCII)"""
    tokenizer = Tokenizer("int x = 5; // α")
    # This should work as comment is skipped, but if unicode is in code:
    tokenizer2 = Tokenizer("α")
    with pytest.raises(Exception):
        tokenizer2.get_tokens_as_string()



