import json

#liberar memória, while e if 

types_per_class = {}
memory_to_free = []
lets = {}
cont = 0

def thisArg():
    return [{"name": "this", "type": {"ptr": "int"}}]

def classMethod(method, class_attr_ordered, currentClass, inheritance):
    if method in class_attr_ordered[currentClass]['classMethods']:
        return currentClass, class_attr_ordered[currentClass]['classMethods'][method].return_type
    return classMethod(method, class_attr_ordered, inheritance[currentClass], inheritance)


def expressionToInstruction(expression, class_attr_ordered, currentClass, inheritance, instructions):
    def letBril(expression, class_attr_ordered, currentClass, inheritance, instructions):
        for param in expression.params:
            if param.type == "Int" and not param.expression:
                instructions += [{
                        "dest": param.name,
                        "op": "const",
                        "type": "int",
                        "value": 0 
                    }]
                lets[param.name] = "Int"
            else:
                if param.expression:
                    var, instructions, typeAux = expressionToInstruction(param.expression, class_attr_ordered, currentClass, inheritance, instructions)
                    instructions += [{
                        "args": [
                            var
                        ],
                        "dest": param.name,
                        "op": "id"
                    }]
                    lets[param.name] = typeAux
                else:
                    lets[param.name] = param.type
        var, instructions, typeAux = expressionToInstruction(expression.expression, class_attr_ordered, currentClass, inheritance, instructions)
        return var, instructions, typeAux

    def assignmentBril(expression, class_attr_ordered, currentClass, inheritance, instructions):
        global cont
        var, instructions, typeAux = expressionToInstruction(expression.expression, class_attr_ordered, currentClass, inheritance, instructions)
        if expression.ID in class_attr_ordered[currentClass]["scopeAttrList"]:
            temp_var = "temp" + str(cont)
            cont += 1
            index = class_attr_ordered[currentClass]["scopeAttrList"].index(expression.ID)
            inst = [
                {
                    "dest": temp_var,
                    "op": "const",
                    "type": "int",
                    "value": index
                },
                {
                    "args": [
                        "this",
                        temp_var
                    ],
                    "dest": "this" + str(cont),
                    "op": "ptradd",
                    "type": {
                        "ptr": "int"
                    }
                },
                {
                    "args": [
                        "this" + str(cont),
                        var
                    ],
                    "op": "store"
                }
            ]
            instructions += inst
            return "this" + str(cont), instructions, typeAux
        else:
            inst = {
                "args": [
                    var
                ],
                "dest": expression.ID,
                "op": "id"
            }
            instructions.append(inst)
            return expression.ID, instructions, typeAux

    def newBril(expression, class_attr_ordered, currentClass, inheritance, instructions):
        global cont
        return_var = "new" + str(cont)
        cont += 1 
        inst = [
            {
                "dest": "size" + return_var,
                "op": "const",
                "type": "int",
                "value": len(class_attr_ordered[expression.type]['scopeAttrList'])
            },
            {
                "args": [
                    "size" + return_var
                ],
                "dest": return_var,
                "op": "alloc",
                "type": {
                    "ptr": "int"
                }
            }
        ]
        memory_to_free.append(return_var)
        instructions += inst
        return return_var, instructions, expression.type

    def idBril(expression, class_attr_ordered, currentClass, inheritance, instructions):
        global cont
        if expression.name in class_attr_ordered[currentClass]['scopeAttrList']:
            temp_var = "temp" + str(cont)
            attr = "this" + str(cont)
            load_var = "load" + str(cont)
            cont += 1
            index = class_attr_ordered[currentClass]["scopeAttrList"].index(expression.name)
            inst = [
                {
                    "dest": temp_var,
                    "op": "const",
                    "type": "int",
                    "value": index
                },
                {
                    "args": [
                        "this",
                        temp_var
                    ],
                    "dest": attr,
                    "op": "ptradd",
                    "type": {
                        "ptr": "int"
                    }
                },
                {
                    "args": [
                        attr
                    ],
                    "dest": load_var,
                    "op": "load",
                    "type": "int"
                }
            ]
            instructions += inst
            return load_var, instructions, "Int"
        return expression.name, instructions, lets.get(expression.name, "Int")

    def integerBril(expression, class_attr_ordered, currentClass, inheritance, instructions):
        global cont
        return_var = "integer" + str(cont)
        cont += 1
        inst = {
            "dest": return_var,
            "op": "const",
            "type": "int",
            "value": expression.value 
        }
        instructions.append(inst)
        return return_var, instructions, "Int"

    def selfMethodAccessBril(expression, class_attr_ordered, currentClass, inheritance, instructions):
        global cont
        class_method, return_type = classMethod(expression.method, class_attr_ordered, currentClass, inheritance)
        return_var = "temp" + str(cont)
        cont += 1
        args = []
        for var in expression.arguments:
            arg, instructions, typeAux = expressionToInstruction(var, class_attr_ordered, currentClass, inheritance, instructions)
            args.append(arg)

        inst = {
          "args": ["this"] + args,
          "dest": return_var,
          "funcs": [
            class_method + "_" + expression.method
          ],
          "op": "call",
          "type": {"ptr": "int"} if return_type != "Int" else "int"
        }
        instructions.append(inst)
        return return_var, instructions, return_type

    def methodAccessBril(expression, class_attr_ordered, currentClass, inheritance, instructions):
        global cont
        argThis, instructions, typeAux = expressionToInstruction(expression.instance, class_attr_ordered, currentClass, inheritance, instructions)
        #Não é a currentClass aqui ... é o tipo do argThis (COMO SABER????)
        class_method, return_type = classMethod(expression.method, class_attr_ordered, typeAux, inheritance)
        return_var = "temp" + str(cont)
        cont += 1
        args = []
        for var in expression.arguments:
            arg, instructions, typeAux = expressionToInstruction(var, class_attr_ordered, currentClass, inheritance, instructions)
            args.append(arg)        

        inst = {
          "args": [argThis] + args,
          "dest": return_var,
          "funcs": [
            class_method + "_" + expression.method
          ],
          "op": "call",
          "type": {"ptr": "int"} if return_type != "Int" else "int"
        }
        instructions.append(inst)
        return return_var, instructions, return_type
    
    def atMethodAccessBril(expression, class_attr_ordered, currentClass, inheritance, instructions):
        global cont
        return_type = class_attr_ordered[expression.type]['classMethods'][expression.method].return_type
        return_var = "temp" + str(cont)
        cont += 1
        args = []
        for var in expression.arguments:
            arg, instructions, typeAux = expressionToInstruction(var, class_attr_ordered, currentClass, inheritance, instructions)
            args.append(arg)

        argThis, instructions, typeAux = expressionToInstruction(expression.instance, class_attr_ordered, currentClass, inheritance, instructions)        

        inst = {
          "args": [argThis] + args,
          "dest": return_var,
          "funcs": [
            expression.type + "_" + expression.method
          ],
          "op": "call",
          "type": {"ptr": "int"} if return_type != "Int" else "int"
        }
        instructions.append(inst)
        return return_var, instructions, return_type
        
    def selfBril(expression, class_attr_ordered, currentClass, inheritance, instructions):
        return "this", instructions, currentClass

    def blockBril(expression, class_attr_ordered, currentClass, inheritance, instructions):
        for exp in expression.expressions: 
            ret, instructions, typeAux = expressionToInstruction(exp, class_attr_ordered, currentClass, inheritance, instructions)
        return ret, instructions, typeAux

    if expression.identifier == "assignment":
        return assignmentBril(expression, class_attr_ordered, currentClass, inheritance, instructions)
    if expression.identifier == "self_method_access":
        return selfMethodAccessBril(expression, class_attr_ordered, currentClass, inheritance, instructions)
    if expression.identifier == "method_access":
        return methodAccessBril(expression, class_attr_ordered, currentClass, inheritance, instructions)
    if expression.identifier == "at_method_access":
        return atMethodAccessBril(expression, class_attr_ordered, currentClass, inheritance, instructions)
    if expression.identifier == "id":
        return idBril(expression, class_attr_ordered, currentClass, inheritance, instructions)
    if expression.identifier == "integer":
        return integerBril(expression, class_attr_ordered, currentClass, inheritance, instructions)
    if expression.identifier == "new":
        return newBril(expression, class_attr_ordered, currentClass, inheritance, instructions)
    if expression.identifier == "self":
        return selfBril(expression, class_attr_ordered, currentClass, inheritance, instructions)
    if expression.identifier == "block":
        return blockBril(expression, class_attr_ordered, currentClass, inheritance, instructions)
    if expression.identifier == "let":
        return letBril(expression, class_attr_ordered, currentClass, inheritance, instructions)



