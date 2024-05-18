import ply.yacc as yacc
from reconhecedor_lexico import lexer, tokens
from criar_codigo import BinOp, Num, Id, Assign, Escrever, String, Concatenate

# Definindo a codificação como UTF-8
# -*- coding: utf-8 -*-

# Precedência e associatividade
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : assignment SEMICOLON
                 | escrever SEMICOLON
                 | entrada SEMICOLON'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ID EQUALS expression'''
    p[0] = Assign(p[1], p[3])

def p_escrever(p):
    '''escrever : ESCREVER expression'''
    p[0] = Escrever(p[2])

def p_entrada(p):
    '''entrada : ENTRADA LPAREN expression RPAREN'''
    # Ação semântica para entrada aqui
    pass

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = BinOp(p[2], p[1], p[3])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = Num(p[1])

def p_expression_id(p):
    '''expression : ID
                  | ID EXCLAMATION_MARK
                  | ID QUESTION_MARK'''
    p[0] = Id(p[1])

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = String(p[1])

def p_expression_concatenate(p):
    '''expression : expression CONCATENATE expression'''
    p[0] = Concatenate(p[1], p[3])

def p_error(p):
    if p:
        print(f"Erro de sintaxe em {p.value}")
    else:
        print("Erro de sintaxe: símbolo inesperado")

parser = yacc.yacc()
