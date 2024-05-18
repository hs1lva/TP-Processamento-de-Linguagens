import sys
from reconhecedor_sintatico import parser

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
