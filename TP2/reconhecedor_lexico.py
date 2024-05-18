import ply.lex as lex
import unicodedata # Para verificar se um caractere é uma letra ou número

# Definindo a codificação como UTF-8
# -*- coding: utf-8 -*-

# Este reconhecedor léxico serve para identificar todos os caracteres (tokens) na linguagem FCA

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
    'CONCATENATE',      # Novo token para o operador de concatenação
    'FUNCAO',           # Token para a palavra reservada 'FUNCAO'
    'FIM',              # Token para a palavra reservada 'FIM'
    'LISTA',            # Token para a palavra reservada 'LISTA'
    'MAP',              # Token para a palavra reservada 'MAP'
    'FOLD',             # Token para a palavra reservada 'FOLD'
    'COMMA',            # Token para a vírgula
    'AND',              # Token para o operador lógico 'E'
    'OR',               # Token para o operador lógico 'OU'
    'NOT',              # Token para o operador lógico 'NÃO'
    'TRUE',             # Token para o valor booleano 'verdadeiro'
    'FALSE'             # Token para o valor booleano 'falso'
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
t_COMMA = r','
t_EXCLAMATION_MARK = r'!'
t_QUESTION_MARK = r'\?'
t_CONCATENATE = r'<>'

# Função para identificar se um caractere é uma letra
def is_letter(char):
    return unicodedata.category(char).startswith('L')

# Função para identificar se um caractere é um número
def is_number(char):
    return unicodedata.category(char).startswith('N')

# Expressão regular para o token ID usando classes de caracteres Unicode
def t_ID(t):
    r'[^\W\d_][\w?!\']*'
    if all(is_letter(c) or is_number(c) or c in "_?!" for c in t.value):
        return t
    else:
        t.type = 'error'
        t_error(t)

# Expressão regular para o token NUMBER
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Expressão regular para a palavra FUNCAO
def t_FUNCAO(t):
    r'FUNCAO'
    return t

# Expressão regular para a palavra FIM
def t_FIM(t):
    r'FIM'
    return t

# Expressão regular para a palavra LISTA
def t_LISTA(t):
    r'LISTA'
    return t

# Expressão regular para a palavra MAP
def t_MAP(t):
    r'MAP'
    return t

# Expressão regular para a palavra FOLD
def t_FOLD(t):
    r'FOLD'
    return t

# Expressão regular para o E
def t_AND(t):
    r'E'
    return t

# Expressão regular para o OU
def t_OR(t):
    r'OU'
    return t

# Expressão regular para o NÃO
def t_NOT(t):
    r'NÃO'
    return t

# Expressão regular para o BOOLEANO TRUE
def t_TRUE(t):
    r'verdadeiro'
    return t

# Expressão regular para o BOOLEANO FALSE
def t_FALSE(t):
    r'falso'
    return t

# Expressão regular para o token STRING
def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]  # Remover as aspas
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