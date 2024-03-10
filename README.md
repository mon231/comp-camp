# comp-camp
My python implementation of a byte-code compiler <br />
GOAL: implement fully functional compiler, from the code-language CPL to the bytecode language QUAD

## CPL (code language)
The compiler should convert code from CPL to QUAD bytecode. <br />
The following is information about that code language:

<details>
    <summary>The CPL grammer I was given</summary>

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
</details>

<details>
    <summary>An auto-generated LALR for the CPL grammer, from the `parser` module I wrote</summary>

    state 0

        (0) S' -> . program
        (1) program -> . declarations stmt_block
        (2) declarations -> . declarations declaration
        (3) declarations -> . epsilon
        (43) epsilon -> .

        LBRACE          reduce using rule 43 (epsilon -> .)
        ID              reduce using rule 43 (epsilon -> .)

        program                        shift and go to state 1
        declarations                   shift and go to state 2
        epsilon                        shift and go to state 3

    state 1

        (0) S' -> program .



    state 2

        (1) program -> declarations . stmt_block
        (2) declarations -> declarations . declaration
        (26) stmt_block -> . LBRACE stmtlist RBRACE
        (4) declaration -> . idlist COLONS type SEMICOLON
        (7) idlist -> . idlist COMMA ID
        (8) idlist -> . ID

        LBRACE          shift and go to state 6
        ID              shift and go to state 8

        stmt_block                     shift and go to state 4
        declaration                    shift and go to state 5
        idlist                         shift and go to state 7

    state 3

        (3) declarations -> epsilon .

        LBRACE          reduce using rule 3 (declarations -> epsilon .)
        ID              reduce using rule 3 (declarations -> epsilon .)


    state 4

        (1) program -> declarations stmt_block .

        $end            reduce using rule 1 (program -> declarations stmt_block .)


    state 5

        (2) declarations -> declarations declaration .

        LBRACE          reduce using rule 2 (declarations -> declarations declaration .)
        ID              reduce using rule 2 (declarations -> declarations declaration .)


    state 6

        (26) stmt_block -> LBRACE . stmtlist RBRACE
        (27) stmtlist -> . stmtlist stmt
        (28) stmtlist -> . epsilon
        (43) epsilon -> .

        RBRACE          reduce using rule 43 (epsilon -> .)
        ID              reduce using rule 43 (epsilon -> .)
        INPUT           reduce using rule 43 (epsilon -> .)
        OUTPUT          reduce using rule 43 (epsilon -> .)
        IF              reduce using rule 43 (epsilon -> .)
        WHILE           reduce using rule 43 (epsilon -> .)
        SWITCH          reduce using rule 43 (epsilon -> .)
        BREAK           reduce using rule 43 (epsilon -> .)
        LBRACE          reduce using rule 43 (epsilon -> .)

        stmtlist                       shift and go to state 9
        epsilon                        shift and go to state 10

    state 7

        (4) declaration -> idlist . COLONS type SEMICOLON
        (7) idlist -> idlist . COMMA ID

        COLONS          shift and go to state 11
        COMMA           shift and go to state 12


    state 8

        (8) idlist -> ID .

        COLONS          reduce using rule 8 (idlist -> ID .)
        COMMA           reduce using rule 8 (idlist -> ID .)


    state 9

        (26) stmt_block -> LBRACE stmtlist . RBRACE
        (27) stmtlist -> stmtlist . stmt
        (9) stmt -> . assignment_stmt
        (10) stmt -> . input_stmt
        (11) stmt -> . output_stmt
        (12) stmt -> . if_stmt
        (13) stmt -> . while_stmt
        (14) stmt -> . switch_stmt
        (15) stmt -> . break_stmt
        (16) stmt -> . stmt_block
        (17) assignment_stmt -> . ID ASSIGNMENT expression SEMICOLON
        (18) input_stmt -> . INPUT LPARENT ID RPARENT SEMICOLON
        (19) output_stmt -> . OUTPUT LPARENT expression RPARENT SEMICOLON
        (20) if_stmt -> . IF LPARENT boolexpr RPARENT stmt ELSE stmt
        (21) while_stmt -> . WHILE LPARENT boolexpr RPARENT stmt
        (22) switch_stmt -> . SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE
        (25) break_stmt -> . BREAK SEMICOLON
        (26) stmt_block -> . LBRACE stmtlist RBRACE

        RBRACE          shift and go to state 13
        ID              shift and go to state 23
        INPUT           shift and go to state 24
        OUTPUT          shift and go to state 25
        IF              shift and go to state 26
        WHILE           shift and go to state 27
        SWITCH          shift and go to state 28
        BREAK           shift and go to state 29
        LBRACE          shift and go to state 6

        stmt                           shift and go to state 14
        assignment_stmt                shift and go to state 15
        input_stmt                     shift and go to state 16
        output_stmt                    shift and go to state 17
        if_stmt                        shift and go to state 18
        while_stmt                     shift and go to state 19
        switch_stmt                    shift and go to state 20
        break_stmt                     shift and go to state 21
        stmt_block                     shift and go to state 22

    state 10

        (28) stmtlist -> epsilon .

        RBRACE          reduce using rule 28 (stmtlist -> epsilon .)
        ID              reduce using rule 28 (stmtlist -> epsilon .)
        INPUT           reduce using rule 28 (stmtlist -> epsilon .)
        OUTPUT          reduce using rule 28 (stmtlist -> epsilon .)
        IF              reduce using rule 28 (stmtlist -> epsilon .)
        WHILE           reduce using rule 28 (stmtlist -> epsilon .)
        SWITCH          reduce using rule 28 (stmtlist -> epsilon .)
        BREAK           reduce using rule 28 (stmtlist -> epsilon .)
        LBRACE          reduce using rule 28 (stmtlist -> epsilon .)
        DEFAULT         reduce using rule 28 (stmtlist -> epsilon .)
        CASE            reduce using rule 28 (stmtlist -> epsilon .)


    state 11

        (4) declaration -> idlist COLONS . type SEMICOLON
        (5) type -> . INT
        (6) type -> . FLOAT

        INT             shift and go to state 31
        FLOAT           shift and go to state 32

        type                           shift and go to state 30

    state 12

        (7) idlist -> idlist COMMA . ID

        ID              shift and go to state 33


    state 13

        (26) stmt_block -> LBRACE stmtlist RBRACE .

        $end            reduce using rule 26 (stmt_block -> LBRACE stmtlist RBRACE .)
        RBRACE          reduce using rule 26 (stmt_block -> LBRACE stmtlist RBRACE .)
        ID              reduce using rule 26 (stmt_block -> LBRACE stmtlist RBRACE .)
        INPUT           reduce using rule 26 (stmt_block -> LBRACE stmtlist RBRACE .)
        OUTPUT          reduce using rule 26 (stmt_block -> LBRACE stmtlist RBRACE .)
        IF              reduce using rule 26 (stmt_block -> LBRACE stmtlist RBRACE .)
        WHILE           reduce using rule 26 (stmt_block -> LBRACE stmtlist RBRACE .)
        SWITCH          reduce using rule 26 (stmt_block -> LBRACE stmtlist RBRACE .)
        BREAK           reduce using rule 26 (stmt_block -> LBRACE stmtlist RBRACE .)
        LBRACE          reduce using rule 26 (stmt_block -> LBRACE stmtlist RBRACE .)
        ELSE            reduce using rule 26 (stmt_block -> LBRACE stmtlist RBRACE .)
        DEFAULT         reduce using rule 26 (stmt_block -> LBRACE stmtlist RBRACE .)
        CASE            reduce using rule 26 (stmt_block -> LBRACE stmtlist RBRACE .)


    state 14

        (27) stmtlist -> stmtlist stmt .

        RBRACE          reduce using rule 27 (stmtlist -> stmtlist stmt .)
        ID              reduce using rule 27 (stmtlist -> stmtlist stmt .)
        INPUT           reduce using rule 27 (stmtlist -> stmtlist stmt .)
        OUTPUT          reduce using rule 27 (stmtlist -> stmtlist stmt .)
        IF              reduce using rule 27 (stmtlist -> stmtlist stmt .)
        WHILE           reduce using rule 27 (stmtlist -> stmtlist stmt .)
        SWITCH          reduce using rule 27 (stmtlist -> stmtlist stmt .)
        BREAK           reduce using rule 27 (stmtlist -> stmtlist stmt .)
        LBRACE          reduce using rule 27 (stmtlist -> stmtlist stmt .)
        DEFAULT         reduce using rule 27 (stmtlist -> stmtlist stmt .)
        CASE            reduce using rule 27 (stmtlist -> stmtlist stmt .)


    state 15

        (9) stmt -> assignment_stmt .

        RBRACE          reduce using rule 9 (stmt -> assignment_stmt .)
        ID              reduce using rule 9 (stmt -> assignment_stmt .)
        INPUT           reduce using rule 9 (stmt -> assignment_stmt .)
        OUTPUT          reduce using rule 9 (stmt -> assignment_stmt .)
        IF              reduce using rule 9 (stmt -> assignment_stmt .)
        WHILE           reduce using rule 9 (stmt -> assignment_stmt .)
        SWITCH          reduce using rule 9 (stmt -> assignment_stmt .)
        BREAK           reduce using rule 9 (stmt -> assignment_stmt .)
        LBRACE          reduce using rule 9 (stmt -> assignment_stmt .)
        ELSE            reduce using rule 9 (stmt -> assignment_stmt .)
        DEFAULT         reduce using rule 9 (stmt -> assignment_stmt .)
        CASE            reduce using rule 9 (stmt -> assignment_stmt .)


    state 16

        (10) stmt -> input_stmt .

        RBRACE          reduce using rule 10 (stmt -> input_stmt .)
        ID              reduce using rule 10 (stmt -> input_stmt .)
        INPUT           reduce using rule 10 (stmt -> input_stmt .)
        OUTPUT          reduce using rule 10 (stmt -> input_stmt .)
        IF              reduce using rule 10 (stmt -> input_stmt .)
        WHILE           reduce using rule 10 (stmt -> input_stmt .)
        SWITCH          reduce using rule 10 (stmt -> input_stmt .)
        BREAK           reduce using rule 10 (stmt -> input_stmt .)
        LBRACE          reduce using rule 10 (stmt -> input_stmt .)
        ELSE            reduce using rule 10 (stmt -> input_stmt .)
        DEFAULT         reduce using rule 10 (stmt -> input_stmt .)
        CASE            reduce using rule 10 (stmt -> input_stmt .)


    state 17

        (11) stmt -> output_stmt .

        RBRACE          reduce using rule 11 (stmt -> output_stmt .)
        ID              reduce using rule 11 (stmt -> output_stmt .)
        INPUT           reduce using rule 11 (stmt -> output_stmt .)
        OUTPUT          reduce using rule 11 (stmt -> output_stmt .)
        IF              reduce using rule 11 (stmt -> output_stmt .)
        WHILE           reduce using rule 11 (stmt -> output_stmt .)
        SWITCH          reduce using rule 11 (stmt -> output_stmt .)
        BREAK           reduce using rule 11 (stmt -> output_stmt .)
        LBRACE          reduce using rule 11 (stmt -> output_stmt .)
        ELSE            reduce using rule 11 (stmt -> output_stmt .)
        DEFAULT         reduce using rule 11 (stmt -> output_stmt .)
        CASE            reduce using rule 11 (stmt -> output_stmt .)


    state 18

        (12) stmt -> if_stmt .

        RBRACE          reduce using rule 12 (stmt -> if_stmt .)
        ID              reduce using rule 12 (stmt -> if_stmt .)
        INPUT           reduce using rule 12 (stmt -> if_stmt .)
        OUTPUT          reduce using rule 12 (stmt -> if_stmt .)
        IF              reduce using rule 12 (stmt -> if_stmt .)
        WHILE           reduce using rule 12 (stmt -> if_stmt .)
        SWITCH          reduce using rule 12 (stmt -> if_stmt .)
        BREAK           reduce using rule 12 (stmt -> if_stmt .)
        LBRACE          reduce using rule 12 (stmt -> if_stmt .)
        ELSE            reduce using rule 12 (stmt -> if_stmt .)
        DEFAULT         reduce using rule 12 (stmt -> if_stmt .)
        CASE            reduce using rule 12 (stmt -> if_stmt .)


    state 19

        (13) stmt -> while_stmt .

        RBRACE          reduce using rule 13 (stmt -> while_stmt .)
        ID              reduce using rule 13 (stmt -> while_stmt .)
        INPUT           reduce using rule 13 (stmt -> while_stmt .)
        OUTPUT          reduce using rule 13 (stmt -> while_stmt .)
        IF              reduce using rule 13 (stmt -> while_stmt .)
        WHILE           reduce using rule 13 (stmt -> while_stmt .)
        SWITCH          reduce using rule 13 (stmt -> while_stmt .)
        BREAK           reduce using rule 13 (stmt -> while_stmt .)
        LBRACE          reduce using rule 13 (stmt -> while_stmt .)
        ELSE            reduce using rule 13 (stmt -> while_stmt .)
        DEFAULT         reduce using rule 13 (stmt -> while_stmt .)
        CASE            reduce using rule 13 (stmt -> while_stmt .)


    state 20

        (14) stmt -> switch_stmt .

        RBRACE          reduce using rule 14 (stmt -> switch_stmt .)
        ID              reduce using rule 14 (stmt -> switch_stmt .)
        INPUT           reduce using rule 14 (stmt -> switch_stmt .)
        OUTPUT          reduce using rule 14 (stmt -> switch_stmt .)
        IF              reduce using rule 14 (stmt -> switch_stmt .)
        WHILE           reduce using rule 14 (stmt -> switch_stmt .)
        SWITCH          reduce using rule 14 (stmt -> switch_stmt .)
        BREAK           reduce using rule 14 (stmt -> switch_stmt .)
        LBRACE          reduce using rule 14 (stmt -> switch_stmt .)
        ELSE            reduce using rule 14 (stmt -> switch_stmt .)
        DEFAULT         reduce using rule 14 (stmt -> switch_stmt .)
        CASE            reduce using rule 14 (stmt -> switch_stmt .)


    state 21

        (15) stmt -> break_stmt .

        RBRACE          reduce using rule 15 (stmt -> break_stmt .)
        ID              reduce using rule 15 (stmt -> break_stmt .)
        INPUT           reduce using rule 15 (stmt -> break_stmt .)
        OUTPUT          reduce using rule 15 (stmt -> break_stmt .)
        IF              reduce using rule 15 (stmt -> break_stmt .)
        WHILE           reduce using rule 15 (stmt -> break_stmt .)
        SWITCH          reduce using rule 15 (stmt -> break_stmt .)
        BREAK           reduce using rule 15 (stmt -> break_stmt .)
        LBRACE          reduce using rule 15 (stmt -> break_stmt .)
        ELSE            reduce using rule 15 (stmt -> break_stmt .)
        DEFAULT         reduce using rule 15 (stmt -> break_stmt .)
        CASE            reduce using rule 15 (stmt -> break_stmt .)


    state 22

        (16) stmt -> stmt_block .

        RBRACE          reduce using rule 16 (stmt -> stmt_block .)
        ID              reduce using rule 16 (stmt -> stmt_block .)
        INPUT           reduce using rule 16 (stmt -> stmt_block .)
        OUTPUT          reduce using rule 16 (stmt -> stmt_block .)
        IF              reduce using rule 16 (stmt -> stmt_block .)
        WHILE           reduce using rule 16 (stmt -> stmt_block .)
        SWITCH          reduce using rule 16 (stmt -> stmt_block .)
        BREAK           reduce using rule 16 (stmt -> stmt_block .)
        LBRACE          reduce using rule 16 (stmt -> stmt_block .)
        ELSE            reduce using rule 16 (stmt -> stmt_block .)
        DEFAULT         reduce using rule 16 (stmt -> stmt_block .)
        CASE            reduce using rule 16 (stmt -> stmt_block .)


    state 23

        (17) assignment_stmt -> ID . ASSIGNMENT expression SEMICOLON

        ASSIGNMENT      shift and go to state 34


    state 24

        (18) input_stmt -> INPUT . LPARENT ID RPARENT SEMICOLON

        LPARENT         shift and go to state 35


    state 25

        (19) output_stmt -> OUTPUT . LPARENT expression RPARENT SEMICOLON

        LPARENT         shift and go to state 36


    state 26

        (20) if_stmt -> IF . LPARENT boolexpr RPARENT stmt ELSE stmt

        LPARENT         shift and go to state 37


    state 27

        (21) while_stmt -> WHILE . LPARENT boolexpr RPARENT stmt

        LPARENT         shift and go to state 38


    state 28

        (22) switch_stmt -> SWITCH . LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE

        LPARENT         shift and go to state 39


    state 29

        (25) break_stmt -> BREAK . SEMICOLON

        SEMICOLON       shift and go to state 40


    state 30

        (4) declaration -> idlist COLONS type . SEMICOLON

        SEMICOLON       shift and go to state 41


    state 31

        (5) type -> INT .

        SEMICOLON       reduce using rule 5 (type -> INT .)


    state 32

        (6) type -> FLOAT .

        SEMICOLON       reduce using rule 6 (type -> FLOAT .)


    state 33

        (7) idlist -> idlist COMMA ID .

        COLONS          reduce using rule 7 (idlist -> idlist COMMA ID .)
        COMMA           reduce using rule 7 (idlist -> idlist COMMA ID .)


    state 34

        (17) assignment_stmt -> ID ASSIGNMENT . expression SEMICOLON
        (35) expression -> . expression ADDOP term
        (36) expression -> . term
        (37) term -> . term MULOP factor
        (38) term -> . factor
        (39) factor -> . LPARENT expression RPARENT
        (40) factor -> . CAST LPARENT expression RPARENT
        (41) factor -> . ID
        (42) factor -> . NUM

        LPARENT         shift and go to state 46
        CAST            shift and go to state 47
        ID              shift and go to state 42
        NUM             shift and go to state 48

        expression                     shift and go to state 43
        term                           shift and go to state 44
        factor                         shift and go to state 45

    state 35

        (18) input_stmt -> INPUT LPARENT . ID RPARENT SEMICOLON

        ID              shift and go to state 49


    state 36

        (19) output_stmt -> OUTPUT LPARENT . expression RPARENT SEMICOLON
        (35) expression -> . expression ADDOP term
        (36) expression -> . term
        (37) term -> . term MULOP factor
        (38) term -> . factor
        (39) factor -> . LPARENT expression RPARENT
        (40) factor -> . CAST LPARENT expression RPARENT
        (41) factor -> . ID
        (42) factor -> . NUM

        LPARENT         shift and go to state 46
        CAST            shift and go to state 47
        ID              shift and go to state 42
        NUM             shift and go to state 48

        expression                     shift and go to state 50
        term                           shift and go to state 44
        factor                         shift and go to state 45

    state 37

        (20) if_stmt -> IF LPARENT . boolexpr RPARENT stmt ELSE stmt
        (29) boolexpr -> . boolexpr OR boolterm
        (30) boolexpr -> . boolterm
        (31) boolterm -> . boolterm AND boolfactor
        (32) boolterm -> . boolfactor
        (33) boolfactor -> . NOT LPARENT boolexpr RPARENT
        (34) boolfactor -> . expression RELOP expression
        (35) expression -> . expression ADDOP term
        (36) expression -> . term
        (37) term -> . term MULOP factor
        (38) term -> . factor
        (39) factor -> . LPARENT expression RPARENT
        (40) factor -> . CAST LPARENT expression RPARENT
        (41) factor -> . ID
        (42) factor -> . NUM

        NOT             shift and go to state 54
        LPARENT         shift and go to state 46
        CAST            shift and go to state 47
        ID              shift and go to state 42
        NUM             shift and go to state 48

        boolexpr                       shift and go to state 51
        boolterm                       shift and go to state 52
        boolfactor                     shift and go to state 53
        expression                     shift and go to state 55
        term                           shift and go to state 44
        factor                         shift and go to state 45

    state 38

        (21) while_stmt -> WHILE LPARENT . boolexpr RPARENT stmt
        (29) boolexpr -> . boolexpr OR boolterm
        (30) boolexpr -> . boolterm
        (31) boolterm -> . boolterm AND boolfactor
        (32) boolterm -> . boolfactor
        (33) boolfactor -> . NOT LPARENT boolexpr RPARENT
        (34) boolfactor -> . expression RELOP expression
        (35) expression -> . expression ADDOP term
        (36) expression -> . term
        (37) term -> . term MULOP factor
        (38) term -> . factor
        (39) factor -> . LPARENT expression RPARENT
        (40) factor -> . CAST LPARENT expression RPARENT
        (41) factor -> . ID
        (42) factor -> . NUM

        NOT             shift and go to state 54
        LPARENT         shift and go to state 46
        CAST            shift and go to state 47
        ID              shift and go to state 42
        NUM             shift and go to state 48

        boolexpr                       shift and go to state 56
        boolterm                       shift and go to state 52
        boolfactor                     shift and go to state 53
        expression                     shift and go to state 55
        term                           shift and go to state 44
        factor                         shift and go to state 45

    state 39

        (22) switch_stmt -> SWITCH LPARENT . expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE
        (35) expression -> . expression ADDOP term
        (36) expression -> . term
        (37) term -> . term MULOP factor
        (38) term -> . factor
        (39) factor -> . LPARENT expression RPARENT
        (40) factor -> . CAST LPARENT expression RPARENT
        (41) factor -> . ID
        (42) factor -> . NUM

        LPARENT         shift and go to state 46
        CAST            shift and go to state 47
        ID              shift and go to state 42
        NUM             shift and go to state 48

        expression                     shift and go to state 57
        term                           shift and go to state 44
        factor                         shift and go to state 45

    state 40

        (25) break_stmt -> BREAK SEMICOLON .

        RBRACE          reduce using rule 25 (break_stmt -> BREAK SEMICOLON .)
        ID              reduce using rule 25 (break_stmt -> BREAK SEMICOLON .)
        INPUT           reduce using rule 25 (break_stmt -> BREAK SEMICOLON .)
        OUTPUT          reduce using rule 25 (break_stmt -> BREAK SEMICOLON .)
        IF              reduce using rule 25 (break_stmt -> BREAK SEMICOLON .)
        WHILE           reduce using rule 25 (break_stmt -> BREAK SEMICOLON .)
        SWITCH          reduce using rule 25 (break_stmt -> BREAK SEMICOLON .)
        BREAK           reduce using rule 25 (break_stmt -> BREAK SEMICOLON .)
        LBRACE          reduce using rule 25 (break_stmt -> BREAK SEMICOLON .)
        ELSE            reduce using rule 25 (break_stmt -> BREAK SEMICOLON .)
        DEFAULT         reduce using rule 25 (break_stmt -> BREAK SEMICOLON .)
        CASE            reduce using rule 25 (break_stmt -> BREAK SEMICOLON .)


    state 41

        (4) declaration -> idlist COLONS type SEMICOLON .

        LBRACE          reduce using rule 4 (declaration -> idlist COLONS type SEMICOLON .)
        ID              reduce using rule 4 (declaration -> idlist COLONS type SEMICOLON .)


    state 42

        (41) factor -> ID .

        MULOP           reduce using rule 41 (factor -> ID .)
        SEMICOLON       reduce using rule 41 (factor -> ID .)
        ADDOP           reduce using rule 41 (factor -> ID .)
        RPARENT         reduce using rule 41 (factor -> ID .)
        RELOP           reduce using rule 41 (factor -> ID .)
        AND             reduce using rule 41 (factor -> ID .)
        OR              reduce using rule 41 (factor -> ID .)


    state 43

        (17) assignment_stmt -> ID ASSIGNMENT expression . SEMICOLON
        (35) expression -> expression . ADDOP term

        SEMICOLON       shift and go to state 58
        ADDOP           shift and go to state 59


    state 44

        (36) expression -> term .
        (37) term -> term . MULOP factor

        SEMICOLON       reduce using rule 36 (expression -> term .)
        ADDOP           reduce using rule 36 (expression -> term .)
        RPARENT         reduce using rule 36 (expression -> term .)
        RELOP           reduce using rule 36 (expression -> term .)
        AND             reduce using rule 36 (expression -> term .)
        OR              reduce using rule 36 (expression -> term .)
        MULOP           shift and go to state 60


    state 45

        (38) term -> factor .

        MULOP           reduce using rule 38 (term -> factor .)
        SEMICOLON       reduce using rule 38 (term -> factor .)
        ADDOP           reduce using rule 38 (term -> factor .)
        RPARENT         reduce using rule 38 (term -> factor .)
        RELOP           reduce using rule 38 (term -> factor .)
        AND             reduce using rule 38 (term -> factor .)
        OR              reduce using rule 38 (term -> factor .)


    state 46

        (39) factor -> LPARENT . expression RPARENT
        (35) expression -> . expression ADDOP term
        (36) expression -> . term
        (37) term -> . term MULOP factor
        (38) term -> . factor
        (39) factor -> . LPARENT expression RPARENT
        (40) factor -> . CAST LPARENT expression RPARENT
        (41) factor -> . ID
        (42) factor -> . NUM

        LPARENT         shift and go to state 46
        CAST            shift and go to state 47
        ID              shift and go to state 42
        NUM             shift and go to state 48

        expression                     shift and go to state 61
        term                           shift and go to state 44
        factor                         shift and go to state 45

    state 47

        (40) factor -> CAST . LPARENT expression RPARENT

        LPARENT         shift and go to state 62


    state 48

        (42) factor -> NUM .

        MULOP           reduce using rule 42 (factor -> NUM .)
        SEMICOLON       reduce using rule 42 (factor -> NUM .)
        ADDOP           reduce using rule 42 (factor -> NUM .)
        RPARENT         reduce using rule 42 (factor -> NUM .)
        RELOP           reduce using rule 42 (factor -> NUM .)
        AND             reduce using rule 42 (factor -> NUM .)
        OR              reduce using rule 42 (factor -> NUM .)


    state 49

        (18) input_stmt -> INPUT LPARENT ID . RPARENT SEMICOLON

        RPARENT         shift and go to state 63


    state 50

        (19) output_stmt -> OUTPUT LPARENT expression . RPARENT SEMICOLON
        (35) expression -> expression . ADDOP term

        RPARENT         shift and go to state 64
        ADDOP           shift and go to state 59


    state 51

        (20) if_stmt -> IF LPARENT boolexpr . RPARENT stmt ELSE stmt
        (29) boolexpr -> boolexpr . OR boolterm

        RPARENT         shift and go to state 65
        OR              shift and go to state 66


    state 52

        (30) boolexpr -> boolterm .
        (31) boolterm -> boolterm . AND boolfactor

        RPARENT         reduce using rule 30 (boolexpr -> boolterm .)
        OR              reduce using rule 30 (boolexpr -> boolterm .)
        AND             shift and go to state 67


    state 53

        (32) boolterm -> boolfactor .

        AND             reduce using rule 32 (boolterm -> boolfactor .)
        RPARENT         reduce using rule 32 (boolterm -> boolfactor .)
        OR              reduce using rule 32 (boolterm -> boolfactor .)


    state 54

        (33) boolfactor -> NOT . LPARENT boolexpr RPARENT

        LPARENT         shift and go to state 68


    state 55

        (34) boolfactor -> expression . RELOP expression
        (35) expression -> expression . ADDOP term

        RELOP           shift and go to state 69
        ADDOP           shift and go to state 59


    state 56

        (21) while_stmt -> WHILE LPARENT boolexpr . RPARENT stmt
        (29) boolexpr -> boolexpr . OR boolterm

        RPARENT         shift and go to state 70
        OR              shift and go to state 66


    state 57

        (22) switch_stmt -> SWITCH LPARENT expression . RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE
        (35) expression -> expression . ADDOP term

        RPARENT         shift and go to state 71
        ADDOP           shift and go to state 59


    state 58

        (17) assignment_stmt -> ID ASSIGNMENT expression SEMICOLON .

        RBRACE          reduce using rule 17 (assignment_stmt -> ID ASSIGNMENT expression SEMICOLON .)
        ID              reduce using rule 17 (assignment_stmt -> ID ASSIGNMENT expression SEMICOLON .)
        INPUT           reduce using rule 17 (assignment_stmt -> ID ASSIGNMENT expression SEMICOLON .)
        OUTPUT          reduce using rule 17 (assignment_stmt -> ID ASSIGNMENT expression SEMICOLON .)
        IF              reduce using rule 17 (assignment_stmt -> ID ASSIGNMENT expression SEMICOLON .)
        WHILE           reduce using rule 17 (assignment_stmt -> ID ASSIGNMENT expression SEMICOLON .)
        SWITCH          reduce using rule 17 (assignment_stmt -> ID ASSIGNMENT expression SEMICOLON .)
        BREAK           reduce using rule 17 (assignment_stmt -> ID ASSIGNMENT expression SEMICOLON .)
        LBRACE          reduce using rule 17 (assignment_stmt -> ID ASSIGNMENT expression SEMICOLON .)
        ELSE            reduce using rule 17 (assignment_stmt -> ID ASSIGNMENT expression SEMICOLON .)
        DEFAULT         reduce using rule 17 (assignment_stmt -> ID ASSIGNMENT expression SEMICOLON .)
        CASE            reduce using rule 17 (assignment_stmt -> ID ASSIGNMENT expression SEMICOLON .)


    state 59

        (35) expression -> expression ADDOP . term
        (37) term -> . term MULOP factor
        (38) term -> . factor
        (39) factor -> . LPARENT expression RPARENT
        (40) factor -> . CAST LPARENT expression RPARENT
        (41) factor -> . ID
        (42) factor -> . NUM

        LPARENT         shift and go to state 46
        CAST            shift and go to state 47
        ID              shift and go to state 42
        NUM             shift and go to state 48

        term                           shift and go to state 72
        factor                         shift and go to state 45

    state 60

        (37) term -> term MULOP . factor
        (39) factor -> . LPARENT expression RPARENT
        (40) factor -> . CAST LPARENT expression RPARENT
        (41) factor -> . ID
        (42) factor -> . NUM

        LPARENT         shift and go to state 46
        CAST            shift and go to state 47
        ID              shift and go to state 42
        NUM             shift and go to state 48

        factor                         shift and go to state 73

    state 61

        (39) factor -> LPARENT expression . RPARENT
        (35) expression -> expression . ADDOP term

        RPARENT         shift and go to state 74
        ADDOP           shift and go to state 59


    state 62

        (40) factor -> CAST LPARENT . expression RPARENT
        (35) expression -> . expression ADDOP term
        (36) expression -> . term
        (37) term -> . term MULOP factor
        (38) term -> . factor
        (39) factor -> . LPARENT expression RPARENT
        (40) factor -> . CAST LPARENT expression RPARENT
        (41) factor -> . ID
        (42) factor -> . NUM

        LPARENT         shift and go to state 46
        CAST            shift and go to state 47
        ID              shift and go to state 42
        NUM             shift and go to state 48

        expression                     shift and go to state 75
        term                           shift and go to state 44
        factor                         shift and go to state 45

    state 63

        (18) input_stmt -> INPUT LPARENT ID RPARENT . SEMICOLON

        SEMICOLON       shift and go to state 76


    state 64

        (19) output_stmt -> OUTPUT LPARENT expression RPARENT . SEMICOLON

        SEMICOLON       shift and go to state 77


    state 65

        (20) if_stmt -> IF LPARENT boolexpr RPARENT . stmt ELSE stmt
        (9) stmt -> . assignment_stmt
        (10) stmt -> . input_stmt
        (11) stmt -> . output_stmt
        (12) stmt -> . if_stmt
        (13) stmt -> . while_stmt
        (14) stmt -> . switch_stmt
        (15) stmt -> . break_stmt
        (16) stmt -> . stmt_block
        (17) assignment_stmt -> . ID ASSIGNMENT expression SEMICOLON
        (18) input_stmt -> . INPUT LPARENT ID RPARENT SEMICOLON
        (19) output_stmt -> . OUTPUT LPARENT expression RPARENT SEMICOLON
        (20) if_stmt -> . IF LPARENT boolexpr RPARENT stmt ELSE stmt
        (21) while_stmt -> . WHILE LPARENT boolexpr RPARENT stmt
        (22) switch_stmt -> . SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE
        (25) break_stmt -> . BREAK SEMICOLON
        (26) stmt_block -> . LBRACE stmtlist RBRACE

        ID              shift and go to state 23
        INPUT           shift and go to state 24
        OUTPUT          shift and go to state 25
        IF              shift and go to state 26
        WHILE           shift and go to state 27
        SWITCH          shift and go to state 28
        BREAK           shift and go to state 29
        LBRACE          shift and go to state 6

        stmt                           shift and go to state 78
        assignment_stmt                shift and go to state 15
        input_stmt                     shift and go to state 16
        output_stmt                    shift and go to state 17
        if_stmt                        shift and go to state 18
        while_stmt                     shift and go to state 19
        switch_stmt                    shift and go to state 20
        break_stmt                     shift and go to state 21
        stmt_block                     shift and go to state 22

    state 66

        (29) boolexpr -> boolexpr OR . boolterm
        (31) boolterm -> . boolterm AND boolfactor
        (32) boolterm -> . boolfactor
        (33) boolfactor -> . NOT LPARENT boolexpr RPARENT
        (34) boolfactor -> . expression RELOP expression
        (35) expression -> . expression ADDOP term
        (36) expression -> . term
        (37) term -> . term MULOP factor
        (38) term -> . factor
        (39) factor -> . LPARENT expression RPARENT
        (40) factor -> . CAST LPARENT expression RPARENT
        (41) factor -> . ID
        (42) factor -> . NUM

        NOT             shift and go to state 54
        LPARENT         shift and go to state 46
        CAST            shift and go to state 47
        ID              shift and go to state 42
        NUM             shift and go to state 48

        boolterm                       shift and go to state 79
        boolfactor                     shift and go to state 53
        expression                     shift and go to state 55
        term                           shift and go to state 44
        factor                         shift and go to state 45

    state 67

        (31) boolterm -> boolterm AND . boolfactor
        (33) boolfactor -> . NOT LPARENT boolexpr RPARENT
        (34) boolfactor -> . expression RELOP expression
        (35) expression -> . expression ADDOP term
        (36) expression -> . term
        (37) term -> . term MULOP factor
        (38) term -> . factor
        (39) factor -> . LPARENT expression RPARENT
        (40) factor -> . CAST LPARENT expression RPARENT
        (41) factor -> . ID
        (42) factor -> . NUM

        NOT             shift and go to state 54
        LPARENT         shift and go to state 46
        CAST            shift and go to state 47
        ID              shift and go to state 42
        NUM             shift and go to state 48

        boolfactor                     shift and go to state 80
        expression                     shift and go to state 55
        term                           shift and go to state 44
        factor                         shift and go to state 45

    state 68

        (33) boolfactor -> NOT LPARENT . boolexpr RPARENT
        (29) boolexpr -> . boolexpr OR boolterm
        (30) boolexpr -> . boolterm
        (31) boolterm -> . boolterm AND boolfactor
        (32) boolterm -> . boolfactor
        (33) boolfactor -> . NOT LPARENT boolexpr RPARENT
        (34) boolfactor -> . expression RELOP expression
        (35) expression -> . expression ADDOP term
        (36) expression -> . term
        (37) term -> . term MULOP factor
        (38) term -> . factor
        (39) factor -> . LPARENT expression RPARENT
        (40) factor -> . CAST LPARENT expression RPARENT
        (41) factor -> . ID
        (42) factor -> . NUM

        NOT             shift and go to state 54
        LPARENT         shift and go to state 46
        CAST            shift and go to state 47
        ID              shift and go to state 42
        NUM             shift and go to state 48

        boolexpr                       shift and go to state 81
        boolterm                       shift and go to state 52
        boolfactor                     shift and go to state 53
        expression                     shift and go to state 55
        term                           shift and go to state 44
        factor                         shift and go to state 45

    state 69

        (34) boolfactor -> expression RELOP . expression
        (35) expression -> . expression ADDOP term
        (36) expression -> . term
        (37) term -> . term MULOP factor
        (38) term -> . factor
        (39) factor -> . LPARENT expression RPARENT
        (40) factor -> . CAST LPARENT expression RPARENT
        (41) factor -> . ID
        (42) factor -> . NUM

        LPARENT         shift and go to state 46
        CAST            shift and go to state 47
        ID              shift and go to state 42
        NUM             shift and go to state 48

        expression                     shift and go to state 82
        term                           shift and go to state 44
        factor                         shift and go to state 45

    state 70

        (21) while_stmt -> WHILE LPARENT boolexpr RPARENT . stmt
        (9) stmt -> . assignment_stmt
        (10) stmt -> . input_stmt
        (11) stmt -> . output_stmt
        (12) stmt -> . if_stmt
        (13) stmt -> . while_stmt
        (14) stmt -> . switch_stmt
        (15) stmt -> . break_stmt
        (16) stmt -> . stmt_block
        (17) assignment_stmt -> . ID ASSIGNMENT expression SEMICOLON
        (18) input_stmt -> . INPUT LPARENT ID RPARENT SEMICOLON
        (19) output_stmt -> . OUTPUT LPARENT expression RPARENT SEMICOLON
        (20) if_stmt -> . IF LPARENT boolexpr RPARENT stmt ELSE stmt
        (21) while_stmt -> . WHILE LPARENT boolexpr RPARENT stmt
        (22) switch_stmt -> . SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE
        (25) break_stmt -> . BREAK SEMICOLON
        (26) stmt_block -> . LBRACE stmtlist RBRACE

        ID              shift and go to state 23
        INPUT           shift and go to state 24
        OUTPUT          shift and go to state 25
        IF              shift and go to state 26
        WHILE           shift and go to state 27
        SWITCH          shift and go to state 28
        BREAK           shift and go to state 29
        LBRACE          shift and go to state 6

        stmt                           shift and go to state 83
        assignment_stmt                shift and go to state 15
        input_stmt                     shift and go to state 16
        output_stmt                    shift and go to state 17
        if_stmt                        shift and go to state 18
        while_stmt                     shift and go to state 19
        switch_stmt                    shift and go to state 20
        break_stmt                     shift and go to state 21
        stmt_block                     shift and go to state 22

    state 71

        (22) switch_stmt -> SWITCH LPARENT expression RPARENT . LBRACE caselist DEFAULT COLONS stmtlist RBRACE

        LBRACE          shift and go to state 84


    state 72

        (35) expression -> expression ADDOP term .
        (37) term -> term . MULOP factor

        SEMICOLON       reduce using rule 35 (expression -> expression ADDOP term .)
        ADDOP           reduce using rule 35 (expression -> expression ADDOP term .)
        RPARENT         reduce using rule 35 (expression -> expression ADDOP term .)
        RELOP           reduce using rule 35 (expression -> expression ADDOP term .)
        AND             reduce using rule 35 (expression -> expression ADDOP term .)
        OR              reduce using rule 35 (expression -> expression ADDOP term .)
        MULOP           shift and go to state 60


    state 73

        (37) term -> term MULOP factor .

        MULOP           reduce using rule 37 (term -> term MULOP factor .)
        SEMICOLON       reduce using rule 37 (term -> term MULOP factor .)
        ADDOP           reduce using rule 37 (term -> term MULOP factor .)
        RPARENT         reduce using rule 37 (term -> term MULOP factor .)
        RELOP           reduce using rule 37 (term -> term MULOP factor .)
        AND             reduce using rule 37 (term -> term MULOP factor .)
        OR              reduce using rule 37 (term -> term MULOP factor .)


    state 74

        (39) factor -> LPARENT expression RPARENT .

        MULOP           reduce using rule 39 (factor -> LPARENT expression RPARENT .)
        SEMICOLON       reduce using rule 39 (factor -> LPARENT expression RPARENT .)
        ADDOP           reduce using rule 39 (factor -> LPARENT expression RPARENT .)
        RPARENT         reduce using rule 39 (factor -> LPARENT expression RPARENT .)
        RELOP           reduce using rule 39 (factor -> LPARENT expression RPARENT .)
        AND             reduce using rule 39 (factor -> LPARENT expression RPARENT .)
        OR              reduce using rule 39 (factor -> LPARENT expression RPARENT .)


    state 75

        (40) factor -> CAST LPARENT expression . RPARENT
        (35) expression -> expression . ADDOP term

        RPARENT         shift and go to state 85
        ADDOP           shift and go to state 59


    state 76

        (18) input_stmt -> INPUT LPARENT ID RPARENT SEMICOLON .

        RBRACE          reduce using rule 18 (input_stmt -> INPUT LPARENT ID RPARENT SEMICOLON .)
        ID              reduce using rule 18 (input_stmt -> INPUT LPARENT ID RPARENT SEMICOLON .)
        INPUT           reduce using rule 18 (input_stmt -> INPUT LPARENT ID RPARENT SEMICOLON .)
        OUTPUT          reduce using rule 18 (input_stmt -> INPUT LPARENT ID RPARENT SEMICOLON .)
        IF              reduce using rule 18 (input_stmt -> INPUT LPARENT ID RPARENT SEMICOLON .)
        WHILE           reduce using rule 18 (input_stmt -> INPUT LPARENT ID RPARENT SEMICOLON .)
        SWITCH          reduce using rule 18 (input_stmt -> INPUT LPARENT ID RPARENT SEMICOLON .)
        BREAK           reduce using rule 18 (input_stmt -> INPUT LPARENT ID RPARENT SEMICOLON .)
        LBRACE          reduce using rule 18 (input_stmt -> INPUT LPARENT ID RPARENT SEMICOLON .)
        ELSE            reduce using rule 18 (input_stmt -> INPUT LPARENT ID RPARENT SEMICOLON .)
        DEFAULT         reduce using rule 18 (input_stmt -> INPUT LPARENT ID RPARENT SEMICOLON .)
        CASE            reduce using rule 18 (input_stmt -> INPUT LPARENT ID RPARENT SEMICOLON .)


    state 77

        (19) output_stmt -> OUTPUT LPARENT expression RPARENT SEMICOLON .

        RBRACE          reduce using rule 19 (output_stmt -> OUTPUT LPARENT expression RPARENT SEMICOLON .)
        ID              reduce using rule 19 (output_stmt -> OUTPUT LPARENT expression RPARENT SEMICOLON .)
        INPUT           reduce using rule 19 (output_stmt -> OUTPUT LPARENT expression RPARENT SEMICOLON .)
        OUTPUT          reduce using rule 19 (output_stmt -> OUTPUT LPARENT expression RPARENT SEMICOLON .)
        IF              reduce using rule 19 (output_stmt -> OUTPUT LPARENT expression RPARENT SEMICOLON .)
        WHILE           reduce using rule 19 (output_stmt -> OUTPUT LPARENT expression RPARENT SEMICOLON .)
        SWITCH          reduce using rule 19 (output_stmt -> OUTPUT LPARENT expression RPARENT SEMICOLON .)
        BREAK           reduce using rule 19 (output_stmt -> OUTPUT LPARENT expression RPARENT SEMICOLON .)
        LBRACE          reduce using rule 19 (output_stmt -> OUTPUT LPARENT expression RPARENT SEMICOLON .)
        ELSE            reduce using rule 19 (output_stmt -> OUTPUT LPARENT expression RPARENT SEMICOLON .)
        DEFAULT         reduce using rule 19 (output_stmt -> OUTPUT LPARENT expression RPARENT SEMICOLON .)
        CASE            reduce using rule 19 (output_stmt -> OUTPUT LPARENT expression RPARENT SEMICOLON .)


    state 78

        (20) if_stmt -> IF LPARENT boolexpr RPARENT stmt . ELSE stmt

        ELSE            shift and go to state 86


    state 79

        (29) boolexpr -> boolexpr OR boolterm .
        (31) boolterm -> boolterm . AND boolfactor

        RPARENT         reduce using rule 29 (boolexpr -> boolexpr OR boolterm .)
        OR              reduce using rule 29 (boolexpr -> boolexpr OR boolterm .)
        AND             shift and go to state 67


    state 80

        (31) boolterm -> boolterm AND boolfactor .

        AND             reduce using rule 31 (boolterm -> boolterm AND boolfactor .)
        RPARENT         reduce using rule 31 (boolterm -> boolterm AND boolfactor .)
        OR              reduce using rule 31 (boolterm -> boolterm AND boolfactor .)


    state 81

        (33) boolfactor -> NOT LPARENT boolexpr . RPARENT
        (29) boolexpr -> boolexpr . OR boolterm

        RPARENT         shift and go to state 87
        OR              shift and go to state 66


    state 82

        (34) boolfactor -> expression RELOP expression .
        (35) expression -> expression . ADDOP term

        AND             reduce using rule 34 (boolfactor -> expression RELOP expression .)
        RPARENT         reduce using rule 34 (boolfactor -> expression RELOP expression .)
        OR              reduce using rule 34 (boolfactor -> expression RELOP expression .)
        ADDOP           shift and go to state 59


    state 83

        (21) while_stmt -> WHILE LPARENT boolexpr RPARENT stmt .

        RBRACE          reduce using rule 21 (while_stmt -> WHILE LPARENT boolexpr RPARENT stmt .)
        ID              reduce using rule 21 (while_stmt -> WHILE LPARENT boolexpr RPARENT stmt .)
        INPUT           reduce using rule 21 (while_stmt -> WHILE LPARENT boolexpr RPARENT stmt .)
        OUTPUT          reduce using rule 21 (while_stmt -> WHILE LPARENT boolexpr RPARENT stmt .)
        IF              reduce using rule 21 (while_stmt -> WHILE LPARENT boolexpr RPARENT stmt .)
        WHILE           reduce using rule 21 (while_stmt -> WHILE LPARENT boolexpr RPARENT stmt .)
        SWITCH          reduce using rule 21 (while_stmt -> WHILE LPARENT boolexpr RPARENT stmt .)
        BREAK           reduce using rule 21 (while_stmt -> WHILE LPARENT boolexpr RPARENT stmt .)
        LBRACE          reduce using rule 21 (while_stmt -> WHILE LPARENT boolexpr RPARENT stmt .)
        ELSE            reduce using rule 21 (while_stmt -> WHILE LPARENT boolexpr RPARENT stmt .)
        DEFAULT         reduce using rule 21 (while_stmt -> WHILE LPARENT boolexpr RPARENT stmt .)
        CASE            reduce using rule 21 (while_stmt -> WHILE LPARENT boolexpr RPARENT stmt .)


    state 84

        (22) switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE . caselist DEFAULT COLONS stmtlist RBRACE
        (23) caselist -> . caselist CASE NUM COLONS stmtlist
        (24) caselist -> . epsilon
        (43) epsilon -> .

        DEFAULT         reduce using rule 43 (epsilon -> .)
        CASE            reduce using rule 43 (epsilon -> .)

        caselist                       shift and go to state 88
        epsilon                        shift and go to state 89

    state 85

        (40) factor -> CAST LPARENT expression RPARENT .

        MULOP           reduce using rule 40 (factor -> CAST LPARENT expression RPARENT .)
        SEMICOLON       reduce using rule 40 (factor -> CAST LPARENT expression RPARENT .)
        ADDOP           reduce using rule 40 (factor -> CAST LPARENT expression RPARENT .)
        RPARENT         reduce using rule 40 (factor -> CAST LPARENT expression RPARENT .)
        RELOP           reduce using rule 40 (factor -> CAST LPARENT expression RPARENT .)
        AND             reduce using rule 40 (factor -> CAST LPARENT expression RPARENT .)
        OR              reduce using rule 40 (factor -> CAST LPARENT expression RPARENT .)


    state 86

        (20) if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE . stmt
        (9) stmt -> . assignment_stmt
        (10) stmt -> . input_stmt
        (11) stmt -> . output_stmt
        (12) stmt -> . if_stmt
        (13) stmt -> . while_stmt
        (14) stmt -> . switch_stmt
        (15) stmt -> . break_stmt
        (16) stmt -> . stmt_block
        (17) assignment_stmt -> . ID ASSIGNMENT expression SEMICOLON
        (18) input_stmt -> . INPUT LPARENT ID RPARENT SEMICOLON
        (19) output_stmt -> . OUTPUT LPARENT expression RPARENT SEMICOLON
        (20) if_stmt -> . IF LPARENT boolexpr RPARENT stmt ELSE stmt
        (21) while_stmt -> . WHILE LPARENT boolexpr RPARENT stmt
        (22) switch_stmt -> . SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE
        (25) break_stmt -> . BREAK SEMICOLON
        (26) stmt_block -> . LBRACE stmtlist RBRACE

        ID              shift and go to state 23
        INPUT           shift and go to state 24
        OUTPUT          shift and go to state 25
        IF              shift and go to state 26
        WHILE           shift and go to state 27
        SWITCH          shift and go to state 28
        BREAK           shift and go to state 29
        LBRACE          shift and go to state 6

        stmt                           shift and go to state 90
        assignment_stmt                shift and go to state 15
        input_stmt                     shift and go to state 16
        output_stmt                    shift and go to state 17
        if_stmt                        shift and go to state 18
        while_stmt                     shift and go to state 19
        switch_stmt                    shift and go to state 20
        break_stmt                     shift and go to state 21
        stmt_block                     shift and go to state 22

    state 87

        (33) boolfactor -> NOT LPARENT boolexpr RPARENT .

        AND             reduce using rule 33 (boolfactor -> NOT LPARENT boolexpr RPARENT .)
        RPARENT         reduce using rule 33 (boolfactor -> NOT LPARENT boolexpr RPARENT .)
        OR              reduce using rule 33 (boolfactor -> NOT LPARENT boolexpr RPARENT .)


    state 88

        (22) switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist . DEFAULT COLONS stmtlist RBRACE
        (23) caselist -> caselist . CASE NUM COLONS stmtlist

        DEFAULT         shift and go to state 91
        CASE            shift and go to state 92


    state 89

        (24) caselist -> epsilon .

        DEFAULT         reduce using rule 24 (caselist -> epsilon .)
        CASE            reduce using rule 24 (caselist -> epsilon .)


    state 90

        (20) if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE stmt .

        RBRACE          reduce using rule 20 (if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE stmt .)
        ID              reduce using rule 20 (if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE stmt .)
        INPUT           reduce using rule 20 (if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE stmt .)
        OUTPUT          reduce using rule 20 (if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE stmt .)
        IF              reduce using rule 20 (if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE stmt .)
        WHILE           reduce using rule 20 (if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE stmt .)
        SWITCH          reduce using rule 20 (if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE stmt .)
        BREAK           reduce using rule 20 (if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE stmt .)
        LBRACE          reduce using rule 20 (if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE stmt .)
        ELSE            reduce using rule 20 (if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE stmt .)
        DEFAULT         reduce using rule 20 (if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE stmt .)
        CASE            reduce using rule 20 (if_stmt -> IF LPARENT boolexpr RPARENT stmt ELSE stmt .)


    state 91

        (22) switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT . COLONS stmtlist RBRACE

        COLONS          shift and go to state 93


    state 92

        (23) caselist -> caselist CASE . NUM COLONS stmtlist

        NUM             shift and go to state 94


    state 93

        (22) switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS . stmtlist RBRACE
        (27) stmtlist -> . stmtlist stmt
        (28) stmtlist -> . epsilon
        (43) epsilon -> .

        RBRACE          reduce using rule 43 (epsilon -> .)
        ID              reduce using rule 43 (epsilon -> .)
        INPUT           reduce using rule 43 (epsilon -> .)
        OUTPUT          reduce using rule 43 (epsilon -> .)
        IF              reduce using rule 43 (epsilon -> .)
        WHILE           reduce using rule 43 (epsilon -> .)
        SWITCH          reduce using rule 43 (epsilon -> .)
        BREAK           reduce using rule 43 (epsilon -> .)
        LBRACE          reduce using rule 43 (epsilon -> .)

        stmtlist                       shift and go to state 95
        epsilon                        shift and go to state 10

    state 94

        (23) caselist -> caselist CASE NUM . COLONS stmtlist

        COLONS          shift and go to state 96


    state 95

        (22) switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist . RBRACE
        (27) stmtlist -> stmtlist . stmt
        (9) stmt -> . assignment_stmt
        (10) stmt -> . input_stmt
        (11) stmt -> . output_stmt
        (12) stmt -> . if_stmt
        (13) stmt -> . while_stmt
        (14) stmt -> . switch_stmt
        (15) stmt -> . break_stmt
        (16) stmt -> . stmt_block
        (17) assignment_stmt -> . ID ASSIGNMENT expression SEMICOLON
        (18) input_stmt -> . INPUT LPARENT ID RPARENT SEMICOLON
        (19) output_stmt -> . OUTPUT LPARENT expression RPARENT SEMICOLON
        (20) if_stmt -> . IF LPARENT boolexpr RPARENT stmt ELSE stmt
        (21) while_stmt -> . WHILE LPARENT boolexpr RPARENT stmt
        (22) switch_stmt -> . SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE
        (25) break_stmt -> . BREAK SEMICOLON
        (26) stmt_block -> . LBRACE stmtlist RBRACE

        RBRACE          shift and go to state 97
        ID              shift and go to state 23
        INPUT           shift and go to state 24
        OUTPUT          shift and go to state 25
        IF              shift and go to state 26
        WHILE           shift and go to state 27
        SWITCH          shift and go to state 28
        BREAK           shift and go to state 29
        LBRACE          shift and go to state 6

        stmt                           shift and go to state 14
        assignment_stmt                shift and go to state 15
        input_stmt                     shift and go to state 16
        output_stmt                    shift and go to state 17
        if_stmt                        shift and go to state 18
        while_stmt                     shift and go to state 19
        switch_stmt                    shift and go to state 20
        break_stmt                     shift and go to state 21
        stmt_block                     shift and go to state 22

    state 96

        (23) caselist -> caselist CASE NUM COLONS . stmtlist
        (27) stmtlist -> . stmtlist stmt
        (28) stmtlist -> . epsilon
        (43) epsilon -> .

        ID              reduce using rule 43 (epsilon -> .)
        INPUT           reduce using rule 43 (epsilon -> .)
        OUTPUT          reduce using rule 43 (epsilon -> .)
        IF              reduce using rule 43 (epsilon -> .)
        WHILE           reduce using rule 43 (epsilon -> .)
        SWITCH          reduce using rule 43 (epsilon -> .)
        BREAK           reduce using rule 43 (epsilon -> .)
        LBRACE          reduce using rule 43 (epsilon -> .)
        DEFAULT         reduce using rule 43 (epsilon -> .)
        CASE            reduce using rule 43 (epsilon -> .)

        stmtlist                       shift and go to state 98
        epsilon                        shift and go to state 10

    state 97

        (22) switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE .

        RBRACE          reduce using rule 22 (switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE .)
        ID              reduce using rule 22 (switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE .)
        INPUT           reduce using rule 22 (switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE .)
        OUTPUT          reduce using rule 22 (switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE .)
        IF              reduce using rule 22 (switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE .)
        WHILE           reduce using rule 22 (switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE .)
        SWITCH          reduce using rule 22 (switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE .)
        BREAK           reduce using rule 22 (switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE .)
        LBRACE          reduce using rule 22 (switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE .)
        ELSE            reduce using rule 22 (switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE .)
        DEFAULT         reduce using rule 22 (switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE .)
        CASE            reduce using rule 22 (switch_stmt -> SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE .)


    state 98

        (23) caselist -> caselist CASE NUM COLONS stmtlist .
        (27) stmtlist -> stmtlist . stmt
        (9) stmt -> . assignment_stmt
        (10) stmt -> . input_stmt
        (11) stmt -> . output_stmt
        (12) stmt -> . if_stmt
        (13) stmt -> . while_stmt
        (14) stmt -> . switch_stmt
        (15) stmt -> . break_stmt
        (16) stmt -> . stmt_block
        (17) assignment_stmt -> . ID ASSIGNMENT expression SEMICOLON
        (18) input_stmt -> . INPUT LPARENT ID RPARENT SEMICOLON
        (19) output_stmt -> . OUTPUT LPARENT expression RPARENT SEMICOLON
        (20) if_stmt -> . IF LPARENT boolexpr RPARENT stmt ELSE stmt
        (21) while_stmt -> . WHILE LPARENT boolexpr RPARENT stmt
        (22) switch_stmt -> . SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE
        (25) break_stmt -> . BREAK SEMICOLON
        (26) stmt_block -> . LBRACE stmtlist RBRACE

        DEFAULT         reduce using rule 23 (caselist -> caselist CASE NUM COLONS stmtlist .)
        CASE            reduce using rule 23 (caselist -> caselist CASE NUM COLONS stmtlist .)
        ID              shift and go to state 23
        INPUT           shift and go to state 24
        OUTPUT          shift and go to state 25
        IF              shift and go to state 26
        WHILE           shift and go to state 27
        SWITCH          shift and go to state 28
        BREAK           shift and go to state 29
        LBRACE          shift and go to state 6

        stmt                           shift and go to state 14
        assignment_stmt                shift and go to state 15
        input_stmt                     shift and go to state 16
        output_stmt                    shift and go to state 17
        if_stmt                        shift and go to state 18
        while_stmt                     shift and go to state 19
        switch_stmt                    shift and go to state 20
        break_stmt                     shift and go to state 21
        stmt_block                     shift and go to state 22
</details>

## Implementation
In quad code, booleans are integers, where True means int!=0, and False means int==0
