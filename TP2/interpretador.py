import sys
from reconhecedor_sintatico import parser

# Definindo a codificação como UTF-8
# -*- coding: utf-8 -*-

def interpretar_arquivo(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        result = parser.parse(data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python interpretador.py <caminho_para_arquivo>")
        sys.exit(1)

    arquivo_fca = sys.argv[1]
    interpretar_arquivo(arquivo_fca)

# Como executar o programa:
# 1º Passo: Abrir o terminal e ir para a pasta TP2
# 2º Passo: Ativar o virtualenv que tem a biblioteca ply: venv/scripts/activate
# 3º Passo: Executar o comando: python interpretador.py <escolher o ficheiro .fca>