def generate_code(types, inheritance, class_attr_ordered, arq_name):
    global cont
    bril_code = {}
    functions = [{
      "args": thisArg() + [
        {
          "name": "number",
          "type": "int"
        }
      ],
      "instrs": [
        {
          "args": [
            "number"
          ],
          "op": "print"
        },
        {
            "args": [
                "this"
            ],
            "op": "ret"
        }
      ],
      "name": "IO_out_int",
      "type": {"ptr": "int"}
    }]

    for cool_class in types:
        if cool_class  in ["Int", "Bool", "IO", "Object", "String"]:
            continue
        for feature in types[cool_class].features:
            if feature.identifier=="feature_attr":
                continue
            cont = 0
            ret, instructions, typeAux = expressionToInstruction(feature.expression, class_attr_ordered, cool_class, inheritance, [])
            retBril = {
                "args": [
                    ret
                ],
                "op": "ret"
            }
            method = {
                "name": cool_class + "_" + feature.name,
                "args": thisArg() + [{"name": formal.name, "type": ("int" if formal.type=="Int" else {"ptr": "int"})} 
                                                for formal in feature.formal_params],
                "type": "int" if feature.return_type=="Int" else {"ptr": "int"},
                "instrs": instructions + [retBril]
            }
            if feature.name=="main" and cool_class=="Main":
                method = {
                    "name": "main",
                    "args": [],
                    "instrs": instructions
                }

            functions.append(method)

    bril_code["functions"] = functions
    out_file = open(arq_name.split(".")[0] + ".bril", "w") 
    json.dump(bril_code, out_file, indent = 2)    
    out_file.close()
