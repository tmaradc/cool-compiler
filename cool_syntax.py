import sys
from cool_lex import tokens
import ply.yacc as yacc

class Node:
    def __init__(self,type,children=None,leaf=None, ):
          self.type = type
          if children:
               self.children = children
          else:
               self.children = [ ]
          self.leaf = leaf

    def __str__(self, level=0):
        ret = "\t"*level+self.type+"/"+str(self.leaf)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret


precedence = (
    ('right','ASSIGNMENT'),
    ('right','NOT'),
    ('nonassoc','LESSOREQUAL','LESSTHAN','EQUALS'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','ISVOID'),
    ('right','TILDE'),
    ('right','AT'),
    ('left','DOT'),
)

ID = {}
TYPE = set()



## PROGRAM --------------------------------------------------------------------
def p_program(p):
    '''program : classes '''
    p[0] = Node("program", children=p[1], leaf="program")

def p_classes(p):
    '''classes : classes class SEMICOLON
               | class SEMICOLON '''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


## CLASS --------------------------------------------------------------------
def p_class(p):
    '''class : CLASS TYPE LBRACKET features_opt RBRACKET '''
    TYPE.add(p[2])
    p[0] = Node("class", children=p[4], leaf=p[2])

def p_class_inherits(p):
    '''class : CLASS TYPE INHERITS TYPE LBRACKET features_opt RBRACKET'''
    TYPE.add(p[2])
    # Verifico se o tipo da classe pai existe no programa??
    p[0] = Node("class_" + p[4], children=p[6], leaf=p[2])

def p_features_opt(p):
    '''features_opt : features
                    | empty '''
    p[0] = [] if p.slice[1].type == "empty" else p[1]

def p_features(p):
    ''' features : features feature SEMICOLON
                 | feature SEMICOLON '''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


## FEATURE --------------------------------------------------------------------
def p_feature_method(p):
    ''' feature : ID LPAREN formal_params RPAREN COLON TYPE LBRACKET expression RBRACKET '''
    p[0] = Node("feature_method_" + p[6], children=p[3]+[p[8]], leaf=p[1])

def p_feature_method_no_formals(p):
    ''' feature : ID LPAREN RPAREN COLON TYPE LBRACKET expression RBRACKET '''
    p[0] = Node("feature_method_"+ p[5], children=[p[7]], leaf=p[1])

def p_feature_attr_initialized(p):
    ''' feature : ID COLON TYPE ASSIGNMENT expression '''
    p[0] = Node("feature_attr_" + p[3], children=[p[5]], leaf=p[1])

def p_feature_attr(p):
    ''' feature : ID COLON TYPE '''
    p[0] = Node("feature_attr_" + p[3], leaf=p[1])

def p_formal_params(p):
    ''' formal_params : formal_params COMMA formal
                      | formal '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


## FORMAL --------------------------------------------------------------------
def p_formal(p):
    ''' formal : ID COLON TYPE '''
    p[0] = Node("formal_"+p[3], leaf=p[1])


## EXPR --------------------------------------------------------------------
def p_expression_assignent(p):
    'expression : ID ASSIGNMENT expression'
    p[0] = Node("assignment", children=[p[3]], leaf=p[1])

def p_expression_id(p):
    ''' expression : ID '''
    try:
        p[0] = Node("ID", leaf=p[1])
        ID[p[1]]
    except LookupError:
        print("Undefined id '%s'" % p[1])

def p_expression_integer(p):
    ''' expression : INTEGER '''
    p[0] = Node("integer", leaf=p[1])

def p_expression_string(p):
    ''' expression : STRING '''
    p[0] = Node("string", leaf=p[1])

def p_expression_true(p):
    ''' expression : TRUE '''
    p[0] = Node("true", leaf=p[1])

def p_expression_false(p):
    ''' expression : FALSE '''
    p[0] = Node("false", leaf=p[1])

def p_expression_self(p):
    ''' expression : SELF '''
    p[0] = Node("self", leaf=p[1])


### { block }
def p_expression_block(p):
    ''' expression : LBRACKET block_expr RBRACKET '''
    p[0] = Node("block", children=p[2], leaf="block")

def p_block_expr(p):
    ''' block_expr : block_expr expression SEMICOLON
                   | expression SEMICOLON'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


### (expr).ID(args) - ID(args) - expr@TYPE.ID(args)
def p_expression_access(p):
    ''' expression : expression DOT ID LPAREN arguments_opt RPAREN '''
    p[0] = Node("expr_method_access", children=[p[1]] + p[5], leaf=p[3])

def p_arguments_opt(p):
    ''' arguments_opt : arguments
                      | empty '''
    p[0] = [] if p.slice[1].type == "empty" else p[1]

def p_arguments(p):
    ''' arguments : arguments COMMA expression
                  | expression '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_expression_access_at_type(p):
    ''' expression : expression AT TYPE DOT ID LPAREN arguments_opt RPAREN '''
    p[0] = Node("expr_at_method_access", children=[p[1], p[2], p[3]] + p[7], leaf=p[5])

def p_expression_self_dispatch(p):
    ''' expression : ID LPAREN arguments_opt RPAREN '''
    p[0] = Node("self_access", children=p[3], leaf=p[1])


### Math
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = Node("binop", children=[p[1],p[3]], leaf=p[2])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


### Comparison
def p_expression_compare(p):
    '''expression : expression LESSTHAN expression
                  | expression LESSOREQUAL expression
                  | expression EQUALS expression'''
    p[0] = Node("compare", children=[p[1],p[3]], leaf=p[2])


### IF
def p_expression_if(p):
    ''' expression : IF expression THEN expression ELSE expression FI '''
    p[0] = Node("condition", children=[p[2], p[4], p[6]], leaf="IF")


### While
def p_expression_while(p):
    ''' expression : WHILE expression LOOP expression POOL '''
    p[0] = Node("loop", children=[p[2], p[4]], leaf="while")


### Sufix
def p_expression_new(p):
    '''expression : NEW TYPE'''
    p[0] = Node("new", children=[p[2]], leaf=p[1])

def p_expression_isvoid(p):
    '''expression : ISVOID expression'''
    p[0] = Node("isvoid", children=[p[2]], leaf=p[1])

def p_expression_tilde(p):
    '''expression : TILDE expression'''
    p[0] = Node("tilde", children=[p[2]], leaf=p[1])

def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = Node("not", children=[p[2]], leaf=p[1])


### CASE
def p_expression_case(p):
    ''' expression : CASE expression OF actions ESAC '''
    p[0] = Node("case", children=[p[2]] + p[4], leaf="case")

def p_actions(p):
    ''' actions : actions action
                | action '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_action_expr(p):
    ''' action : ID COLON TYPE ARROW expression SEMICOLON '''
    p[0] = Node("case_action_" + p[3], children=[p[5]], leaf=p[1])




def p_empty(p):
    ''' empty : '''
    p[0] = None

def p_error(p):
    print("Syntax error at '%s'" % p.value)



arq_name = sys.argv[1]
f = open(arq_name, "r")

parser = yacc.yacc()
root = parser.parse(f.read())

print(root)
