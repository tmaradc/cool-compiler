import sys
from cool_lex import tokens
from cool_semantic import *
import ply.yacc as yacc

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


## PROGRAM --------------------------------------------------------------------
def p_program(p):
    '''program : classes '''
    p[0] = Program(classes=p[1])

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
    p[0] = Class(name=p[2], features=p[4])

def p_class_inherits(p):
    '''class : CLASS TYPE INHERITS TYPE LBRACKET features_opt RBRACKET'''
    # Verifico se o tipo da classe pai existe no programa??
    p[0] = Class(name=p[2], features=p[6], inherits=p[4])

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
    p[0] = FeatureMethod(name=p[1], return_type=p[6], expression=p[8], formal_params=p[3])

def p_feature_method_no_formals(p):
    ''' feature : ID LPAREN RPAREN COLON TYPE LBRACKET expression RBRACKET '''
    p[0] = FeatureMethod(name=p[1], return_type=p[5], expression=p[7])

def p_feature_attr_initialized(p):
    ''' feature : ID COLON TYPE ASSIGNMENT expression '''
    p[0] = FeatureAttr(name=p[1], type=p[3], init=p[5])

def p_feature_attr(p):
    ''' feature : ID COLON TYPE '''
    p[0] = FeatureAttr(name=p[1], type=p[3])

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
    p[0] = Formal(name=p[1], type=p[3])


## EXPR --------------------------------------------------------------------
def p_expression_assignment(p):
    'expression : ID ASSIGNMENT expression'
    p[0] = Assignment(ID=p[1], expression=p[3])

def p_expression_id(p):
    ''' expression : ID '''
    p[0] = ID(name=p[1])

def p_expression_integer(p):
    ''' expression : INTEGER '''
    p[0] = Integer(value=p[1])

def p_expression_string(p):
    ''' expression : STRING '''
    p[0] = String(value=p[1])

def p_expression_true(p):
    ''' expression : TRUE '''
    p[0] = Boolean(value=p[1])

def p_expression_false(p):
    ''' expression : FALSE '''
    p[0] = Boolean(value=p[1])

def p_expression_self(p):
    ''' expression : SELF '''
    p[0] = Self()


### { block }
def p_expression_block(p):
    ''' expression : LBRACKET block_expr RBRACKET '''
    p[0] = Block(expressions=p[2])

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
    p[0] = MethodAccess(instance=p[1], method=p[3], arguments=p[5])

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
    p[0] = AtMethodAccess(instance=p[1], type=p[3], method=p[5], arguments=p[7])

def p_expression_self_dispatch(p):
    ''' expression : ID LPAREN arguments_opt RPAREN '''
    p[0] = SelfMethodAccess(method=p[1], arguments=p[3])


### Math
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = MathBinop(operation=p[2], expression_left=p[1], expression_right=p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


### Comparison
def p_expression_compare(p):
    '''expression : expression LESSTHAN expression
                  | expression LESSOREQUAL expression
                  | expression EQUALS expression'''
    p[0] = Comparison(operation=p[2], expression_left=p[1], expression_right=p[3])


### IF
def p_expression_if(p):
    ''' expression : IF expression THEN expression ELSE expression FI '''
    p[0] = IF(condition=p[2], condition_true=p[4], condition_false=p[6])


### While
def p_expression_while(p):
    ''' expression : WHILE expression LOOP expression POOL '''
    p[0] = While(condition=p[2], body=p[4])


### Sufix
def p_expression_new(p):
    '''expression : NEW TYPE'''
    p[0] = New(type=p[2])

def p_expression_isvoid(p):
    '''expression : ISVOID expression'''
    p[0] = IsVoid(expression=p[2])

def p_expression_tilde(p):
    '''expression : TILDE expression'''
    p[0] = Tilde(expression=p[2])

def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = Not(expression=p[2])


### CASE
def p_expression_case(p):
    ''' expression : CASE expression OF actions ESAC '''
    p[0] = Case(expression=p[2], actions=p[4])

def p_actions(p):
    ''' actions : actions action
                | action '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_action_expr(p):
    ''' action : ID COLON TYPE ARROW expression SEMICOLON '''
    p[0] = CaseAction(name=p[1], type=p[3], expression=p[5])


### LET
def p_expression_let(p):
    ''' expression : LET let_params IN expression '''
    p[0] = Let(params=p[2], expression=p[4])

def p_let_params(p):
    ''' let_params : let_params COMMA inner_let
                   | inner_let '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_inner_let(p):
    '''
    inner_let : ID COLON TYPE ASSIGNMENT expression
              | ID COLON TYPE
    '''
    children = None
    if len(p) == 6:
        children = p[5]
    p[0] = InnerLet(name=p[1], type=p[3], expression=children)


## OTHER --------------------------------------------------------------------
def p_empty(p):
    ''' empty : '''
    p[0] = None

def p_error(p):
    print("Syntax error! Line: {}, position: {}, character: {}, type: {}".format(p.lineno, p.lexpos, p.value, p.type))


## Parse
arq_name = sys.argv[1]
f = open(arq_name, "r")

parser = yacc.yacc()
root = parser.parse(f.read())

# Print abstract syntax tree (AST) 
#print(root)

semantic_analysis(root)
print("OK")