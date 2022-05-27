import ply.yacc as yacc
from analyzer.lexercat import tokens
from analyzer.datatypes import Head, Chain, Rule, Section
from analyzer.expression import *

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
        p[0] = [Chain(p[4], p[2], alert=True),]
    elif len(p) == 7:
        p[0] = p[1]+[Chain(p[5], p[3], alert=True)]


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


def p_expr_quotes(p):
    r'''
    expr	:	QUOTES
            |   FUNC QUOTES
    '''
    if len(p) == 2:
        p[0] = StrExpr(p[1])
    elif len(p) == 3:
        p[0] = StrExpr(p[2], p[1])

def p_expr_number(p):
    '''     
    expr    :	NUMBER
		    |	NUMBER RANGE
		    |	RANGE NUMBER
		    |	NUMBER RANGE NUMBER
    '''
    if len(p) == 2:
        p[0] = IntExpr(min=p[1], max=p[1])
    elif len(p) == 3:
        if isinstance(p[1], int):
            p[0] = IntExpr(min=p[1])
        elif isinstance(p[2], int):
            p[0] = IntExpr(min=None, max=p[2])
    elif len(p) == 4:
        p[0] = IntExpr(min=p[1], max=p[3])

def p_expr_or(p):
    '''
    expr    :   expr OR expr
    '''
    p[0] = OrExpr(p[1], [3])

def p_expr_and(p):
    '''
    expr    :   expr AND expr
    '''
    p[0] = AndExpr(p[1], [3])

def p_expr_not(p):
    '''
    expr    :   NOT expr
    '''
    p[0] = NotExpr(p[2])


def p_error(p):
    if p:
         print("Syntax error at token:", p.type, "\nAt position: ", (p.lexpos, p.lineno), "\nIllegal char(s):", p.value)
    else:
         print("ParserError: End-Of-File")

parser = yacc.yacc()

def parse(s):
    result = parser.parse(s)
    result = Head(result)
    return result