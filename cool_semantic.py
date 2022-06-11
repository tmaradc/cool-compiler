from ast import arguments
from AST import *

# BASIC CLASSES

# OBS.: It is an error to inherit from Int, String and Bool

## Object

abort = FeatureMethod(name="abort", return_type="Object", expression=None)
type_name = FeatureMethod(name="type_name", return_type="String", expression=None)
copy = FeatureMethod(name="copy", return_type="SELF_TYPE", expression=None)

object_class = Class(name="Object", features=[abort, type_name, copy])
object_class.scopeMethods = { "abort": abort, "type_name": type_name, "copy": copy} 

## IO 
in_int = FeatureMethod(name="in_int", return_type="Int", expression=None)
in_string = FeatureMethod(name="in_string", return_type="String", expression=None)
out_int = FeatureMethod(name="out_int", return_type="SELF_TYPE", expression=None, 
                                formal_params=[Formal(name="x", type="Int")])
out_string = FeatureMethod(name="out_string", return_type="SELF_TYPE", expression=None, 
                                formal_params=[Formal(name="x", type="String")])

IO_class = Class(name="IO", features=[in_int, in_string, out_int, out_string])
IO_class.scopeMethods = { "in_int": in_int, "in_string": in_string, "out_int": out_int, "out_string": out_string} 
IO_class.scopeMethods.update(object_class.scopeMethods)

## Int 
int_class = Class(name="Int", features=[])
int_class.scopeMethods = {}
int_class.scopeMethods.update(object_class.scopeMethods)

## String 
length = FeatureMethod(name="length", return_type="Int", expression=None)
concat = FeatureMethod(name="concat", return_type="String", expression=None, 
                                 formal_params=[Formal(name="s", type="String")])
substr = FeatureMethod(name="substr", return_type="String", expression=None, 
                                 formal_params=[Formal(name="i", type="Int"),
                                                Formal(name="l", type="Int")])

string_class = Class(name="String", features=[length, concat, substr])
string_class.scopeMethods = { "length": length, "concat": concat, "substr": substr} 
string_class.scopeMethods.update(object_class.scopeMethods)

## Bool 
bool_class = Class(name="Bool", features=[])
bool_class.scopeMethods = {}
bool_class.scopeMethods.update(object_class.scopeMethods)
## ---------------------------------------------------------------------------------------------

## key: child ; value: parent
inheritance = {"IO": "Object", "Int": "Object", "Bool": "Object", "String": "Object"}

types = {"Object": object_class,
         "IO": IO_class,
         "Int": int_class,
         "String": string_class,
         "Bool": bool_class}

hasMainClassWithMainMethod = False

def error(message):
    raise Exception(message) 

def mainRule(ast_node):
    global hasMainClassWithMainMethod
    if ast_node.name == "Main":
        for feature in ast_node.features:
            if feature.identifier=="feature_method" and feature.name=="main":
                if feature.formal_params:
                    error('"main" method in class "Main" should have no arguments')
                else:
                    hasMainClassWithMainMethod = True

def inheritancePathTilObject(type):
    path = [type]
    while type != "Object":
        path.append(types[type])
        type = types[type]
    path.append("Object")

def least_parent(type1, type2):
    if type1 == type2:
        return type1
    if type1 in ["Int", "String", "Bool", "IO", "Object"]:
        return "Object"
    if type2 in ["Int", "String", "Bool", "IO", "Object"]:
        return "Object"
    
    path1 = inheritancePathTilObject(type1)
    path2 = inheritancePathTilObject(type2)

    for parent in path1:
        if parent in path2:
            return parent
    return "Object"

def selfTypeStaticRule(return_type, currentClass):
    if return_type == "SELF_TYPE":
        return currentClass
    return return_type

def invalidType(return_type, declared_type, currentClass):
    #return_type <= declared_type
    if declared_type == "SELF_TYPE":
        #para ser válido, tem que ser igual ao tipo da classe ou ser filho
        declared_type = currentClass

    if return_type == "SELF_TYPE":
        return_type = currentClass

    parent = return_type
    while parent!="Object":
        if parent == declared_type:
            return False
        parent = inheritance[parent]
    if parent == declared_type:
        return False
    return True

