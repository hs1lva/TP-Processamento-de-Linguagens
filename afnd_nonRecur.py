import json

def converter_expressao_para_afnd(expressao):
   for chave in expressao:
        if chave == 'simb':
            return expressao[chave]
           
        


def escrever_afnd_json(afnd, caminho_arquivo_saida):
    # Obtendo todos os símbolos do alfabeto
    alfabeto = set()
    for transicoes in afnd['transicoes'].values():
        for simbolo in transicoes.keys():
            if simbolo != 'ε':
                alfabeto.add(simbolo)
    
    # Convertendo os conjuntos de estados finais e de transições para o formato especificado
    estados_finais = list(afnd['estados_finais'])
    delta = {}
    for estado, transicoes in afnd['transicoes'].items():
        delta[estado] = {}
        for entrada, destinos in transicoes.items():
            delta[estado][entrada] = list(destinos)

    # Construindo o objeto JSON
    afnd_json = {
        "Q": list(afnd['transicoes'].keys()),  # Estados são as chaves das transições
        "V": list(alfabeto),  # O alfabeto são os símbolos não vazios presentes nas transições
        "q0": afnd['estado_inicial'],
        "F": estados_finais,
        "delta": delta
    }

    # Escrevendo o JSON no arquivo
    with open(caminho_arquivo_saida, 'w') as arquivo_saida:
        json.dump(afnd_json, arquivo_saida, indent=4)


def main(expressao_regular):
    # Chama a função para converter a expressão regular em um AFND
    afnd = converter_expressao_para_afnd(expressao_regular)
    
    #escrever 
    escrever_afnd_json(afnd, 'afnd.json')

    # Verifica se o AFND foi gerado com sucesso
    if afnd:
        # Escreve o AFND no arquivo JSON
        with open('afnd.json', 'w') as arquivo_saida:
            json.dump(afnd, arquivo_saida, indent=4)
        print("AFND gerado com sucesso!")
    else:
        print("Não foi possível gerar o AFND.")

if __name__ == "__main__":
    # Expressão regular fornecida
    expressao_regular = {
        "op": "alt",
        "args": [
            {"simb": "a"},
            {
                "op": "seq",
                "args": [
                    {"simb": "a"},
                    {"op": "kle", "args": [{"simb": "b"}]}
                ]
            }
        ]
    }

    # Chama a função principal
    main(expressao_regular)
