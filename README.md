# Cool Compiler

A compiler for the Cool language, which I developed for the Compilers course of my Computer Science degree.

I'm using [PLY](https://www.dabeaz.com/ply/) for the lexical and syntax analysis.

The intermediate language used for the code generation was the [Bril](https://github.com/sampsyo/bril) language.

# Phases of Compilation

- lexical analysis: [`cool_lex.py`](cool_lex.py) 
- syntax analysis: [`cool_syntax.py`](cool_syntax.py) 

    > Ply-Yacc uses a parsing technique known as LR-parsing or shift-reduce parsing. LR parsing is a *bottom up* technique that tries to recognize the right-hand-side of various grammar rules.

- semantic analysis: [`cool_semantic.py`](cool_semantic.py)
- code generation: [`code_generation.py`](code_generation.py)
    > Since Bril doesn't have the type *string*, my code only accepts `Bool` and `Int` as primitive types. For class attributes, it only accepts *integers*. Also, some expressions were not translated to Bril.


# How to run

Install PLY
```console
pip install ply
```

Compile the code
```console
python cool_syntax.py cool_files/cool.cl
```

After compiling, it will be generated a Bril code in the *json* format. This file will have the same path and name of the cool file, but with the `.bril` extension.

You can run the Bril code with the `brili` tool. 
```console
brili < cool_files/cool.bril
```

To install this tool, read the [bril documentation](https://github.com/sampsyo/bril).
