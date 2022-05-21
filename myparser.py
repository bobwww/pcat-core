import ply.lex as lex

#   Reserved keywords
ACTIONS = (
    'alert', 'deny', 'pass'
)
PROTOS = (
    'tcp', 'udp', 'http'
)


#   Tokens
tokens = (
    'ACTION', 'PROTO', 'HEADER', 'QUOTES', 'EOL', 
    'RCBRACKET', 'LCBRACKET', 'DELIMETER', 
    'FUNC', 'COMMENT', 'NUMBER', 'RANGE', 'OR', 'AND'
)

#   States
#   initial - starting state
#   expr - state that is used for tokenizing expressions.
#   Expressions are declarations of values. They may contain certain keywords
#   defined by the parser. They may also contain strings.
#   For example: contains "hello, world" or len > 10
states = (
    ('expr', 'exclusive'),  # State for evaluating expression for header, e.g. regex
)


t_LCBRACKET = r'\{'
t_RCBRACKET = r'\}'

#   Ignore tabs and spaces
#   Note: only relevant in initial state
t_ignore = ' \t'


#   Comments are prefixed with '#' till the end of line
def t_COMMENT(t):
    r'\#.*'
    pass


def t_name(t):
    r'[A-Za-z_][A-Za-z0-9_]*'

    t.value = t.value.lower()
    if t.value in ACTIONS:
        t.type = 'ACTION'
    elif t.value in PROTOS:
        t.type = 'PROTO'
    else:
        t.type = 'HEADER'

    return t


def t_newline(t):
    r'\n+'
    #t.lexer.lineno += t.value.count('\n')
    t.lexer.lineno += len(t.value)


def t_error(t):
    print('Illegal character: %s' % t.value[0])
    t.lexer.skip(1)

# Expr state tokenizers
def t_begin_expr(t):
    r'\:'
    t.lexer.push_state('expr')

t_expr_ignore = ' \t'
t_expr_RANGE = r'\-'
t_expr_OR = r'or'
t_expr_AND = r'and'

def t_expr_FUNC(t):
    r'[A-Za-z_]+'
    t.value = t.value.lower()
    return t

def t_expr_QUOTES(t):
    r'"[\S\s]*"|\'[\S\s]*\''
    t.value = t.value[1:-1]
    return t

def t_expr_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_expr_EOL(t):
    r'\;'
    t.lexer.pop_state()
    return t

def t_expr_error(t):
    print('Illegal character in expr: %s' % t.value[0])
    t.lexer.skip(1)


#   Building the lexer

lexer = lex.lex()

s=r'''
alert {
     tcp {
        dport: 80;
        sport: "http";
    }
}
'''

# s = ':1;'
#Test input
lexer.input(s)

for tok in lexer:
    print(tok)

import ply.yacc as yacc
from datatypes import Head, Chain, ExceptChain, Rule, Section

"""
Grammar rules:


head    :   ACTION LCBRACKET chain RCBRACKET
        |	head ACTION LCBRACKET chain RCBRACKET

chain	:	PROTO LCBRACKET rule RCBRACKET
        |	chain PROTO LCBRACKET rule RCBRACKET
    
rule	:	section EOL
        |	rule section EOL

section :	HEADER expr

expr	:	QUOTES
        |	NUMBER


"""

def p_head(p):
    r'''
    head    :   ACTION LCBRACKET chain RCBRACKET
		    |	head ACTION LCBRACKET chain RCBRACKET
    '''
    if len(p) == 5:
        p[0] = [Chain(p[3], p[1]),]
    elif len(p) == 6:
        p[0] = p[1] [Chain(p[4, p[2]])]
    
def p_chain(p):
    r'''
    chain	:	PROTO LCBRACKET rule RCBRACKET
		    |	chain PROTO LCBRACKET rule RCBRACKET
    '''
    if len(p) == 5:
        p[0] = [Rule(p[3], p[1]),]
    elif len(p) == 6:
        p[0] = p[1]+ [Rule(p[4], p[2])]


def p_rule(p):
    r'''
    rule	:	section EOL
		    |	rule section EOL
    '''
    if len(p) == 3:
        p[0] = [p[1],]
    elif len(p) == 4:
        p[0] = p[1] + [p[2]]

def p_section(p):
    r'''
    section :	HEADER expr
    '''
    p[0] = Section(p[1], p[2])

def p_expr(p):
    r'''
    expr	:	QUOTES
		    |	NUMBER
    '''
    p[0] = p[1]

def p_error(p):
    if p:
         print("Syntax error at token", p.type, "\nAt position: ", (p.lexpos, p.lineno), "\nIllegal char:", p.value)
    else:
         print("Syntax error at EOF")


parser = yacc.yacc()
result = parser.parse(s)
result = Head(result, [])