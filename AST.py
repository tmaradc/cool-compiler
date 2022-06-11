class AST:
    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self, level=0):
        pass

class Program(AST):
    def __init__(self, classes):
        super().__init__("program")
        self.classes = classes

    def __str__(self, level=0):
        ret = "\t"*level+"Program"+"\n"
        for child in self.classes:
            ret += child.__str__(level+1)
        return ret

class Class(AST):
    def __init__(self, name, features, inherits=None):
        super().__init__("class")
        self.name = name
        self.features = features
        self.inherits = inherits if inherits else "Object"

    def __str__(self, level=0):
        ret = "\t"*level+"Class_"+self.name+"/"+self.inherits+"\n"
        for child in self.features:
            ret += child.__str__(level+1)
        return ret

class FeatureMethod(AST):
    def __init__(self, name, return_type, expression, formal_params=[]):
        super().__init__("feature_method")
        self.name = name
        self.return_type = return_type
        self.expression = expression
        self.formal_params = formal_params

    def __str__(self, level=0):
        ret = "\t"*level+"Method_"+self.name+"/"+self.return_type+"\n"
        ret += "\t"*level+"Formal Params:\n"
        if self.formal_params:
            for child in self.formal_params:
                ret += child.__str__(level+1)
        if self.expression:
            ret += self.expression.__str__(level+1)
        return ret

class FeatureAttr(AST):
    def __init__(self, name, type, init=None):
        super().__init__("feature_attr")
        self.name = name
        self.type = type
        self.init = init #expression

    def __str__(self, level=0):
        ret = "\t"*level+"Attr_"+self.name+"/"+self.type+"\n"
        if self.init:
            ret += self.init.__str__(level+1)
        return ret

class Formal(AST):
    def __init__(self, name, type):
        super().__init__("formal")
        self.name = name
        self.type = type

    def __str__(self, level=0):
        ret = "\t"*level+"Formal_"+self.name+"/"+self.type+"\n"
        return ret

### ---------------------------------- EXPRESSIONS

class Expression(AST):
    def __init__(self, identifier):
        super().__init__(identifier)

class Assignment(Expression):
    def __init__(self, ID, expression):
        super().__init__("assignment")
        self.ID = ID
        self.expression = expression

    def __str__(self, level=0):
        ret = "\t"*level+"Assignment_"+self.ID+"\n"
        ret += self.expression.__str__(level+1)
        return ret

class ID(Expression):
    def __init__(self, name):
        super().__init__("id")
        self.name = name

    def __str__(self, level=0):
        ret = "\t"*level+"ID_"+self.name+"\n"
        return ret

class Integer(Expression):
    def __init__(self, value):
        super().__init__("integer")
        self.value = value

    def __str__(self, level=0):
        ret = "\t"*level+"Integer_"+str(self.value)+"\n"
        return ret

class String(Expression):
    def __init__(self, value):
        super().__init__("string")
        self.value = value

    def __str__(self, level=0):
        ret = "\t"*level+"String_"+self.value+"\n"
        return ret

class Boolean(Expression):
    def __init__(self, value):
        super().__init__("boolean")
        self.value = value

    def __str__(self, level=0):
        ret = "\t"*level+"Boolean_"+self.value+"\n"
        return ret

class Self(Expression):
    def __init__(self):
        super().__init__("self")

    def __str__(self, level=0):
        ret = "\t"*level+"Self\n"
        return ret

class Block(Expression):
    def __init__(self, expressions):
        super().__init__("block")
        self.expressions = expressions

    def __str__(self, level=0):
        ret = "\t"*level+"Block\n"
        for child in self.expressions:
            ret += child.__str__(level+1)
        return ret

class MethodAccess(Expression):
    def __init__(self, instance, method, arguments=[]):
        super().__init__("method_access")
        self.instance = instance
        self.method = method
        self.arguments = arguments

    def __str__(self, level=0):
        ret = "\t"*level+"MethodAccess_"+self.method+"\n"
        ret += "\t"*level+"Instance\n"
        ret += self.instance.__str__(level+1)
        if self.arguments:
            ret += "\t"*level+"Arguments\n"
            for child in self.arguments:
                ret += child.__str__(level+1)
        return ret

class AtMethodAccess(Expression):
    def __init__(self, instance, type, method, arguments=[]):
        super().__init__("at_method_access")
        self.instance = instance
        self.type = type
        self.method = method
        self.arguments = arguments

    def __str__(self, level=0):
        ret = "\t"*level+"AtMethodAccess_"+self.method+"/"+self.type+"\n"
        ret += "\t"*level+"Instance\n"
        ret += self.instance.__str__(level+1)
        if self.arguments:
            ret += "\t"*level+"Arguments\n"
            for child in self.arguments:
                ret += child.__str__(level+1)
        return ret

