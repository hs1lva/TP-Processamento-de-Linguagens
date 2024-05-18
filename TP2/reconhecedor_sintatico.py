import ply.yacc as yacc
from reconhecedor_lexico import lexer, tokens
from criar_codigo import BinOp, Num, Id, Assign, Escrever, String, Concatenate, Funcao, Lista, Map, Fold, And, Or, Not, Bool

# Definindo a codificação como UTF-8
# -*- coding: utf-8 -*-

# Este reconhecedor sintatico serve para estruturar a forma como os tokens são organizados na linguagem FCA

# Precedência e associatividade
precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'NOT'),
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
                 | entrada SEMICOLON
                 | funcao
                 | lista
                 | map
                 | fold'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ID EQUALS expression'''
    p[0] = Assign(p[1], p[3])

def p_escrever(p):
    '''escrever : ESCREVER expression'''
    p[0] = Escrever(p[2])

def p_entrada(p):
    '''entrada : ENTRADA LPAREN expression RPAREN'''
    pass  # Implementar se necessário

def p_funcao(p):
    '''funcao : FUNCAO ID LPAREN param_list RPAREN statement_list FIM'''
    p[0] = Funcao(p[2], p[4], p[6])

def p_param_list(p):
    '''param_list : ID
                  | param_list COMMA ID
                  | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_lista(p):
    '''lista : LISTA LPAREN expression_list RPAREN'''
    p[0] = Lista(p[3])

def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_map(p):
    '''map : MAP LPAREN expression COMMA expression RPAREN'''
    p[0] = Map(p[3], p[5])

def p_fold(p):
    '''fold : FOLD LPAREN expression COMMA expression COMMA expression RPAREN'''
    p[0] = Fold(p[3], p[5], p[7])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = BinOp(p[2], p[1], p[3])

def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = Not(p[2])

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

def p_expression_bool(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = Bool(p[1])

def p_empty(p):
    '''empty :'''
    p[0] = None

parser = yacc.yacc()
