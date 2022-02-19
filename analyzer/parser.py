from datatypes import *

def parse(s):

    tmp = s.split()

def parse_expression(x):
    s = x.split()


def parse_section(x):
    field, expr = x.split(':', maxsplit=1)
    expr = expr[:expr.find(';')]
    expr = expr.strip()
    expr = parse_expression(expr)
    return Section(field, expr)
    