class SelfMethodAccess(Expression):
    def __init__(self, method, arguments=[]):
        super().__init__("self_method_access")
        self.method = method
        self.arguments = arguments

    def __str__(self, level=0):
        ret = "\t"*level+"SelfMethodAccess_"+self.method+"\n"
        if self.arguments:
            ret += "\t"*level+"Arguments\n"
            for child in self.arguments:
                ret += child.__str__(level+1)
        return ret

class MathBinop(Expression):
    def __init__(self, operation, expression_left, expression_right):
        super().__init__("math_binop")
        self.operation = operation
        self.expression_left = expression_left
        self.expression_right = expression_right

    def __str__(self, level=0):
        ret = "\t"*level+"MathBinop/"+self.operation+"\n"
        ret += "\t"*level+"Expression_left\n"
        ret += self.expression_left.__str__(level+1)
        ret += "\t"*level+"Expression_right\n"
        ret += self.expression_right.__str__(level+1)
        return ret

class Comparison(Expression):
    def __init__(self, operation, expression_left, expression_right):
        super().__init__("comparison")
        self.operation = operation
        self.expression_left = expression_left
        self.expression_right = expression_right

    def __str__(self, level=0):
        ret = "\t"*level+"Comparison/"+self.operation+"\n"
        ret += "\t"*level+"Expression_left\n"
        ret += self.expression_left.__str__(level+1)
        ret += "\t"*level+"Expression_right\n"
        ret += self.expression_right.__str__(level+1)
        return ret

class IF(Expression):
    def __init__(self, condition, condition_true, condition_false):
        super().__init__("if")
        self.condition = condition
        self.condition_true = condition_true
        self.condition_false = condition_false

    def __str__(self, level=0):
        ret = "\t"*level+"IF\n"
        ret += "\t"*level+"Condition\n"
        ret += self.condition.__str__(level+1)
        ret += "\t"*level+"If true\n"
        ret += self.condition_true.__str__(level+1)
        ret += "\t"*level+"If false\n"
        ret += self.condition_false.__str__(level+1)
        return ret

class While(Expression):
    def __init__(self, condition, body):
        super().__init__("while")
        self.condition = condition
        self.body = body

    def __str__(self, level=0):
        ret = "\t"*level+"IF\n"
        ret += "\t"*level+"Condition\n"
        ret += self.condition.__str__(level+1)
        ret += "\t"*level+"Body\n"
        ret += self.body.__str__(level+1)
        return ret

class New(Expression):
    def __init__(self, type):
        super().__init__("new")
        self.type = type

    def __str__(self, level=0):
        ret = "\t"*level+"New/"+self.type+"\n"
        return ret

class IsVoid(Expression):
    def __init__(self, expression):
        super().__init__("isvoid")
        self.expression = expression

    def __str__(self, level=0):
        ret = "\t"*level+"Isvoid\n"
        ret += self.expression.__str__(level+1)
        return ret

class Tilde(Expression):
    def __init__(self, expression):
        super().__init__("tilde")
        self.expression = expression

    def __str__(self, level=0):
        ret = "\t"*level+"Tilde\n"
        ret += self.expression.__str__(level+1)
        return ret

class Not(Expression):
    def __init__(self, expression):
        super().__init__("not")
        self.expression = expression

    def __str__(self, level=0):
        ret = "\t"*level+"Not\n"
        ret += self.expression.__str__(level+1)
        return ret

class Case(Expression):
    def __init__(self, expression, actions):
        super().__init__("case")
        self.expression = expression
        self.actions = actions

    def __str__(self, level=0):
        ret = "\t"*level+"Case\n"
        ret += self.expression.__str__(level+1)
        ret += "\t"*level+"Actions\n"
        for child in self.actions:
            ret += child.__str__(level+1)
        return ret

class CaseAction(Expression):
    def __init__(self, name, type, expression):
        super().__init__("case_action")
        self.name = name
        self.type = type
        self.expression = expression

    def __str__(self, level=0):
        ret = "\t"*level+"Case_"+self.name+"/"+self.type+"\n"
        ret += self.expression.__str__(level+1)
        return ret

class Let(Expression):
    def __init__(self, params, expression):
        super().__init__("let")
        self.params = params
        self.expression = expression

    def __str__(self, level=0):
        ret = "\t"*level+"Let\n"
        ret += "\t"*level+"Expression\n"
        ret += self.expression.__str__(level+1)
        ret += "\t"*level+"Params\n"
        for child in self.params:
            ret += child.__str__(level+1)
        return ret

class InnerLet(Expression):
    def __init__(self, name, type, expression=None):
        super().__init__("inner_let")
        self.name = name
        self.type = type
        self.expression = expression

    def __str__(self, level=0):
        ret = "\t"*level+"InnerLet_"+self.name+"/"+self.type+"\n"
        if self.expression:
            ret += "\t"*level+"Expression\n"
            ret += self.expression.__str__(level+1)
        return ret
        