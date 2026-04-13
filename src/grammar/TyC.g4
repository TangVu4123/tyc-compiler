grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.STRING_LIT:
        # Get the original text (e.g., '"hello"')
        original_text = self.text
        # Strip the first and last characters (the quotes)
        self.text = original_text[1:-1]
        return super().emit()
        
    elif tk == self.UNCLOSE_STRING:       
        result = super().emit()
        # Lexeme does not include opening quote 
        raise UncloseString(result.text[1:])
        
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit()
        # Wrong string is from beginning without opening quote 
        raise IllegalEscape(result.text[1:])
        
    elif tk == self.ERROR_CHAR:
        result = super().emit()
        raise ErrorToken(result.text)
        
    else:
        return super().emit()
}

options {
    language = Python3;
}

// --- PARSER RULES ---

// Comments & WS 
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;

program: (funcDecl| structDecl)* EOF; 

// Declarations
structDecl: STRUCT ID LB structMember* RB SEMI; 
structMember: type ID SEMI; 

funcDecl: (type | VOID)? ID LP paramList? RP block; 

paramList: param (COMMA param)*; 
param: type ID; 

// Statements
statement: varDecl 
         | block 
         | ifStmt 
         | whileStmt 
         | forStmt 
         | switchStmt 
         | breakStmt 
         | continueStmt 
         | returnStmt 
         | exprStmt; 

varDecl: (AUTO | type) ID (ASSIGN expr)? SEMI; 

block: LB (varDecl | statement)* RB; 

ifStmt: IF LP expr RP statement (ELSE statement)?; 

whileStmt: WHILE LP expr RP statement; 

forStmt: FOR LP (varDecl | exprStmt | SEMI) (expr? SEMI) expr? RP statement; 

switchStmt: SWITCH LP expr RP LB (caseStmt | defaultStmt)* RB; 
caseStmt: CASE expr COLON (varDecl | statement)*; 
defaultStmt: DEFAULT COLON (varDecl | statement)*; 

breakStmt: BREAK SEMI; 
continueStmt: CONTINUE SEMI; 
returnStmt: RETURN expr? SEMI; 
exprStmt: expr SEMI; 

// Types
type: INT | FLOAT | STRING | ID; 

// Expressions (Precedence: Highest to Lowest) 
expr: primary                                   #primaryExpr
    | expr DOT ID                               #memberAccess
    | expr (INC | DEC | LP argList? RP) #postfixExpr
    | (NOT | SUB | ADD | INC | DEC) expr        #unaryExpr
    | expr (MUL | DIV | MOD) expr               #binaryExpr
    | expr (ADD | SUB) expr                     #binaryExpr
    | expr (LT | LTE | GT | GTE) expr           #binaryExpr
    | expr (EQ | NEQ) expr                      #binaryExpr
    | expr AND expr                             #binaryExpr
    | expr OR expr                              #binaryExpr
    | <assoc=right> expr ASSIGN expr            #assignExpr
    ;

argList: expr (COMMA expr)*; 

primary: ID 
       | INT_LIT 
       | FLOAT_LIT 
       | STRING_LIT 
       | structLiteral 
       | LP expr RP; 

structLiteral: LB argList? RB; 

// --- LEXER RULES ---

// Keywords 
AUTO: 'auto';
BREAK: 'break';
CASE: 'case';
CONTINUE: 'continue';
DEFAULT: 'default';
ELSE: 'else';
FLOAT: 'float';
FOR: 'for';
IF: 'if';
INT: 'int';
RETURN: 'return';
STRING: 'string';
STRUCT: 'struct';
SWITCH: 'switch';
VOID: 'void';
WHILE: 'while';

// Operators & Separators 
ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
MOD: '%';
EQ: '==';
NEQ: '!=';
LT: '<';
GT: '>';
LTE: '<=';
GTE: '>=';
OR: '||';
AND: '&&';
NOT: '!';
INC: '++';
DEC: '--';
ASSIGN: '=';
DOT: '.';

//Separators
LB: '{';
RB: '}';
LP: '(';
RP: ')';
SEMI: ';';
COMMA: ',';
COLON: ':';

// Literals 
INT_LIT: [0-9]+; 

FLOAT_LIT: ([0-9]+ '.' [0-9]* EXP? | '.' [0-9]+ EXP? | [0-9]+ EXP); 
fragment EXP: [eE] [+-]? [0-9]+;

// Valid String
STRING_LIT: '"' ( ESC | ~["\\\r\n] )* '"'; 
fragment ESC: '\\' [bfrtn"\\/]; // Removed the backslash before /

ID: [a-zA-Z_] [a-zA-Z_0-9]*; 


// Error Handling Requirements [cite: 1, 2]
ILLEGAL_ESCAPE: '"' ( ESC | ~["\\\r\n] )* '\\' ~[bfrtn"\\/]; // Removed the backslash before /
UNCLOSE_STRING: '"' ( ESC | ~["\\\r\n] )*;

WS : [ \t\r\n\f]+ -> skip;

ERROR_CHAR: .;