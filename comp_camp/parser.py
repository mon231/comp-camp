from sys import stderr
from ply.yacc import GrammarError, PlyLogger, yacc

from .cpl_types import *
from .tokenizer import tokens, lexer


def p_program(p):
    '''program : declarations stmt_block'''
    p[0] = Program(declarations=p[1], statement_block=p[2])


def p_declarations(p):
    '''declarations : declarations declaration
                    | epsilon'''

    if len(p) == 3:
        p[1].add_declaration(p[2])
        p[0] = p[1]
    else:
        p[0] = Declarations()


def p_declaration(p):
    '''declaration : idlist COLONS type SEMICOLON'''
    p[0] = Declaration(p[1], p[3])


def p_type(p):
    '''type : INT
            | FLOAT'''
    p[0] = p[1]


def p_idlist(p):
    '''idlist : idlist COMMA ID
              | ID'''

    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_stmt(p):
    '''stmt : assignment_stmt
            | input_stmt
            | output_stmt
            | if_stmt
            | while_stmt
            | switch_stmt
            | break_stmt
            | stmt_block'''

    p[0] = p[1]


def p_assignment_stmt(p):
    '''assignment_stmt : ID ASSIGNMENT expression SEMICOLON'''
    p[0] = AssignmentStatement(p[1], p[3])


def p_input_stmt(p):
    '''input_stmt : INPUT LPARENT ID RPARENT SEMICOLON'''
    p[0] = InputStatement(p[3])


def p_output_stmt(p):
    '''output_stmt : OUTPUT LPARENT expression RPARENT SEMICOLON'''
    p[0] = OutputStatement(p[3])


def p_if_stmt(p):
    '''if_stmt : IF LPARENT boolexpr RPARENT stmt ELSE stmt'''
    p[0] = IFStatement(p[3], p[5], p[7])


def p_while_stmt(p):
    '''while_stmt : WHILE LPARENT boolexpr RPARENT stmt'''
    p[0] = WhileStatement(p[3], p[5])


def p_switch_stmt(p):
    '''switch_stmt : SWITCH LPARENT expression RPARENT LBRACE caselist DEFAULT COLONS stmtlist RBRACE'''
    p[0] = SwitchStatement(expression=p[3], conditional_cases=p[6], default_case=DefaultCase(statements=p[9]))


def p_caselist(p):
    '''caselist : caselist CASE NUM COLONS stmtlist
                | epsilon'''

    if len(p) == 6:
        try:
            p[3] = int(p[3])
        except:
            raise GrammarError('Invalid number-value for case (must be integer)')

        p[1].add_case(ConditionalCase(number=p[3], statements=p[5]))
        p[0] = p[1]
    else:
        p[0] = ConditionalCases([])


def p_break_stmt(p):
    '''break_stmt : BREAK SEMICOLON'''
    p[0] = BreakStatement()


def p_stmt_block(p):
    '''stmt_block : LBRACE stmtlist RBRACE'''
    p[0] = StatementBlock(p[2])


def p_stmtlist(p):
    '''stmtlist : stmtlist stmt
                | epsilon'''

    if len(p) == 3:
        p[1].add_statement(p[2])
        p[0] = p[1]
    else:
        p[0] = StatementList()


def p_boolexpr(p):
    '''boolexpr : boolexpr OR boolterm
                | boolterm'''

    if len(p) == 4:
        p[0] = BooleanExpression(value=BooleanOperationOR(p[1], p[3]))
    else:
        p[0] = BooleanExpression(value=p[1])


def p_boolterm(p):
    '''boolterm : boolterm AND boolfactor
                | boolfactor'''

    if len(p) == 4:
        p[0] = BooleanTerm(value=BooleanOperationAND(p[1], p[3]))
    else:
        p[0] = BooleanTerm(value=p[1])


def p_boolfactor(p):
    '''boolfactor : NOT LPARENT boolexpr RPARENT
                  | expression RELOP expression'''

    if len(p) == 5:
        p[0] = BooleanFactor(value=BooleanOperationNOT(p[3]))
    else:
        match p[2]:
            case '<=':
                p[0] = BooleanOperationOR(
                    BooleanRelationOperation(left_expression=p[1], right_expression=p[3], relation_operation='<'),
                    BooleanRelationOperation(left_expression=p[1], right_expression=p[3], relation_operation='==')
                )

            case '>=':
                p[0] = BooleanOperationOR(
                    BooleanRelationOperation(left_expression=p[1], right_expression=p[3], relation_operation='>'),
                    BooleanRelationOperation(left_expression=p[1], right_expression=p[3], relation_operation='==')
                )

            case _:
                p[0] = BooleanRelationOperation(left_expression=p[1], right_expression=p[3], relation_operation=p[2])


def p_expression(p):
    '''expression : expression ADDOP term
                  | term'''

    if len(p) == 4:
        match p[2]:
            case '-':
                p[0] = NumericExpression(value=NumericOperationSUB(p[1], p[3]))

            case '+':
                p[0] = NumericExpression(value=NumericOperationADD(p[1], p[3]))
    else:
        p[0] = NumericExpression(value=p[1])


def p_term(p):
    '''term : term MULOP factor
            | factor'''

    if len(p) == 4:
        match p[2]:
            case '*':
                p[0] = NumericTerm(value=NumericOperationMUL(p[1], p[3]))

            case '/':
                p[0] = NumericTerm(value=NumericOperationDIV(p[1], p[3]))
    else:
        p[0] = NumericTerm(value=p[1])


def p_factor(p):
    '''factor : LPARENT expression RPARENT
              | CAST LPARENT expression RPARENT
              | ID
              | NUM'''

    match len(p):
        case 2:
            p[0] = NumericFactor(p[1])

        case 4:
            p[0] = p[2]

        case 5:
            p[0] = NumericOperationCast(p[3], p[1].split('<')[1].split('>')[0])


def p_epsilon(p):
    'epsilon :'
    pass


def p_error(p):
    print(f'Unexpected parsing error occurred at line {p.lineno}!', file=stderr)


# NOTE: Build the parser, log into stderr
parser = yacc(errorlog=PlyLogger(stderr), write_tables=False, debug=False)
