# Cool Compiler

A compiler for the Cool language, which I am developing for the Compilers course of my Computer Science degree.

I'm using [PLY](https://www.dabeaz.com/ply/) for the lexical and syntax analysis.


# Phases of Compilation

- lexical analysis: [`cool_lex.py`](cool_lex.py) 
- syntax analysis: [`cool_syntax.py`](cool_syntax.py) 

    > Ply-Yacc uses a parsing technique known as LR-parsing or shift-reduce parsing. LR parsing is a *bottom up* technique that tries to recognize the right-hand-side of various grammar rules.

Soon

- semantic analysis
- code generation

# How to run

Install PLY
```console
pip install ply
```

Generate and print abstract syntax tree (AST)
```console
python cool_lex.py cool_files/cool.cl
```
    
