import sys
import chardet # Para detetar a codificação do ficheiro .fca
from reconhecedor_sintatico import parser

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
    return chardet.detect(rawdata)['encoding']

def interpretar_ficheiro(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding) as file:
        data = file.read()
        result = parser.parse(data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python interpretador.py <caminho_para_ficheirofca>")
        sys.exit(1)

    ficheiro_fca = sys.argv[1]
    interpretar_ficheiro(ficheiro_fca)

# Como executar o programa:
# 1º Passo: Abrir o terminal e ir para a pasta TP2
# 2º Passo: Ativar o virtualenv que tem a biblioteca ply: venv/scripts/activate
# 3º Passo: Executar o comando: python interpretador.py <escolher o ficheiro .fca>

# O que foi instalado em venv?
# - pip install ply
# - pip install chardet
