import ply.lex as lex

# Definindo a codificação como UTF-8
# -*- coding: utf-8 -*-

# Lista de tokens
tokens = (
    'ID',               # Novo token para identificadores
    'NUMBER',           # Novo token para números inteiros
    'PLUS',             # Novo token para o caractere '+'
    'MINUS',            # Novo token para o caractere '-'
    'TIMES',            # Novo token para o caractere '*'
    'DIVIDE',           # Novo token para o caractere '/'
    'EQUALS',           # Novo token para o caractere '='
    'LPAREN',           # Novo token para o caractere '('
    'RPAREN',           # Novo token para o caractere ')'
    'SEMICOLON',        # Novo token para o caractere ';'
    'ESCREVER',         # Novo token para a função de escrita
    'ENTRADA',          # Novo token para a função de entrada
    'EXCLAMATION_MARK', # Novo token para o caractere '!'
    'QUESTION_MARK',    # Novo token para o caractere '?'
    'STRING',           # Novo token para strings
    'CONCATENATE'       # Novo token para o operador de concatenação
)

# Regras de expressão regular para tokens simples
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUALS  = r'='
t_SEMICOLON = r';'

# Expressão regular para o token ID
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9?!\']*'
    return t

# Expressão regular para o token NUMBER
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Expressão regular para o token ESCREVER
def t_ESCREVER(t):
    r'ESCREVER'
    return t

# Expressão regular para o token ENTRADA
def t_ENTRADA(t):
    r'ENTRADA'
    return t

# Expressão regular para o token EXCLAMATION_MARK
def t_EXCLAMATION_MARK(t):
    r'!'
    return t

# Expressão regular para o token QUESTION_MARK
def t_QUESTION_MARK(t):
    r'\?'
    return t

# Expressão regular para o token STRING
def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]  # Remover as aspas
    return t

# Expressão regular para o token CONCATENATE
def t_CONCATENATE(t):
    r'<>'
    return t

# Caracteres ignorados (espaços e tabulações)
t_ignore = ' \t'

# Função para rastrear números de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Função de erro para caracteres desconhecidos
def t_error(t):
    print(f"Erro: Caractere desconhecido '{t.value[0]}' na linha {t.lineno}, coluna {t.lexpos + 1}")
    t.lexer.skip(1)

# Construa o analisador léxico
lexer = lex.lex()
