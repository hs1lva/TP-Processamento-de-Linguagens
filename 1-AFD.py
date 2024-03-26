import json
import graphviz
import argparse

class Automato:
    def __init__(self, ficheiro_definicao):
        # Carrega a definição do automato a partir do ficheiro JSON
        with open(ficheiro_definicao, 'r') as ficheiro:
            self.definicao = json.load(ficheiro)

    def reconhecer_palavra(self, palavra):
        # Executa o automato para reconhecer a palavra
        estado_atual = self.definicao['q0']
        caminho = [estado_atual]

        # Percorre a palavra e transita entre os estados conforme as transições do automato
        for char in palavra:
            try:
                prox_estado = self.definicao['delta'][estado_atual][char]
                caminho.append(prox_estado)
                estado_atual = prox_estado
            except KeyError:
                return False, caminho, f"Não há transição do estado {estado_atual} com o símbolo '{char}'."

        # Verifica se o estado final alcançado é um estado final do automato
        if estado_atual in self.definicao['F']:
            return True, caminho, None
        else:
            return False, caminho, f"O estado {estado_atual} não é um estado final."

    def verificar_afd(self):
        # Verifica se o automato carregado é um AFD válido
        for estado, trans in self.definicao['delta'].items():
            for simbolo, prox_estado in trans.items():
                if isinstance(prox_estado, list):
                    return False  # Se houver transição não determinística, não é um AFD
        return True  # Se não houver transições não determinísticas, é um AFD válido

def main():
    # Configuração do parser de argumentos
    # Terminal ------> python 1-AFD.py ficheiro.json palavra
    parser = argparse.ArgumentParser(description="Implementação de AFD")
    parser.add_argument('ficheiro_json', metavar='ficheiro_json', type=str,
                        help='O caminho para o ficheiro JSON contendo a definição do AFD')
    parser.add_argument('palavra', metavar='palavra', type=str,
                        help='A palavra a ser reconhecida pelo automato')

    # Parse dos argumentos da linha de comando
    args = parser.parse_args()

    # Carrega o AFD a partir do ficheiro JSON fornecido
    automato = Automato(args.ficheiro_json)

    # Verifica se o automato é um AFD válido antes de executá-lo
    if automato.verificar_afd():
        print("O automato é um AFD válido.")
        reconhecido, caminho, erro = automato.reconhecer_palavra(args.palavra)
        if reconhecido:
            print(f"A palavra '{args.palavra}' é reconhecida.")
            print("Caminho percorrido:", ' -> '.join(caminho))
        else:
            print(f"A palavra '{args.palavra}' não é reconhecida.")
            print("Situação de erro:", erro)
    else:
        print("O automato não é um AFD válido.")

if __name__ == "__main__":
    main()
