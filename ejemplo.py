from antlr4 import *
from  antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser

def main():
    # Leer archivo
    input_stream = FileStream("programa.leng")

    #  LEXER 
    lexer = LenguajeLexer(input_stream)

    print("\nTOKENS:\n")

    # Sacar tokens DIRECTAMENTE del lexer (IMPORTANTE)
    token = lexer.nextToken()

    while token.type != Token.EOF:
        tipo = lexer.symbolicNames[token.type] if token.type < len(lexer.symbolicNames) else str(token.type)
        print(f"{tipo:15} -> {token.text:10} (línea {token.line}, col {token.column})")
        token = lexer.nextToken()

    print("EOF")

    #  PARSER 
    # Volver a leer archivo (porque el lexer ya se consumió)
    input_stream = FileStream("programa.leng")
    lexer = LenguajeLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LenguajeParser(stream)

    tree = parser.programa()

    print("\nÁRBOL:\n")
    print(tree.toStringTree(recog=parser))


if __name__ == '__main__':
    main()