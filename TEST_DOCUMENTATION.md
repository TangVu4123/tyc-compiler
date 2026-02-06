# Test Cases Documentation

## Overview
This document describes the 200 comprehensive test cases (100 for lexer, 100 for parser) implemented for the TyC compiler project.

## Test Lexer (100 tests)

### Test Coverage Summary

#### 1. Keywords (16 tests) - Tests 1-16
Tests all 16 reserved keywords in TyC:
- `auto`, `break`, `case`, `continue`, `default`, `else`
- `float`, `for`, `if`, `int`, `return`, `string`
- `struct`, `switch`, `void`, `while`

**Boundary considerations:**
- Each keyword tested individually
- Ensures lexer properly recognizes reserved words
- Prevents keywords from being treated as identifiers

#### 2. Operators (18 tests) - Tests 17-34
Tests all operators with proper tokenization:
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical: `||`, `&&`, `!`
- Increment/Decrement: `++`, `--`
- Assignment: `=`
- Member access: `.`

**Boundary considerations:**
- Two-character operators (`==`, `!=`, `<=`, `>=`, `||`, `&&`, `++`, `--`)
- Ensures proper tokenization vs single character variants

#### 3. Separators (7 tests) - Tests 35-41
Tests all separator characters:
- Braces: `{`, `}`
- Parentheses: `(`, `)`
- Others: `;`, `,`, `:`

**Boundary considerations:**
- Proper pairing and recognition
- Critical for grammar structure

#### 4. Integer Literals (10 tests) - Tests 42-51
Comprehensive integer literal testing:
- Zero: `0`
- Single digit: `5`
- Multiple digits: `12345`
- Negative: `-123`
- Large numbers: `2147483647`
- Negative zero: `-0`
- In expressions: `5+10-3`
- With spaces: `  123  `
- Multiple integers: `1 2 3 4 5`
- Leading zeros: `00123` (treated as separate tokens)

**Boundary considerations:**
- Maximum integer values
- Negative numbers
- Zero edge case
- Leading zeros behavior

#### 5. Float Literals (12 tests) - Tests 52-63
Extensive float literal testing:
- Simple decimal: `3.14`
- Zero: `0.0`
- No integer part: `.5`
- No decimal part: `5.`
- With positive exponent: `1.23e4`
- With negative exponent: `5.67E-2`
- Exponent only: `1e4`
- Negative floats: `-3.14`
- Negative with exponent: `-2E-3`
- Explicit plus in exponent: `1.5e+10`
- Multiple floats: `1.0 2.5 3.14`
- In expressions: `3.14*2.0+1.5`

**Boundary considerations:**
- All valid float formats per specification
- Scientific notation variations
- Negative values
- Edge cases with decimal point placement

#### 6. String Literals (15 tests) - Tests 64-78
Comprehensive string testing:
- Empty string: `""`
- Simple string: `"hello"`
- With spaces: `"hello world"`
- All escape sequences:
  - Newline: `\n`
  - Tab: `\t`
  - Backslash: `\\`
  - Quote: `\"`
  - Backspace: `\b`
  - Formfeed: `\f`
  - Carriage return: `\r`
- All escapes together: `"\b\f\r\n\t\"\\"`
- Multiple strings
- With numbers: `"test123"`
- Special characters: `"!@#$%^&*()"`
- In statements: `printString("Hello");`

**Boundary considerations:**
- All valid escape sequences
- Empty strings
- Complex character combinations
- Proper quote handling

#### 7. Identifiers (8 tests) - Tests 79-86
Identifier recognition:
- Single letter: `x`
- Multiple letters: `myVar`
- With underscore: `_variable`
- With numbers: `var123`
- All underscores: `___`
- Long names: `thisIsAVeryLongIdentifierName123`
- Case sensitivity: `MyVar myvar MYVAR`
- vs keywords: `integer floatValue strings`

**Boundary considerations:**
- Starting characters (letter or underscore)
- Length limits
- Case sensitivity
- Distinction from keywords

#### 8. Comments (4 tests) - Tests 87-90
Comment handling:
- Line comment: `// This is a comment`
- Line comment after code: `int x = 5; // assign value`
- Block comment single line: `/* comment */`
- Block comment multiline: `/* line1\nline2\nline3 */`

**Boundary considerations:**
- Comment removal from token stream
- Line vs block comments
- Comments mixed with code

#### 9. Error Cases (10 tests) - Tests 91-100
Comprehensive error detection:
- **ERROR_CHAR**: Unrecognized characters
  - `@` - special character
  - `#` - hash symbol
  - Unicode characters outside ASCII
