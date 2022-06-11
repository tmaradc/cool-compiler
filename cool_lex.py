# ------------------------------------------------------------
# cool_lex.py
#
# tokenizer for the cool language
# ------------------------------------------------------------

import ply.lex as lex

## Tokens

tokens = [ 
    'STRING',
    'PLUS','MINUS','TIMES','DIVIDE',
    'COLON', 'ASSIGNMENT', 'ARROW', 'DOT', 'COMMA', 'SEMICOLON', 'AT',
    'TILDE', 'LESSTHAN', 'LESSOREQUAL', 'EQUALS',
    'LBRACKET','RBRACKET','LPAREN','RPAREN',
    'TRUE', 'FALSE',
    'ID', 'TYPE', 'SELF', 'INTEGER', 'WHITE_SPACE'
]

reserved_words = {
    "class": "CLASS",
    "else": "ELSE",
    "fi": "FI",
    "if": "IF",
    "in": "IN",
    "inherits": "INHERITS",
    "isvoid": "ISVOID",
    "let": "LET",
    "loop": "LOOP",
    "pool": "POOL",
    "then": "THEN",
    "while": "WHILE",
    "case": "CASE",
    "esac": "ESAC",
    "new": "NEW",
    "of": "OF",
    "not": "NOT"
}

tokens = tokens + list(reserved_words.values())

## Regex for tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'

t_COLON  = r':'
t_ASSIGNMENT = r'<-'
t_ARROW = r'=>'
t_DOT = r'\.' 
t_COMMA = r','
t_SEMICOLON = r';'
t_AT = r'@'

t_TILDE = r'~'
t_LESSTHAN = r'<'
t_LESSOREQUAL = r'<='
t_EQUALS  = r'='

t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_COMMENT(t):
    r'\(\*(.|\n)*?\*\)'
    pass

def t_COMMENT_INLINE(t):
    r'--.*\n?'
    pass

def t_STRING(t):
    r'"[^"\0\n]*((\\\n)|[^"\0\n])*"'
    t.type = "STRING"
    return t

def t_TRUE(t):
    r't(r|R)(u|U)(e|E)'
    t.type = "TRUE"
    return t

def t_FALSE(t):
    r'f(a|A)(l|L)(s|S)(e|E)'
    t.type = "FALSE"
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    if t.value=="SELF_TYPE":
        t.type = "TYPE"
    elif t.value=="self":
        t.type = "SELF"
    elif t.value.lower() in reserved_words:
        t.type = reserved_words[t.value.lower()]
    elif t.value[0].isupper():
        t.type = "TYPE"
    else: 
        t.type = "ID"
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_WHITE_SPACE(t):
    r'\f|\r|\t|\v|\ ' 
    pass

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
