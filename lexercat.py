import ply.lex as lex

#   Reserved keywords
ACTIONS = (
    'allow', 'sallow', 'deny', 'sdeny'
)
PROTOS = (
    'tcp', 'udp', 'http', 'ftp', 'icmp', 'dns'
)


#   Tokens
tokens = (
    'ACTION', 'PROTO', 'HEADER', 'QUOTES', 'EOL', 
    'RCBRACKET', 'LCBRACKET', 'DELIMETER', 'ALERT',
    'FUNC', 'COMMENT', 'NUMBER', 'RANGE', 'OR', 'AND',
     'NOT'
)


#   States
#   initial - starting state
#   expr - state that is used for tokenizing inside expressions
#   Expressions are conditions that must be met by the field value.. They may contain certain keywords
#   defined by the parser. They may also contain strings.
#   For example: contains "hello, world" or len > 10
states = (
    ('expr', 'exclusive'),
)

# Initial state token definitions
#
#

t_LCBRACKET = r'\{'
t_RCBRACKET = r'\}'

t_ignore = ' \t'    # Ignore tabs and spaces

# Counts newlines, for error information/debugging.
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Handles invalid characters by printing and skipping to next char
def t_error(t):
    print('Illegal character: %s' % t.value[0])
    t.lexer.skip(1)

#   Comments are prefixed with '#' till the end of line
def t_COMMENT(t):
    r'\#.*'
    pass

#   Any names that appear will be handled here.
def t_name(t):
    r'[A-Za-z_][A-Za-z0-9_]*'

    t.value = t.value.lower()
    if t.value in ACTIONS:
        t.type = 'ACTION'
    elif t.value in PROTOS:
        t.type = 'PROTO'
    elif t.value == 'alert':
        t.type = 'ALERT'
    else:
        t.type = 'HEADER'

    return t


# Expr state token definitions
#
#

# Expr state begins once ':' is encountered in input
def t_begin_expr(t):
    r'\:'
    t.lexer.push_state('expr')

t_expr_ignore = ' \t'

def t_expr_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_expr_RANGE = r'\-'

def t_expr_OR(t):
    r'or'
    return t

def t_expr_AND(t):
    r'and'
    return t

def t_expr_NOT(t):
    r'not'
    return t

def t_expr_FUNC(t):
    r'[A-Za-z_]+'
    t.value = t.value.lower()
    return t

def t_expr_QUOTES(t):
    r'"[\S\s]*?"|\'[\S\s]*?\''
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

# Builds the lexer. Necessary for parser
lexer = lex.lex()