- **UNCLOSE_STRING**: Unterminated strings
  - Missing closing quote: `"hello`
  - With newline: `"hello\n`
  - Backslash at end: `"text\`
- **ILLEGAL_ESCAPE**: Invalid escape sequences
  - Invalid char: `"hello\x"`
  - Digit: `"text\1"`
  - Letter: `"test\a"`
- Multiple errors in sequence

**Boundary considerations:**
- All three error types tested
- Proper exception raising
- Error message format compliance
- Edge cases in error detection

### Lexer Test Strategy

**Coverage:**
- ✓ All 16 keywords
- ✓ All 18 operators
- ✓ All 7 separators
- ✓ Integer literals (positive, negative, zero, boundary)
- ✓ Float literals (all formats, scientific notation)
- ✓ String literals (empty, with escapes, special chars)
- ✓ Identifiers (various valid formats)
- ✓ Comments (line and block)
- ✓ All 3 error types (ERROR_CHAR, UNCLOSE_STRING, ILLEGAL_ESCAPE)

**Test Design Principles:**
- Boundary value analysis
- Error handling verification
- Format variations
- Edge cases and special cases
- Real-world usage patterns

---

## Test Parser (100 tests)

### Test Coverage Summary

#### 1. Program Structure (5 tests) - Tests 1-5
Program-level testing:
- Empty program
- Main function only
- Struct then function
- Multiple structs and functions
- Multiple functions

**Boundary considerations:**
- Minimum valid program (empty)
- Required main function
- Order of declarations
- Multiple declaration types

#### 2. Struct Declarations (10 tests) - Tests 6-15
Comprehensive struct testing:
- **Valid cases:**
  - Simple struct with one member
  - Multiple members
  - Different member types (int, float, string)
  - Nested struct types (member is another struct)
  - Many members (5+ fields)
  
- **Error cases:**
  - void member (invalid)
  - auto member (invalid)
  - No members (invalid)
  - Missing semicolons

**Boundary considerations:**
- Member count (1 to many)
- Type variety
- Nested type references
- Syntax errors

#### 3. Function Declarations (15 tests) - Tests 16-30
Extensive function testing:
- **Return types:**
  - void, int, float, string, struct types
  - Inferred return type (omitted)
  
- **Parameters:**
  - No parameters
  - Single parameter
  - Multiple parameters (3+)
  - Mixed parameter types
  - Struct parameters
  
- **Error cases:**
  - auto parameter (invalid)
  - Missing parameter type
  - Missing braces
  
- **Function bodies:**
  - Empty body
  - Complex recursive body

**Boundary considerations:**
- All valid return types
- Parameter count variations
- Type inference support
- Syntax error detection

#### 4. Variable Declarations (10 tests) - Tests 31-40
Variable declaration variations:
- **auto type:**
  - With initialization
  - Without initialization
  
- **Explicit types:**
  - int, float, string
  - With/without initialization
  - Struct types
  
- **Initialization:**
  - Literal values
  - Expressions
  - Struct initialization `{1, 2}`
  - Complex expressions

**Boundary considerations:**
- Type inference with auto
- All valid types
- Initialization patterns
- Expression complexity

#### 5. If Statements (5 tests) - Tests 41-45
Conditional statement testing:
- Simple if
- If-else
- With blocks
- Nested if statements
- Else-if chains

**Boundary considerations:**
- Single vs block statements
- Nesting depth
- Complex conditionals

#### 6. While Statements (3 tests) - Tests 46-48
Loop testing:
- Simple while
- With block
- Nested while loops

**Boundary considerations:**
- Nesting depth
- Loop body complexity

#### 7. For Statements (6 tests) - Tests 49-54
For loop variations:
- Standard for loop
- With block
- Empty initialization
- Empty condition (infinite loop)
- Empty update
- All parts empty `for(;;)`

**Boundary considerations:**
- Optional clause testing
- Infinite loop handling
- Various initialization types

#### 8. Switch Statements (5 tests) - Tests 55-59
Switch-case testing:
- Simple switch with one case
- Multiple cases
- With default clause
- Fall-through (no break)
- Empty switch

**Boundary considerations:**
- Case count
- Default clause placement
- Fall-through behavior

#### 9. Break and Continue (4 tests) - Tests 60-63
Control flow alteration:
- Break in while
- Continue in while
- Break in for
- Continue in for

**Boundary considerations:**
- Context-appropriate usage
- Within different loop types

#### 10. Return Statements (4 tests) - Tests 64-67
Return variations:
- Void return (no value)
- Integer return
- Expression return
- Function call return

**Boundary considerations:**
- With/without value
- Expression complexity
- Nested function calls

#### 11. Expression Precedence & Associativity (15 tests) - Tests 68-82
Comprehensive expression testing:
- **Assignment:** Right associative `x = y = z = 0`
- **Logical OR:** `x || y || z`
- **Logical AND:** `x && y && z`
- **Equality:** `x == y != z`
- **Relational:** `x < y <= z > w >= u`
- **Additive:** `x + y - z + w`
- **Multiplicative:** `x * y / z % w`
- **Precedence:** `x + y * z` (mul before add)
- **Complex precedence:** `a + b * c - d / e % f`
- **Unary:** `-x + !y`
- **Prefix:** `++x; --y;`
- **Postfix:** `x++; y--;`
- **Parentheses:** `(x + y) * (z - w)`
- **Member access:** `p.x + p.y`

**Boundary considerations:**
- All precedence levels (10 levels)
- Associativity (left vs right)
- Operator combinations
- Grouping with parentheses
- Member access chaining

#### 12. Function Calls (4 tests) - Tests 83-86
Function call patterns:
- No arguments
- Single argument
- Multiple arguments
- Nested function calls

**Boundary considerations:**
- Argument count (0 to many)
- Nesting depth
- Expression arguments

#### 13. Block Statements (3 tests) - Tests 87-89
Block structure:
- Empty blocks
- Nested blocks (depth 3)
- Multiple statements in block

**Boundary considerations:**
- Nesting depth
- Statement count
- Scope implications

#### 14. Complex and Nested Structures (6 tests) - Tests 90-95
Integration testing:
- **Nested control flow:** for + if + while + switch combined
- **Complex expressions in control:** compound conditions
- **Struct operations:** member access and assignment
- **Multiple function interactions:** functions calling functions
- **All operators:** comprehensive operator usage
- **Realistic program:** Point distance calculator

**Boundary considerations:**
- Nesting depth (4+ levels)
- Feature integration
- Real-world patterns
- Maximum complexity

#### 15. Error Cases (5 tests) - Tests 96-100
Syntax error detection:
- Missing semicolon
- Unbalanced braces
- Unbalanced parentheses
- Invalid expression syntax
- Statement outside function

**Boundary considerations:**
- Common syntax errors
- Error recovery capability
- Proper error reporting

### Parser Test Strategy

**Coverage:**
- ✓ All statement types (7 types)
- ✓ All expression operators (18 operators)
- ✓ All precedence levels (10 levels)
- ✓ All data types (int, float, string, void, struct, auto)
- ✓ Function declarations (6+ variations)
- ✓ Struct declarations (5+ variations)
- ✓ Variable declarations (8+ variations)
- ✓ Nested structures (depth 4+)
- ✓ Error detection (5 common errors)

**Test Design Principles:**
- Grammar rule coverage (100%)
- Precedence and associativity verification
- Nesting depth testing (boundary)
- Error recovery testing
- Integration testing (multiple features)
- Real-world program patterns

---

## Test Execution

### Running Tests

```bash
# Run all lexer tests
python3 run.py test-lexer

