from sys import stderr
from pathlib import Path
from typing import Optional
from argparse import ArgumentParser
from ply.lex import lex, Lexer, LexToken


CPL_TYPED_TOKENS = {
    'keywords': [
        'BREAK', 'CASE', 'DEFAULT', 'ELSE', 'FLOAT', 'IF', 'INPUT', 'INT', 'OUTPUT', 'SWITCH', 'WHILE'
    ],
    'symbols': [
        'LPARENT', 'RPARENT', 'LBRACE', 'RBRACE', 'COMMA', 'COLONS', 'SEMICOLON', 'ASSIGNMENT'
    ],
    'operators': [
        'RELOP', 'ADDOP', 'MULOP', 'OR', 'AND', 'NOT', 'CAST'
    ],
    'extra': [
        'ID', 'NUM'
    ]
}

LT = r'<'
GT = r'>'
LE = r'<='
GE = r'>='

EQ = r'=='
NE = r'!='

DEVIDE = r'/'
MULTIPLY = r'\*'

PLUS = r'\+'
MINUS = r'-'

DIGIT = r'[0-9]'
LETTER = r'[a-zA-Z]'
LETTER_OR_DIGIT = r'[0-9a-zA-Z]'

t_ignore = ' \t'
tokens = [token for token_list in CPL_TYPED_TOKENS.values() for token in token_list]

# NOTE: operators
t_OR = r'\|\|'
t_AND = r'\&\&'
t_ADDOP = rf'{PLUS}|{MINUS}'
t_MULOP = rf'{MULTIPLY}|{DEVIDE}'


def t_CAST(t: LexToken):
    r'static_cast<(int|float)>'
    return t


def t_OPERATORS(t: LexToken):
    '==|!=|>=|<=|<|>|!|='

    if t.value == '!':
        t.type = 'NOT'
    elif t.value == '=':
        t.type = 'ASSIGNMENT'
    else:
        t.type = 'RELOP'

    return t

# NOTE: symbols
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = ','
t_COLONS = ':'
t_SEMICOLON = ';'

# NOTE: extra tokens
t_NUM = rf'{DIGIT}+(?:\.{DIGIT}*)?'

def t_ID(t: LexToken):
    '[a-zA-Z][a-zA-Z0-9]*'

    if t.value.upper() in CPL_TYPED_TOKENS['keywords']:
        t.type = t.value.upper()

    return t


# NOTE: global rules
def t_count_newlines(t: LexToken):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


def t_ignore_comments(t: LexToken):
    r'\/\*[^(/*)]*\*\/'

    if not ((t.value.count('/*') == 1) and (t.value.count('*/') == 1)):
        raise SyntaxError(f'Invalid comment at line {t.lexer.lineno}')


def t_error(t: LexToken):
    raise SyntaxError(f'Illegal character {t.value[0]!r} at line {t.lexer.lineno}')


def get_next_token(lexer: Lexer) -> Optional[LexToken]:
    return lexer.token()


def find_token_category(token_type: str) -> str:
    for token_category, category_types in CPL_TYPED_TOKENS.items():
        if token_type in category_types:
            return token_category

    raise RuntimeError('Unexpected token category')


def create_token_stream(cpl_code: str):
    try:
        lexer: Lexer = lex()
        lexer.input(cpl_code)

        while token := get_next_token(lexer):
            yield token
    except Exception as e:
        print(e, file=stderr)
        raise
