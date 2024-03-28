import json
import argparse

def ler_expressao_regular(ficheiro_json):
    """
    Lê a expressão regular a partir do ficheiro JSON.

    Args:
        ficheiro_json (str): O caminho para o ficheiro JSON contendo a expressão regular.

    Returns:
        dict: A expressão regular representada como um dicionário Python.
    """
    with open(ficheiro_json, 'r') as ficheiro:
        return json.load(ficheiro)

def converter_afnd(expressao_regular):
    """
    Converte uma expressão regular num autômato finito não determinista (AFND) equivalente.

    Args:
        expressao_regular (dict): A expressão regular representada como um dicionário Python.

    Returns:
        dict: O AFND equivalente representado como um dicionário Python.
    """

    def criar_estado():
        """
        Função auxiliar para criar um novo estado único.
        """
        nonlocal contador_estado
        estado = f"q{contador_estado}"
        contador_estado += 1
        return estado

    def concatenacao(afnd1, afnd2):
        """
        Realiza a operação de concatenação entre dois AFNDs.

        Args:
            afnd1 (dict): O primeiro AFND representado como um dicionário Python.
            afnd2 (dict): O segundo AFND representado como um dicionário Python.

        Returns:
            dict: O AFND resultante da concatenação.
        """
        # Adiciona transições vazias do estado final de afnd1 para o estado inicial de afnd2
        for estado_final in afnd1["F"]:
            afnd1["delta"].setdefault(estado_final, {}).update({"" : [afnd2["q0"]]})
        # Atualiza os estados finais do AFND resultante
        afnd1["F"] = afnd2["F"]
        # Atualiza as transições do AFND resultante
        afnd1["delta"].update(afnd2["delta"])
        return afnd1

    def uniao(afnd1, afnd2):
        """
        Realiza a operação de união entre dois AFNDs.

        Args:
            afnd1 (dict): O primeiro AFND representado como um dicionário Python.
            afnd2 (dict): O segundo AFND representado como um dicionário Python.

        Returns:
            dict: O AFND resultante da união.
        """
        # Cria um novo estado inicial para o AFND resultante
        novo_estado_inicial = criar_estado()
        # Define as transições vazias do novo estado inicial para os estados iniciais de afnd1 e afnd2
        novo_delta = {"": [afnd1["q0"], afnd2["q0"]]}
        # Atualiza o conjunto de estados, alfabeto e conjunto de estados finais do AFND resultante
        novo_afnd = {
            "Q": [novo_estado_inicial] + afnd1["Q"] + afnd2["Q"],
            "Sigma": afnd1["Sigma"] | afnd2["Sigma"],
            "delta": {**novo_delta, **afnd1["delta"], **afnd2["delta"]},
            "q0": novo_estado_inicial,
            "F": afnd1["F"] + afnd2["F"]
        }
        return novo_afnd

    def kleene(afnd):
        """
        Realiza a operação de fecho de Kleene num AFND.

        Args:
            afnd (dict): O AFND representado como um dicionário Python.

        Returns:
            dict: O AFND resultante do fecho de Kleene.
        """
        # Cria um novo estado inicial e um novo estado final para o AFND resultante
        novo_estado_inicial = criar_estado()
        novo_estado_final = criar_estado()
        # Define as transições vazias do novo estado inicial para o estado inicial do AFND original
        # e do estado final do AFND original para o novo estado final
        novo_delta = {"": [afnd["q0"], novo_estado_final]}
        # Atualiza o conjunto de estados, alfabeto e conjunto de estados finais do AFND resultante
        novo_afnd = {
            "Q": [novo_estado_inicial, novo_estado_final] + afnd["Q"],
            "Sigma": afnd["Sigma"],
            "delta": {**novo_delta, **afnd["delta"]},
            "q0": novo_estado_inicial,
            "F": [novo_estado_final]
        }
        return novo_afnd

    # Inicializa o contador de estados
    contador_estado = 0

    # Dicionário para mapear os operadores para suas funções correspondentes
    operadores = {
        "seq": concatenacao,
        "alt": uniao,
        "kle": kleene
    }

    def converter_no(no):
        """
        Função recursiva para converter um nó da árvore de expressão regular num AFND.

        Args:
            no (dict): Um nó da árvore de expressão regular representado como um dicionário Python.

        Returns:
            dict: O AFND resultante do nó convertido.
        """
        if "simb" in no:  # Se o nó representa um símbolo
            # Cria dois novos estados para representar a transição com o símbolo
            estado_inicial = criar_estado()
            estado_final = criar_estado()
            # Define a transição com o símbolo do estado inicial para o estado final
            delta = {estado_inicial: {no["simb"]: [estado_final]}}
            return {
                "Q": [estado_inicial, estado_final],
                "Sigma": {no["simb"]},
                "delta": delta,
                "q0": estado_inicial,
                "F": [estado_final]
            }
        else:  # Se o nó representa um operador
            # Converte recursivamente os argumentos do operador para AFNDs
            sub_afnds = [converter_no(arg) for arg in no["args"]]
            # Aplica a operação correspondente ao operador aos AFNDs convertidos
            return operadores[no["op"]](*sub_afnds)

    # Converte a expressão regular num AFND
    afnd = converter_no(expressao_regular)

    return afnd


def main():
    # Configuração do parser de argumentos
    parser = argparse.ArgumentParser(description="Conversão de expressão regular para AFND")
    parser.add_argument('ficheiro_json', metavar='ficheiro_json', type=str,
                        help='O caminho para o ficheiro JSON contendo a expressão regular')
    parser.add_argument('--output', metavar='ficheiro_afnd_json', type=str,
                        help='O caminho para salvar o AFND em formato JSON')

    # Parse dos argumentos da linha de comando
    args = parser.parse_args()

    # Ler a expressão regular a partir do ficheiro JSON
    expressao_regular = ler_expressao_regular(args.ficheiro_json)

    # Converter a expressão regular num AFND
    afnd = converter_afnd(expressao_regular)

    # Salvar o AFND em formato JSON
    if args.output:
        with open(args.output, 'w') as ficheiro_afnd:
            json.dump(afnd, ficheiro_afnd, indent=4)
            print(f"AFND salvo em '{args.output}'")

if __name__ == "__main__":
    main()
