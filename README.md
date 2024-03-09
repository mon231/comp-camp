# comp-camp
My python implementation of a byte-code compiler <br />
GOAL: implement fully functional compiler, from the code-language CPL to the bytecode language QUAD


## CPL Grammer
The following is the grammer I was given for the CPL code language:

```
program -> declarations stmt_block

declarations -> declarations declaration
    | epsilon

declaration -> idlist ':' type ';'

type -> INT
    | FLOAT

idlist -> idlist ',' ID
    | ID

stmt -> assignment_stmt
    | input_stmt
    | output_stmt
    | if_stmt
    | while_stmt
    | switch_stmt
    | break_stmt
    | stmt_block

assignment_stmt -> ID '=' expression ';'

input_stmt -> INPUT '(' ID ')' ';'

output_stmt -> OUTPUT '(' expression ')' ';'

if_stmt -> IF '(' boolexpr ')' stmt ELSE stmt

while_stmt -> WHILE '(' boolexpr ')' stmt

switch_stmt -> SWITCH '(' expression ')' '{' caselist DEFAULT ':' stmtlist '}'

caselist -> caselist CASE NUM ':' stmtlist
    | epsilon

break_stmt -> BREAK ';'

stmt_block -> '{' stmtlist '}'

stmtlist -> stmtlist stmt
    | epsilon

boolexpr -> boolexpr OR boolterm
    | boolterm

boolterm -> boolterm AND boolfactor
    | boolfactor

boolfactor -> NOT '(' boolexpr ')'
    | expression RELOP expression

expression -> expression ADDOP term
    | term

term -> term MULOP factor
    | factor

factor -> '(' expression ')'
    | CAST '(' expression ')'
    | ID
    | NUM
```