# Run all parser tests
python3 run.py test-parser

# Run with pytest directly
pytest tests/test_lexer.py -v
pytest tests/test_parser.py -v
```

### Expected Results

- **Lexer:** 100/100 tests passing
  - 90 successful token recognition tests
  - 10 error detection tests (with exceptions)

- **Parser:** 100/100 tests passing
  - 95 successful parse tests
  - 5 error detection tests (expecting parse errors)

---

## Quality Metrics

### Lexer Test Quality
- **Keyword Coverage:** 100% (16/16)
- **Operator Coverage:** 100% (18/18)
- **Separator Coverage:** 100% (7/7)
- **Literal Types:** 100% (integer, float, string)
- **Error Types:** 100% (3/3 error types)
- **Edge Cases:** Comprehensive (20+ boundary tests)

### Parser Test Quality
- **Statement Coverage:** 100% (all statement types)
- **Expression Coverage:** 100% (all operators)
- **Declaration Coverage:** 100% (structs, functions, variables)
- **Precedence Coverage:** 100% (10 precedence levels)
- **Nesting Depth:** 4+ levels tested
- **Error Detection:** 5 common syntax errors

---

## Maintenance Notes

### Adding New Tests
1. Follow the numbering convention (test_xxx with number in docstring)
2. Group similar tests together
3. Include clear docstrings
4. Test both valid and invalid cases
5. Consider boundary conditions

### Updating Tests
When grammar changes:
1. Update affected parser tests
2. Update token tests if lexer changes
3. Verify error message formats
4. Check precedence/associativity if operators change
5. Re-run full test suite

---

## Test Statistics

### Lexer Tests Distribution
- Keywords: 16 tests (16%)
- Operators: 18 tests (18%)
- Separators: 7 tests (7%)
- Integer Literals: 10 tests (10%)
- Float Literals: 12 tests (12%)
- String Literals: 15 tests (15%)
- Identifiers: 8 tests (8%)
- Comments: 4 tests (4%)
- Error Cases: 10 tests (10%)

### Parser Tests Distribution
- Program Structure: 5 tests (5%)
- Structs: 10 tests (10%)
- Functions: 15 tests (15%)
- Variables: 10 tests (10%)
- Control Flow: 23 tests (23%)
  - If: 5, While: 3, For: 6, Switch: 5, Break/Continue: 4
- Return: 4 tests (4%)
- Expressions: 15 tests (15%)
- Function Calls: 4 tests (4%)
- Blocks: 3 tests (3%)
- Complex: 6 tests (6%)
- Errors: 5 tests (5%)

---

**Total Test Count: 200 tests**
- Lexer: 100 tests
- Parser: 100 tests

**Quality Level: Comprehensive**
- All language features covered
- Boundary conditions tested
- Error handling verified
- Real-world patterns included
