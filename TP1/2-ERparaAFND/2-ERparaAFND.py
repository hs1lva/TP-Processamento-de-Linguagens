import json
import argparse

def converter_afnd(expressao_regular):
    """
    Converte uma expressão regular em um autômato finito não determinístico (AFND) equivalente.

    Args:
        expressao_regular (str): A expressão regular fornecida como uma string.

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
        Realiza a operação de fecho de Kleene em um AFND.

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
        Função recursiva para converter um nó da árvore de expressão regular em um AFND.

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

    # Converte a expressão regular em um AFND
    afnd = converter_no(expressao_regular)

    return afnd

def main():
    # Configuração do parser de argumentos
    parser = argparse.ArgumentParser(description="Conversão de expressão regular para AFND")
    parser.add_argument('er_file', metavar='er_file', type=str,
                        help='O arquivo JSON contendo a expressão regular')

    # Parse dos argumentos da linha de comando
    args = parser.parse_args()

    # Ler a expressão regular do arquivo JSON
    with open(args.er_file, 'r') as file:
        expressao_regular = json.load(file)

    # Converter a expressão regular fornecida em um AFND
    afnd = converter_afnd(expressao_regular)

    # Converter o alfabeto para uma lista antes de serializar para JSON
    afnd["Sigma"] = list(afnd["Sigma"])

    # Imprimir o AFND resultante
    print(json.dumps(afnd, indent=4))

if __name__ == "__main__":
    main()

# Exemplo de uso (dentro da pasta 2-ERparaAFND):
# python 2-ERparaAFND.py er.json