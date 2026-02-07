grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// TODO: Define grammar rules here
program: (structDecl | funcDecl)* EOF;

structDecl: STRUCT ID LB structMember* RB SEMI;
structMember: type ID SEMI;

funcDecl: (returnType | ) ID LP paramList? RP block;
returnType: VOID | type;
paramList: param (COMMA param)*;
param: type ID;
block: LB stmt* RB;
stmt
    : block
    | varDeclStmt
    | ifStmt
    | whileStmt
    | forStmt
    | switchStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | exprStmt
;

varDeclStmt: (AUTO | type) ID (ASSIGN expr)? SEMI;

ifStmt: IF LP expr RP  stmt (ELSE  stmt )?; // Lưu ý {} ở statement

whileStmt: WHILE LP expr RP stmt ;

forStmt: FOR LP (varDeclStmt | exprStmt | SEMI) expr? SEMI expr? RP stmt ;

switchStmt: SWITCH LP expr RP LB (caseClause | defaultClause)* RB;
caseClause: CASE expr COLON stmt*;
defaultClause: DEFAULT COLON stmt*;

breakStmt: BREAK SEMI;

continueStmt: CONTINUE SEMI;

returnStmt: RETURN expr? SEMI;

exprStmt: expr? SEMI;


// Expressions with precedence and associativity
expr: expr1 (ASSIGN expr1)*;  // Right associative

expr1: expr2 (OR expr2)*;  // Left associative

expr2: expr3 (AND expr3)*;  // Left associative

expr3: expr4 ((EQ | NEQ) expr4)*;  // Left associative

expr4: expr5 ((LT | LE | GT | GE) expr5)*;  // Left associative

expr5: expr6 ((PLUS | MINUS) expr6)*;  // Left associative

expr6: expr7 ((STAR | SLASH | PERCENT) expr7)*;  // Left associative

expr7: expr8 (DOT ID)*;  // Left associative - member access

expr8: (NOT | MINUS | PLUS | INCR | DECR) expr8  // Right associative - unary/prefix
     | expr9;

expr9: expr10 (INCR | DECR)?;  // Postfix

expr10: INTLIT
      | FLOATLIT
      | STRINGLIT
      | ID (LP argList? RP)?  // ID or function call
      | LP expr RP
      | LB exprList? RB  // Struct initialization
      ;

argList: expr (COMMA expr)*;

exprList: expr (COMMA expr)*;

type: INT | FLOAT | STRING | ID;


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

// Operators
PLUS: '+';
MINUS: '-';
STAR: '*';
SLASH: '/';
PERCENT: '%';
EQ: '==';
NEQ: '!=';
LT: '<';
GT: '>';
LE: '<=';
GE: '>=';
OR: '||';
AND: '&&';
NOT: '!';
INCR: '++';
DECR: '--';
ASSIGN: '=';
DOT: '.';

// Separators
LB: '{';
RB: '}';
LP: '(';
RP: ')';
SEMI: ';';
COMMA: ',';
COLON: ':';

ID: [a-zA-Z_][a-zA-Z0-9_]*;

fragment DIGITS: [0-9]+;

fragment EXPONENT: [eE] [+-]? DIGITS;

INTLIT:  DIGITS;

FLOATLIT
        : DIGITS '.' DIGITS? EXPONENT?
        | '.' DIGITS EXPONENT?
        | DIGITS EXPONENT?
        ;

fragment ESC_SEQ: '\\' [bfrnt"\\];

fragment STR_CHAR: ~["\r\n\\] | ESC_SEQ ;


ILLEGAL_ESCAPE: '"' (STR_CHAR)* '\\' ~[bfrnt"\\\r\n]
              {
                  text = str(self.text)
                  self.text = text[1:]  
              };

UNCLOSE_STRING: '"' (STR_CHAR)* (EOF | '\r' | '\n')
              {
                txt = (self.text[1:])
                if( len(txt) > 0 and (txt[-1] == '\r' or txt[-1] == '\n')):
                  self.text = txt[:-1]
              }
;

STRINGLIT: '"' STR_CHAR* '"'
         {
             text = str(self.text)
             self.text = text[1:-1]
         };

BLOCK_COMMENT: '/*' .*? '*/' -> skip;  //Dấu ? là để lưu ý dừng lại ngay lập tức khi gặp dấu hiệu dừng lại gần nhất
LINE_COMMENT: '//' ~[\r\n]* -> skip;

WS : [ \t\r\n]+ -> skip ; 

ERROR_CHAR: .;