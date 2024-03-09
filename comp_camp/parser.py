import ply.yacc
from .tokenizer import tokens, lexer


def p_program(p):
    '''program : declarations stmt_block'''
    p[0] = ('program', p[1], p[2])


def p_declarations(p):
    '''declarations : declarations declaration
                    | epsilon'''

    if len(p) == 3:
        p[0] = ('declarations', p[1], p[2])
    else:
        p[0] = ('declarations',)


def p_declaration(p):
    '''declaration : idlist COLONS type SEMICOLON'''
    p[0] = ('declaration', p[1], p[3])


def p_type(p):
    '''type : INT
            | FLOAT'''
    p[0] = ('type', p[1])


def p_idlist(p):
    '''idlist : idlist COMMA ID
              | ID'''

    if len(p) == 4:
        p[0] = ('idlist', p[1], p[3])
    else:
        p[0] = ('idlist', p[1])


def p_stmt(p):
    '''stmt : assignment_stmt
            | input_stmt
            | output_stmt
            | if_stmt
            | while_stmt
            | switch_stmt
            | break_stmt
            | stmt_block'''

    p[0] = ('stmt', p[1])


def p_assignment_stmt(p):
    '''assignment_stmt : ID ASSIGNMENT expression SEMICOLON'''
    p[0] = ('assignment_stmt', p[1], p[3])


def p_input_stmt(p):
    '''input_stmt : INPUT LPARENT ID RPARENT SEMICOLON'''
    p[0] = ('input_stmt', p[3])


def p_output_stmt(p):
    '''output_stmt : OUTPUT LPARENT expression RPARENT SEMICOLON'''
    p[0] = ('output_stmt', p[3])


def p_if_stmt(p):
    '''if_stmt : IF LPARENT boolexpr RPARENT stmt ELSE stmt'''
    p[0] = ('if_stmt', p[3], p[5], p[7])


def p_while_stmt(p):
    '''while_stmt : WHILE LPARENT boolexpr RPARENT stmt'''
    p[0] = ('while_stmt', p[3], p[5])


def p_switch_stmt(p):
    '''switch_stmt : SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE'''
    p[0] = ('switch_stmt', p[3], p[6], p[9])


def p_caselist(p):
    '''caselist : caselist CASE NUM COLONS stmtlist
                | epsilon'''

    if len(p) == 6:
        p[0] = ('caselist', p[1], p[3], p[5])
    else:
        p[0] = ('caselist',)


def p_break_stmt(p):
    '''break_stmt : BREAK SEMICOLON'''
    p[0] = ('break_stmt',)


def p_stmt_block(p):
    '''stmt_block : LBRACE stmtlist RBRACE'''
    p[0] = ('stmt_block', p[2])


def p_stmtlist(p):
    '''stmtlist : stmtlist stmt
                | epsilon'''

    if len(p) == 3:
        p[0] = ('stmtlist', p[1], p[2])
    else:
        p[0] = ('stmtlist',)


def p_boolexpr(p):
    '''boolexpr : boolexpr OR boolterm
                | boolterm'''

    if len(p) == 4:
        p[0] = ('boolexpr', p[1], p[2], p[3])
    else:
        p[0] = ('boolexpr', p[1])


def p_boolterm(p):
    '''boolterm : boolterm AND boolfactor
                | boolfactor'''

    if len(p) == 4:
        p[0] = ('boolterm', p[1], p[2], p[3])
    else:
        p[0] = ('boolterm', p[1])


def p_boolfactor(p):
    '''boolfactor : NOT LPARENT boolexpr RPARENT
                  | expression RELOP expression'''

    if len(p) == 5:
        p[0] = ('boolfactor', p[1], p[3])
    else:
        # NOTE: subtree root is RELOP

        #          <=
        #         /  \
        #        /    \
        #       /      \
        # expression   expression

        p[0] = ('boolfactor', p[2], p[1], p[3])


def p_expression(p):
    '''expression : expression ADDOP term
                  | term'''
    if len(p) == 4:
        p[0] = ('expression', p[2], p[1], p[3])
    else:
        p[0] = ('expression', p[1])


def p_term(p):
    '''term : term MULOP factor
            | factor'''

    if len(p) == 4:
        p[0] = ('term', p[2], p[1], p[3])
    else:
        p[0] = ('term', p[1])


def p_factor(p):
    '''factor : LPARENT expression RPARENT
              | CAST LPARENT expression RPARENT
              | ID
              | NUM'''

    match len(p):
        case 2:
            p[0] = ('factor', p[1])

        case 4:
            p[0] = ('factor', p[2])

        case 5:
            p[0] = ('factor', p[1], p[3])


def p_epsilon(p):
    'epsilon :'
    pass


# NOTE: Build the parser
parser = ply.yacc.yacc()