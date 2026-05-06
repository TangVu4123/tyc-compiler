
from tests.utils import Checker


# =============================================================================
# VALID PROGRAMS – test_001 đến test_015
# =============================================================================

def test_001():
    """Valid: khai báo và dùng biến int cơ bản."""
    source = """
void main() {
    int x = 5;
    int y = x + 1;
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_002():
    """Valid: auto inference từ literal."""
    source = """
void main() {
    auto x = 10;
    auto y = 3.14;
    auto z = x + y;
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_003():
    """Valid: hàm khai báo TRƯỚC main rồi được gọi."""
    source = """
int add(int x, int y) {
    return x + y;
}
void main() {
    int sum = add(5, 3);
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_004():
    """Valid: struct khai báo trước, dùng member access."""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p;
    p.x = 10;
    p.y = 20;
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_005():
    """Valid: block lồng nhau, biến outer visible trong inner."""
    source = """
void main() {
    int x = 10;
    {
        int y = 20;
        int z = x + y;
    }
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_006():
    """Valid: shadow biến local (không phải param) qua nhiều cấp block."""
    source = """
void main() {
    int x = 10;
    {
        int x = 20;
        {
            int x = 30;
        }
    }
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_007():
    """Valid: struct lồng struct (struct con khai báo trước)."""
    source = """
struct Point { int x; int y; };
struct Rect { Point p1; Point p2; };
void main() {
    Rect r;
    r.p1.x = 0;
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_008():
    """Valid: gọi built-in functions readInt và printInt."""
    source = """
void main() {
    int x = readInt();
    printInt(x);
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_009():
    """Valid: for loop với break và continue."""
    source = """
void main() {
    for (int i = 0; i < 10; ++i) {
        if (i == 5) break;
        if (i == 2) continue;
    }
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_010():
    """Valid: while loop với break và continue."""
    source = """
void main() {
    int i = 0;
    while (i < 10) {
        if (i == 5) break;
        if (i == 2) continue;
        ++i;
    }
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_011():
    """Valid: switch statement với case và break."""
    source = """
void main() {
    int x = 2;
    switch(x) {
        case 1: x = 10; break;
        case 2: x = 20; break;
    }
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_012():
    """Valid: auto inference từ hàm return value và từ expression."""
    source = """
int getVal() { return 42; }
void main() {
    auto a = getVal();
    auto b;
    b = a + 5;
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_013():
    """Valid: relational và logical operators với int và float."""
    source = """
void main() {
    int a = 5;
    float b = 6.0;
    int c = a < b;
    int d = c && (a == 5);
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_014():
    """Valid: assignment expression trong initializer và chained assignment."""
    source = """
void main() {
    int x;
    int y = (x = 5) + 3;
    int a; int b; int c;
    a = b = c = 10;
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


def test_015():
    """Valid: struct literal và struct assignment."""
    source = """
struct Point { int x; int y; };
void main() {
    Point p1 = {10, 20};
    Point p2;
    p2 = p1;
}
"""
    assert "Static checking passed" in Checker(source).check_from_source()


# =============================================================================
# REDECLARED – test_016 đến test_025
# =============================================================================

def test_016():
    """Redeclared(Struct, Point): khai báo struct cùng tên hai lần."""
    source = """
struct Point { int x; };
struct Point { int y; };
void main() {}
"""
    assert "Redeclared(Struct, Point)" in Checker(source).check_from_source()


def test_017():
    """Redeclared(Function, add): khai báo hàm cùng tên hai lần."""
    source = """
int add() { return 1; }
int add(int x) { return x; }
void main() {}
"""
    assert "Redeclared(Function, add)" in Checker(source).check_from_source()


def test_018():
    """Redeclared(Variable, x): biến khai báo lại trong cùng block."""
    source = """
void main() {
    int x = 5;
    int x = 10;
}
"""
    assert "Redeclared(Variable, x)" in Checker(source).check_from_source()


def test_019():
    """Redeclared(Parameter, x): tham số trùng tên trong danh sách param."""
    source = """
int calculate(int x, int x) {
    return x;
}
void main() {}
"""
    assert "Redeclared(Parameter, x)" in Checker(source).check_from_source()


def test_020():
    """Redeclared(Variable, x): biến local trùng tên param ngay trong body."""
    source = """
void func(int x) {
    int x = 10;
}
void main() {}
"""
    assert "Redeclared(Variable, x)" in Checker(source).check_from_source()


def test_021():
    """Redeclared(Member, x): tên member trùng nhau trong cùng struct."""
    source = """
struct Point {
    int x;
    int x;
};
void main() {}
"""
    assert "Redeclared(Member, x)" in Checker(source).check_from_source()


def test_022():
    """Redeclared(Variable, a): khai báo lại biến với kiểu khác."""
    source = """
void main() {
    int a = 1;
    float b = 2.0;
    string a = "test";
}
"""
    assert "Redeclared(Variable, a)" in Checker(source).check_from_source()


def test_023():
    """Redeclared(Variable, p): biến local trùng tên param trong block lồng."""
    source = """
void func(int p) {
    {
        int p = 5;
    }
}
void main() {}
"""
    assert "Redeclared(Variable, p)" in Checker(source).check_from_source()


def test_024():
    """Redeclared(Member, val): member trùng với kiểu khác."""
    source = """
struct Test {
    int val;
    float val;
};
void main() {}
"""
    assert "Redeclared(Member, val)" in Checker(source).check_from_source()


def test_025():
    """Redeclared(Parameter, a): tham số trùng tên với kiểu khác."""
    source = """
void test(int a, float a) {}
void main() {}
"""
    assert "Redeclared(Parameter, a)" in Checker(source).check_from_source()


# =============================================================================
# UNDECLARED IDENTIFIER – test_026 đến test_035
# =============================================================================

def test_026():
    """UndeclaredIdentifier(y): dùng biến chưa khai báo."""
    source = """
void main() {
    int x = y + 1;
}
"""
    assert "UndeclaredIdentifier(y)" in Checker(source).check_from_source()


def test_027():
    """UndeclaredIdentifier(x): gán cho biến chưa khai báo."""
    source = """
void main() {
    x = 5;
    int x;
}
"""
    assert "UndeclaredIdentifier(x)" in Checker(source).check_from_source()


def test_028():
    """UndeclaredIdentifier(x): truy cập biến đã ra khỏi scope."""
    source = """
void main() {
    { int x = 5; }
    int y = x;
}
"""
    assert "UndeclaredIdentifier(x)" in Checker(source).check_from_source()


def test_029():
    """UndeclaredIdentifier(x): biến dùng trong chính initializer của nó."""
    source = """
void main() {
    int x = x + 1;
}
"""
    assert "UndeclaredIdentifier(x)" in Checker(source).check_from_source()


def test_030():
    """UndeclaredIdentifier(z): biến chưa khai báo trong expression phức tạp."""
    source = """
void main() {
    int x = 5 + z * 2;
}
"""
    assert "UndeclaredIdentifier(z)" in Checker(source).check_from_source()


def test_031():
    """UndeclaredIdentifier(undeclared): biến chưa khai báo trong function call."""
    source = """
void foo(int a) {}
void main() {
    foo(undeclared);
}
"""
    assert "UndeclaredIdentifier(undeclared)" in Checker(source).check_from_source()


def test_032():
    """UndeclaredIdentifier(cond): biến chưa khai báo dùng làm condition."""
    source = """
void main() {
    if (cond) {}
}
"""
    assert "UndeclaredIdentifier(cond)" in Checker(source).check_from_source()


def test_033():
    """UndeclaredIdentifier(retVal): biến chưa khai báo trong return."""
    source = """
int foo() {
    return retVal;
}
void main() {}
"""
    assert "UndeclaredIdentifier(retVal)" in Checker(source).check_from_source()


def test_034():
    """UndeclaredIdentifier(a): biến local của hàm khác không visible."""
    source = """
void func1() { int a = 1; }
void func2() { int b = a; }
void main() {}
"""
    assert "UndeclaredIdentifier(a)" in Checker(source).check_from_source()


def test_035():
    """UndeclaredIdentifier(p): param của hàm khác không visible."""
    source = """
void func1(int p) {}
void func2() { int x = p; }
void main() {}
"""
    assert "UndeclaredIdentifier(p)" in Checker(source).check_from_source()


# =============================================================================
# UNDECLARED FUNCTION – test_036 đến test_045
# =============================================================================

def test_036():
    """UndeclaredFunction(foo): gọi hàm hoàn toàn chưa khai báo."""
    source = """
void main() {
    foo();
}
"""
    assert "UndeclaredFunction(foo)" in Checker(source).check_from_source()


def test_037():
    """UndeclaredFunction(bar): gọi hàm khai báo SAU (single-pass: không cho forward ref)."""
    source = """
void main() {
    bar();
}
void bar() {}
"""
    assert "UndeclaredFunction(bar)" in Checker(source).check_from_source()


def test_038():
    """UndeclaredFunction(getVal): gọi hàm chưa khai báo trong assignment."""
    source = """
void main() {
    int x = getVal();
}
"""
    assert "UndeclaredFunction(getVal)" in Checker(source).check_from_source()


def test_039():
    """UndeclaredFunction(calc): gọi hàm chưa khai báo trong expression."""
    source = """
void main() {
    int x = 5 + calc(2);
}
"""
    assert "UndeclaredFunction(calc)" in Checker(source).check_from_source()


def test_040():
    """UndeclaredFunction(process): gọi hàm chưa khai báo với nhiều argument."""
    source = """
void main() {
    process(1, 2.0, "3");
}
"""
    assert "UndeclaredFunction(process)" in Checker(source).check_from_source()


def test_041():
    """UndeclaredFunction(getMissing): gọi hàm chưa khai báo trong return."""
    source = """
int foo() {
    return getMissing();
}
void main() {}
"""
    assert "UndeclaredFunction(getMissing)" in Checker(source).check_from_source()


def test_042():
    """UndeclaredFunction(check): gọi hàm chưa khai báo trong condition."""
    source = """
void main() {
    if (check()) {}
}
"""
    assert "UndeclaredFunction(check)" in Checker(source).check_from_source()


def test_043():
    """UndeclaredFunction(missing): gọi hàm chưa khai báo trong nested call."""
    source = """
void main() {
    printInt(missing());
}
"""
    assert "UndeclaredFunction(missing)" in Checker(source).check_from_source()


def test_044():
    """UndeclaredFunction(x): gọi biến như một hàm."""
    source = """
void main() {
    int x = 5;
    x();
}
"""
    assert "UndeclaredFunction(x)" in Checker(source).check_from_source()


def test_045():
    """UndeclaredFunction(p): gọi tham số như một hàm."""
    source = """
void test(int p) {
    p();
}
void main() {}
"""
    assert "UndeclaredFunction(p)" in Checker(source).check_from_source()


# =============================================================================
# UNDECLARED STRUCT – test_046 đến test_055
# =============================================================================

def test_046():
    """UndeclaredStruct(Point): dùng struct hoàn toàn chưa khai báo."""
    source = """
void main() {
    Point p;
}
"""
    assert "UndeclaredStruct(Point)" in Checker(source).check_from_source()


def test_047():
    """UndeclaredStruct(Data): dùng struct khai báo SAU (single-pass: không cho forward ref)."""
    source = """
void test() {
    Data d;
}
struct Data { int x; };
void main() {}
"""
    assert "UndeclaredStruct(Data)" in Checker(source).check_from_source()


def test_048():
    """UndeclaredStruct(Missing): struct member dùng struct chưa khai báo."""
    source = """
struct Node {
    Missing m;
};
void main() {}
"""
    assert "UndeclaredStruct(Missing)" in Checker(source).check_from_source()


def test_049():
    """UndeclaredStruct(Unknown): struct chưa khai báo dùng làm kiểu param."""
    source = """
void process(Unknown u) {}
void main() {}
"""
    assert "UndeclaredStruct(Unknown)" in Checker(source).check_from_source()


def test_050():
    """UndeclaredStruct(Result): struct chưa khai báo dùng làm return type."""
    source = """
Result getRes() {}
void main() {}
"""
    assert "UndeclaredStruct(Result)" in Checker(source).check_from_source()


def test_051():
    """UndeclaredStruct(BadStruct): struct chưa khai báo trong local variable."""
    source = """
void main() {
    int x;
    BadStruct b;
}
"""
    assert "UndeclaredStruct(BadStruct)" in Checker(source).check_from_source()


def test_052():
    """UndeclaredStruct(B): struct member dùng struct B chưa khai báo."""
    source = """
struct A { B b; };
void main() {}
"""
    assert "UndeclaredStruct(B)" in Checker(source).check_from_source()


def test_053():
    """UndeclaredStruct(Data): struct chưa khai báo dùng trong param function."""
    source = """
void doWork(Data d) {}
void main() {}
"""
    assert "UndeclaredStruct(Data)" in Checker(source).check_from_source()


def test_054():
    """UndeclaredStruct(Missing): struct chưa khai báo trong VarDecl với init."""
    source = """
void main() {
    Missing m = {1, 2};
}
"""
    assert "UndeclaredStruct(Missing)" in Checker(source).check_from_source()


def test_055():
    """UndeclaredStruct(InnerStruct): struct chưa khai báo trong block lồng."""
    source = """
void main() {
    {
        InnerStruct s;
    }
}
"""
    assert "UndeclaredStruct(InnerStruct)" in Checker(source).check_from_source()


# =============================================================================
# TYPE CANNOT BE INFERRED – test_056 đến test_065
# =============================================================================

def test_056():
    """TypeCannotBeInferred: auto x và y đều unknown, dùng x + y."""
    source = """
void main() {
    auto x;
    auto y;
    auto z = x + y;
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_057():
    """TypeCannotBeInferred: auto x; không bao giờ được dùng."""
    source = """
void main() {
    auto x;
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_058():
    """TypeCannotBeInferred: auto a = b; khi b cũng là auto unknown."""
    source = """
void main() {
    auto a;
    auto b;
    a = b;
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_059():
    """TypeCannotBeInferred: cả hai auto unknown trong relational operator."""
    source = """
void main() {
    auto x;
    auto y;
    int z = x < y;
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_060():
    """TypeCannotBeInferred: auto x unknown + string literal không thể infer."""
    source = """
void main() {
    auto x;
    auto y = x + "hello";
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_061():
    """TypeCannotBeInferred: return auto chưa giải được."""
    source = """
func() {
    auto x;
    return x;
}
void main() {}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_062():
    """TypeCannotBeInferred: cả hai auto unknown trong phép nhân."""
    source = """
void main() {
    auto a;
    auto b;
    int c = a * b;
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_063():
    """TypeCannotBeInferred: auto a = a; – tự tham chiếu."""
    source = """
void main() {
    auto a;
    a = a;
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_064():
    """TypeCannotBeInferred: auto val; trong block lồng, không bao giờ dùng."""
    source = """
void main() {
    {
        auto val;
    }
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_065():
    """TypeCannotBeInferred: cả hai auto unknown dùng trong float initializer."""
    source = """
void main() {
    auto x;
    auto y;
    float f = x + y;
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


# =============================================================================
# TYPE MISMATCH IN STATEMENT – test_066 đến test_078
# =============================================================================

def test_066():
    """TypeMismatchInStatement: if condition là float literal."""
    source = """
void main() {
    if (3.14) {}
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_067():
    """TypeMismatchInStatement: if condition là string literal."""
    source = """
void main() {
    if ("true") {}
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_068():
    """TypeMismatchInStatement: if condition là struct variable."""
    source = """
struct S { int x; };
void main() {
    S s;
    if (s) {}
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_069():
    """TypeMismatchInStatement: while condition là string literal."""
    source = """
void main() {
    while ("loop") {}
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_070():
    """TypeMismatchInStatement: for condition là float literal."""
    source = """
void main() {
    for (int i = 0; 1.5; ++i) {}
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_071():
    """TypeMismatchInStatement: gán float vào int (statement-level assignment)."""
    source = """
void main() {
    int x;
    x = 3.14;
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_072():
    """TypeMismatchInStatement: gán struct B vào struct A (statement-level)."""
    source = """
struct A { int x; };
struct B { int x; };
void main() {
    A a; B b;
    a = b;
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_073():
    """TypeMismatchInStatement: return string từ int function."""
    source = """
int foo() {
    return "text";
}
void main() {}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_074():
    """TypeMismatchInStatement: return; (empty) từ int function."""
    source = """
int foo() {
    return;
}
void main() {}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_075():
    """TypeMismatchInStatement: return int từ void function."""
    source = """
void main() {
    return 1;
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_076():
    """TypeMismatchInStatement: switch expression là float."""
    source = """
void main() {
    switch (3.14) { case 1: break; }
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_077():
    """TypeMismatchInStatement: switch expression là string."""
    source = """
void main() {
    switch ("str") { case 1: break; }
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_078():
    """TypeMismatchInStatement: switch expression là struct."""
    source = """
struct S { int x; };
void main() {
    S s;
    switch (s) { case 1: break; }
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


# =============================================================================
# TYPE MISMATCH IN EXPRESSION – test_079 đến test_093
# =============================================================================

def test_079():
    """TypeMismatchInExpression: int + string."""
    source = """
void main() {
    int x = 5 + "text";
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_080():
    """TypeMismatchInExpression: int + struct."""
    source = """
struct S { int x; };
void main() {
    S s;
    int x = 5 + s;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_081():
    """TypeMismatchInExpression: float % int (modulus chỉ dùng int)."""
    source = """
void main() {
    int x = 5.5 % 2;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_082():
    """TypeMismatchInExpression: float < string (relational cần numeric)."""
    source = """
void main() {
    int b = 1.0 < "1";
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_083():
    """TypeMismatchInExpression: struct == struct (equality không áp dụng cho struct)."""
    source = """
struct S { int x; };
void main() {
    S s1; S s2;
    int b = s1 == s2;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_084():
    """TypeMismatchInExpression: float && int (logical cần int)."""
    source = """
void main() {
    int b = 1.5 && 1;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_085():
    """TypeMismatchInExpression: !float (logical NOT cần int)."""
    source = """
void main() {
    int b = !1.5;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_086():
    """TypeMismatchInExpression: prefix ++ trên float."""
    source = """
void main() {
    float f = 1.0;
    ++f;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_087():
    """TypeMismatchInExpression: prefix ++ trên literal (không phải lvalue)."""
    source = """
void main() {
    ++5;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_088():
    """TypeMismatchInExpression: postfix ++ trên expression (không phải lvalue)."""
    source = """
void main() {
    int x = 1;
    (x + 1)++;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_089():
    """TypeMismatchInExpression: member access trên int (không phải struct)."""
    source = """
void main() {
    int x = 1;
    int y = x.mem;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_090():
    """TypeMismatchInExpression: member không tồn tại trong struct."""
    source = """
struct S { int x; };
void main() {
    S s;
    int y = s.y;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_091():
    """TypeMismatchInExpression: sai kiểu argument khi gọi hàm."""
    source = """
void foo(int a) {}
void main() {
    foo("123");
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_092():
    """TypeMismatchInExpression: sai số lượng argument khi gọi hàm."""
    source = """
void foo(int a) {}
void main() {
    foo(1, 2);
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_093():
    """TypeMismatchInExpression: LHS của assignment là literal (không phải lvalue)."""
    source = """
void main() {
    int x = (5 = 2) + 1;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


# =============================================================================
# MUST IN LOOP – test_094 đến test_100
# =============================================================================

def test_094():
    """MustInLoop: break ngoài loop và switch."""
    source = """
void main() {
    break;
}
"""
    assert "MustInLoop" in Checker(source).check_from_source()


def test_095():
    """MustInLoop: continue ngoài loop."""
    source = """
void main() {
    continue;
}
"""
    assert "MustInLoop" in Checker(source).check_from_source()


def test_096():
    """MustInLoop: break trong if (không có loop bao quanh)."""
    source = """
void main() {
    if (1) { break; }
}
"""
    assert "MustInLoop" in Checker(source).check_from_source()


def test_097():
    """MustInLoop: continue trong if (không có loop bao quanh)."""
    source = """
void main() {
    if (1) { continue; }
}
"""
    assert "MustInLoop" in Checker(source).check_from_source()


def test_098():
    """MustInLoop: continue trong switch (switch không phải loop)."""
    source = """
void main() {
    int x = 1;
    switch(x) {
        case 1: continue;
    }
}
"""
    assert "MustInLoop" in Checker(source).check_from_source()


def test_099():
    """MustInLoop: break trong hàm helper được gọi từ loop – loop context không truyền qua call."""
    source = """
void helper() { break; }
void main() {
    while(1) { helper(); }
}
"""
    assert "MustInLoop" in Checker(source).check_from_source()


def test_100():
    """MustInLoop: continue trong hàm helper được gọi từ for loop."""
    source = """
void helper() { continue; }
void main() {
    for(int i=0; i<1; ++i) { helper(); }
}
"""
    assert "MustInLoop" in Checker(source).check_from_source()


