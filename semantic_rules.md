Tipos, escopos, 

# Rules

## Program

- Every program must have a class Main; OK 
- The Main class must have a method main that takes no formal parameters; OK

## Class

- Defines a type, that must by unique; OK 
- Globally visible; OK 
- Must not make a cicly in the inheritance graph; OK
- Must inheritance from a defined class; OK

## Features

- All attributes have scope local to the class OK
- All methods have global scope (can be accessed by a child) OK
- No method name may be defined multiple times in a class OK
- No attribute name may be defined multiple times in a class OK
- A method and an attribute may have the same name OK

Inheritance
- The method of a child overrides the method of a parent if it has the same name OK
- It is illegal to redefine attribute names OK

## Method

- The identifiers used in the formal parameter list must be distinct OK
- The type of the method body must conform to the declared return type

## Attributes

- Inherited attributes cannot be redefined OK
- The static type of the expression must conform to the declared type of the attribute

## Types

- Special type SELF_TYPE, its the type of self (não tá claro, verificar)
- if C inherits from P, either directly or indirectly, then a C can be used wherever a P would suffice

## Expressions

## Constants

- Bool, Int and String

## Identifiers

- it is an error to assign to self or to bind self in a let, a case, or as a formal parameter
