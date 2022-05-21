import ply.yacc as yacc
from lexercat import tokens
from datatypes import Head, Chain, Rule, Section

"""
Grammar rules: (Not updated)


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
        p[0] = p[1]+[Chain(p[4], p[2])]

def p_head_with_alert(p):
    r'''
    head    :   ALERT ACTION LCBRACKET chain RCBRACKET
		    |	head ALERT ACTION LCBRACKET chain RCBRACKET
    '''
    if len(p) == 6:
        p[0] = [Chain(p[4], p[1], alert=True),]
    elif len(p) == 7:
        p[0] = p[1]+[Chain(p[5], p[2], alert=True)]


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
         print("Syntax error at token:", p.type, "\nAt position: ", (p.lexpos, p.lineno), "\nIllegal char:", p.value)
    else:
         print("Syntax error: EOF")

parser = yacc.yacc()

def parse(s):
    result = parser.parse(s)
    result = Head(result)
    return result