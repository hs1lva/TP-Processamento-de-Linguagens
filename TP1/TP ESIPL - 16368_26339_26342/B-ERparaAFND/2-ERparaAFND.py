import json
import argparse

# Função para converter uma expressão regular num automato finito não determinístico (AFND)
# Args : expressao_regular (str) : expressão regular como uma string
# Returns : dict : AFND como um dicionário Python
def converter_afnd(expressao_regular):

    # Função para criar um novo estado único
    def criar_estado():
        
        nonlocal contador_estado # Variável não local para manter o contador de estados
        estado = f"q{contador_estado}" # Cria um novo estado único
        contador_estado += 1 # Incrementa o contador de estados
        return estado 

    # Funções para realizar as operações de concatenação entre AFNDs
    # Args : afnd1 (dict) : O primeiro AFND como um dicionário Python
    #        afnd2 (dict) : O segundo AFND como um dicionário Python
    # Returns : dict : O AFND resultante da concatenação
    def concatenacao(afnd1, afnd2):
        
        # Adiciona transições vazias do estado final de afnd1 para o estado inicial de afnd2
        for estado_final in afnd1["F"]:
            afnd1["delta"].setdefault(estado_final, {}).update({"" : [afnd2["q0"]]})

        # Atualiza os estados finais do AFND resultante
        afnd1["F"] = afnd2["F"]

        # Atualiza as transições do AFND resultante
        afnd1["delta"].update(afnd2["delta"])

        return afnd1

    # Função para realizar a operação de união entre dois AFNDs
    # Args : afnd1 (dict) : O primeiro AFND como um dicionário Python
    #        afnd2 (dict) : O segundo AFND como um dicionário Python
    # Returns : dict : O AFND resultante da união
    def uniao(afnd1, afnd2):
        
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

    # Função para realizar a operação de fecho de Kleene num AFND
    # Args : afnd (dict) : O AFND como um dicionário Python
    # Returns : dict : O AFND resultante do fecho de Kleene
    def kleene(afnd):
        
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

    # Função para realizar a operação de transição vazia num AFND, para usar o trans (transição vazia) na expressão regular
    # Args : afnd (dict) : O AFND como um dicionário Python
    # Returns : dict : O AFND resultante da transição vazia
    def transicao_vazia(afnd):
        novo_estado_inicial = criar_estado()
        novo_estado_final = criar_estado()
        novo_delta = {"": [novo_estado_final]}
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

    # Dicionário para mapear as operações
    operadores = {
        "seq": concatenacao,
        "alt": uniao,
        "kle": kleene,
        "trans": transicao_vazia  # Adiciona a operação de transição vazia - função transicao_vazia
    }

    # Função recursiva para converter um estado da expressão regular num AFND
    # Args : estadoER (dict) : Um estado da expressão regular como um dicionário Python
    # Returns : dict : O AFND resultante do nó convertido
    def converter_estadoER(estadoER):
        
        if "simb" in estadoER:  # Se o nó representa um símbolo então...

            # Cria dois novos estados para representar a transição com o símbolo
            estado_inicial = criar_estado()
            estado_final = criar_estado()

            # Define a transição com o símbolo do estado inicial para o estado final
            delta = {estado_inicial: {estadoER["simb"]: [estado_final]}}
            return {
                "Q": [estado_inicial, estado_final],
                "Sigma": {estadoER["simb"]},
                "delta": delta,
                "q0": estado_inicial,
                "F": [estado_final]
            }
        
        else:  # Se o nó representa um operador (seq, alt ou kle) então...

            # Converte recursivamente os argumentos do operador para AFNDs
            sub_afnds = [converter_estadoER(arg) for arg in estadoER["args"]]

            # Aplica a operação correspondente ao operador aos AFNDs convertidos
            return operadores[estadoER["op"]](*sub_afnds)

    # Converte a expressão regular num AFND
    afnd = converter_estadoER(expressao_regular)

    return afnd

def gravar_automato(automato: dict, ficheiro_automato: str) -> None:
    with open(ficheiro_automato, 'w') as ficheiro:
        json.dump(automato, ficheiro, indent=4)

def main():

    # Configuração do parser de argumentos
    parser = argparse.ArgumentParser(description="Conversão de expressão regular para AFND")
    parser.add_argument('er_file', metavar='er_file', type=str,
                        help='O ficheiro JSON com a expressão regular')
    
    parser.add_argument('-output', metavar='palavra', type=str,
                        help='Output JSON do AFD')

    
    # Parse dos argumentos da linha de comando
    args : argparse.Namespace = parser.parse_args()

    # Ler a expressão regular do ficheiro JSON
    with open(args.er_file, 'r') as file:
        expressao_regular = json.load(file)

    # Converter a expressão regular num AFND
    afnd = converter_afnd(expressao_regular)

    # Converter o alfabeto para uma lista antes de serializar para JSON
    afnd["Sigma"] = list(afnd["Sigma"])

    # Imprimir o AFND resultante (json.dumps converte o dicionário Python para uma string JSON)
    print(json.dumps(afnd, indent=4)) # indent=4 para imprimir o JSON de uma forma mais legível

    #Grava o AFND num ficheiro 
    gravar_automato(afnd, args.output)
    print(f"Ficheiro criado")

if __name__ == "__main__":
    main()

# Exemplo de uso (dentro da pasta 2-ERparaAFND):
# python 2-ERparaAFND.py er.json -output output.json