def expression(ast_node, scopeMethods, scopeAttr, currentClass):
    def assignment(ast_node, scopeMethods, scopeAttr, currentClass):
        expression_return_type = expression(ast_node.expression,scopeMethods, scopeAttr, currentClass)
        if ast_node.ID not in scopeAttr:
            error('assignment to undeclared variable "{0}"'.format(ast_node.ID))
        expected_type = (scopeAttr[ast_node.ID]).type
        if invalidType(expression_return_type, expected_type, currentClass):
            error('type "{0}" is not assignable to type "{1}"'.format(expression_return_type, expected_type))
        return selfTypeStaticRule(expected_type, currentClass)
    
    def id(ast_node, scopeMethods, scopeAttr, currentClass):
        if ast_node.name not in scopeAttr:
            error('undeclared variable "{0}"'.format(ast_node.name))
        return (scopeAttr[ast_node.name]).type

    def string(ast_node, scopeMethods, scopeAttr, currentClass):
        return "String"
    
    def boolean(ast_node, scopeMethods, scopeAttr, currentClass):
        return "Bool"

    def integer(ast_node, scopeMethods, scopeAttr, currentClass):
        return "Int"

    def rself(ast_node, scopeMethods, scopeAttr, currentClass):
        return currentClass
    
    def block(ast_node, scopeMethods, scopeAttr, currentClass):
        for expr in ast_node.expressions[0:len(ast_node.expressions)-1]:
            expression(expr,scopeMethods, scopeAttr, currentClass)
        
        lastExpression = ast_node.expressions[-1]
        return expression(lastExpression,scopeMethods, scopeAttr, currentClass)
    
    def math_binop(ast_node, scopeMethods, scopeAttr, currentClass):
        expr_right = expression(ast_node.expression_left,scopeMethods, scopeAttr, currentClass)
        expr_left = expression(ast_node.expression_right,scopeMethods, scopeAttr, currentClass)
        if expr_left != "Int":
            error('left side of the operator "{0}" must be of type "Int"'.format(ast_node.operation))
        if expr_right != "Int":
            error('right side of the operator "{0}" must be of type "Int"'.format(ast_node.operation))
        return "Int"

    def comparison(ast_node, scopeMethods, scopeAttr, currentClass):
        expr_right = expression(ast_node.expression_left,scopeMethods, scopeAttr, currentClass)
        expr_left = expression(ast_node.expression_right,scopeMethods, scopeAttr, currentClass)
            
        if ast_node.operation in ["<", "<="]:
            if expr_left != "Int":
                error('left side of the operator "{0}" must be of type "Int"'.format(ast_node.operation))
            if expr_right != "Int":
                error('right side of the operator "{0}" must be of type "Int"'.format(ast_node.operation))
        
        basic_types = ["Int", "Bool", "String"]
        if (expr_left in basic_types or expr_right in basic_types) and expr_left!=expr_right:
               error('illegal comparison between type "{0}" and type "{1}"'.format(expr_left, expr_right))

        return "Bool"
    
    def tilde(ast_node, scopeMethods, scopeAttr, currentClass):
        expression_return_type = expression(ast_node.expression,scopeMethods, scopeAttr, currentClass)
        if expression_return_type!="Int":
            error('expression following the "~" operator must be of type "Int"')

        return "Int"
    
    def rnot(ast_node, scopeMethods, scopeAttr, currentClass):
        expression_return_type = expression(ast_node.expression,scopeMethods, scopeAttr, currentClass)
        if expression_return_type!="Bool":
            error('expression following the "not" operator must be of type "Bool"')

        return "Bool"

    def isvoid(ast_node, scopeMethods, scopeAttr, currentClass):
        expression(ast_node.expression,scopeMethods, scopeAttr, currentClass)
        return "Bool"

    def new(ast_node, scopeMethods, scopeAttr, currentClass):
        if ast_node.type not in types:
            error('{0} is not defined'.format(ast_node.type))

        return ast_node.type
    
    def rwhile(ast_node, scopeMethods, scopeAttr, currentClass):
        condition_type = expression(ast_node.condition,scopeMethods, scopeAttr, currentClass)
        expression(ast_node.body,scopeMethods, scopeAttr, currentClass)    
        if condition_type != "Bool":
            error('the condition expression of a "while" statement must return a "Bool"')
        return "Object"
    
    def rif(ast_node, scopeMethods, scopeAttr, currentClass):
        condition_type = expression(ast_node.condition,scopeMethods, scopeAttr, currentClass)
        if condition_type != "Bool":
            error('the condition expression of a "if" statement must return a "Bool"')

        condition_true_type = expression(ast_node.condition_true,scopeMethods, scopeAttr, currentClass)
        condition_false_type = expression(ast_node.condition_false,scopeMethods, scopeAttr, currentClass) 
        
        return least_parent(condition_true_type, condition_false_type)
    
    def case(ast_node, scopeMethods, scopeAttr, currentClass):
        expression(ast_node.expression,scopeMethods, scopeAttr, currentClass)
        actions_types = []
        for action in ast_node.actions:
            copyScope = dict(scopeAttr)
            copyScope.update({action.name: action})
            actions_types.append(expression(action.expression, scopeMethods, copyScope, currentClass))
        
        return_type = ""
        for i in range(len(actions_types)-1):
            return_type = least_parent(actions_types[i], actions_types[i+1])
        return return_type
    
    def let(ast_node, scopeMethods, scopeAttr, currentClass):
        letScope = dict(scopeAttr)
        for param in ast_node.params:
            letScope.update({param.name: param})
            if param.expression:
                expression(param.expression,scopeMethods, letScope, currentClass)

        return_body_type = expression(ast_node.expression,scopeMethods, letScope, currentClass)
        return return_body_type

    def method_access(ast_node, scopeMethods, scopeAttr, currentClass):
        return_type = expression(ast_node.instance, scopeMethods, scopeAttr, currentClass)
        if ast_node.method not in types[return_type].scopeMethods:
            error('method "{0}" does not exist on type "{1}"'.format(ast_node.method, return_type))
        method = types[return_type].scopeMethods[ast_node.method]
        if len(method.formal_params) != len(ast_node.arguments): 
            error('method "{0}" takes exactly {1} parameter. {2} parameters were provided.'.format(ast_node.method, method.formal_params, ast_node.arguments))
        for i in range(len(ast_node.arguments)):
            expr_type = expression(ast_node.arguments[i], scopeMethods, scopeAttr, currentClass)
            if invalidType(expr_type, method.formal_params[i].type, currentClass):
                error('parameter {0} of method "{1}" must be of type "{2}". A parameter of type "{3}" was provided instead '.format(i, ast_node.method, method.formal_params[i].type, expr_type))
        return selfTypeStaticRule(method.return_type, return_type)
        
    def self_method_access(ast_node, scopeMethods, scopeAttr, currentClass):
        if ast_node.method not in scopeMethods:
            error('method "{0}" does not exist on type "{1}"'.format(ast_node.method, currentClass))
        method = scopeMethods[ast_node.method]
        if len(method.formal_params) != len(ast_node.arguments): 
            error('method "{0}" takes exactly {1} parameter. {2} parameters were provided.'.format(ast_node.method, method.formal_params, ast_node.arguments))
        for i in range(len(ast_node.arguments)):
            expr_type = expression(ast_node.arguments[i], scopeMethods, scopeAttr, currentClass)
            if invalidType(expr_type, method.formal_params[i].type, currentClass):
                error('parameter {0} of method "{1}" must be of type "{2}". A parameter of type "{3}" was provided instead '.format(i, ast_node.method, method.formal_params[i].type, expr_type))
        return selfTypeStaticRule(method.return_type, currentClass)
    
    def at_method_access(ast_node, scopeMethods, scopeAttr, currentClass):
        return_type = expression(ast_node.instance, scopeMethods, scopeAttr, currentClass)
        if ast_node.method not in types[ast_node.type].scopeMethods:
            error('method "{0}" does not exist on type "{1}"'.format(ast_node.method, ast_node.type))
        method = types[return_type].scopeMethods[ast_node.method]
        if invalidType(return_type, ast_node.type, currentClass):
            error('expression must be of type "{0}" instead of type "{1}"'.format(return_type, ast_node.type))
        if len(method.formal_params) != len(ast_node.arguments): 
            error('method "{0}" takes exactly {1} parameter. {2} parameters were provided.'.format(ast_node.method, method.formal_params, ast_node.arguments))
        for i in range(len(ast_node.arguments)):
            expr_type = expression(ast_node.arguments[i], scopeMethods, scopeAttr, currentClass)
            if invalidType(expr_type, method.formal_params[i].type, currentClass):
                error('parameter {0} of method "{1}" must be of type "{2}". A parameter of type "{3}" was provided instead '.format(i, ast_node.method, method.formal_params[i].type, expr_type))
        return method.return_type
    
    if ast_node.identifier == "assignment":
        return assignment(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "id":
        return id(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "string":
        return string(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "boolean":
        return boolean(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "integer":
        return integer(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "self":
        return rself(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "block":
        return block(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "math_binop":
        return math_binop(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "comparison":
        return comparison(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "tilde":
        return tilde(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "not":
        return rnot(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "isvoid":
        return isvoid(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "new":
        return new(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "while":
        return rwhile(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "if":
        return rif(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "case":
        return case(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "let":
        return let(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "method_access":
        return method_access(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "self_method_access":
        return self_method_access(ast_node, scopeMethods, scopeAttr, currentClass)
    if ast_node.identifier == "at_method_access":
        return at_method_access(ast_node, scopeMethods, scopeAttr, currentClass)


class FeatureSemantics():
    def __init__(self, ast_node, scopeMethods, scopeAttr, currentClass):
        if ast_node.identifier=="feature_method":
            self.methodRules(ast_node, scopeAttr)
            expression_return_type = expression(ast_node.expression, scopeMethods, scopeAttr, currentClass)
            if invalidType(expression_return_type, ast_node.return_type, currentClass):
                error('return type "{0}" of method "{1}" is not assignable to the declared type of "{2}"'.format(expression_return_type, ast_node.name, ast_node.return_type))

        if ast_node.identifier=="feature_attr" and ast_node.init:
            expression_return_type = expression(ast_node.init, scopeMethods, scopeAttr, currentClass)
            if invalidType(expression_return_type, ast_node.type, currentClass):
                error('type "{0}" is not assignable to type "{1}"'.format(expression_return_type, ast_node.return_type))


    def methodRules(self, ast_node, scopeAttr):
        formals = {}
        if ast_node.formal_params:
            for formal in ast_node.formal_params:
                if formal.name in formals:
                    error('parameter "{0}" is defined multiply times in method "{1}"'.format(formal.name, ast_node.name))
                formals[formal.name] = formal
        self.scopeAttr = scopeAttr.update(formals)


class ClassSemantics():
    def __init__(self, ast_node):
        self.parentScopeMethods = {}
        self.parentScopeAttr = {}
        self.ast_node = ast_node

        if ast_node.name in types:
            error('{0} has already been defined'.format(ast_node.name))
        if ast_node.inherits and ast_node.inherits not in types:
            error('{0} is not defined'.format(ast_node.inherits))
        if ast_node.inherits in ["Bool", "String", "Int"]:
            error('classes cannot inherit from "{0}"'.format(ast_node.inherits))
        if ast_node.inherits:
            self.addInheritance(ast_node.name, ast_node.inherits)
        if ast_node.name == "Main":
            mainRule(ast_node)
        
        self.addParentScopes(ast_node.inherits)
        scopeFeaturesMethods = {}
        scopeFeaturesAttr = {}
        for feature in ast_node.features:
            if feature.identifier=="feature_method":
                if feature.name in scopeFeaturesMethods:
                    error('method "{0}" is multiply defined in class "{1}"'.format(feature.name, ast_node.name))
                else:
                    scopeFeaturesMethods[feature.name] = feature
            if feature.identifier=="feature_attr":
                if feature.name in scopeFeaturesAttr or feature.name in self.parentScopeAttr:
                    error('property "{0}" is multiply defined in class "{1}"'.format(feature.name, ast_node.name))
                else:
                    scopeFeaturesAttr[feature.name] = feature

        #Override parents methods if has the same name
        (self.parentScopeMethods).update(scopeFeaturesMethods)
        (self.parentScopeAttr).update(scopeFeaturesAttr)
        ast_node.scopeMethods = self.parentScopeMethods
        types[ast_node.name] = ast_node

    def featuresCheck(self):
        for feature in self.ast_node.features:
            FeatureSemantics(feature, self.parentScopeMethods, self.parentScopeAttr, self.ast_node.name)

    #Is it possible to have a cycle??
    def verifyCycle(self, parent: String, new_type: String):
        if parent == "Object":
            return

        if inheritance[parent]==new_type:
            error("inheritance is cyclic")
        else:
            self.verifyCycle(inheritance[parent], new_type)

    def addInheritance(self, new_class_name: String, parent: String):
        inheritance[new_class_name] = parent
        if parent in ["Int", "String", "Bool"]:
            error("a class can't inherit from Int, String or Bool")
        self.verifyCycle(parent, new_class_name)

    def addParentScopes(self, parent):
        #recursive
        ast_parent = types[parent] 
        for feature in ast_parent.features:
            if feature.identifier=="feature_method":
                self.parentScopeMethods[feature.name] = feature
            if feature.identifier=="feature_attr":
                self.parentScopeAttr[feature.name] = feature
        if parent!="Object":
            self.addParentScopes(inheritance[parent])



def semantic_analysis(ast_node: AST):
    classesRules = []
    if ast_node.identifier == "program":
        for class_program in ast_node.classes:
            classesRules.append(ClassSemantics(class_program))
        for class_rule in classesRules:
            class_rule.featuresCheck()

    if not hasMainClassWithMainMethod:
        error("the program must have a class Main with a main method defined")

