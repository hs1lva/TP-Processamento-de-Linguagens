import json

def ler_expressao_regular(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        expressao_regular = json.load(arquivo)
    return expressao_regular

def converter_expressao_para_afnd(expressao, contador=[0]):
    if 'simb' in expressao:
        estado_inicial = 'q' + str(contador[0])
        estado_final = 'q' + str(contador[0] + 1)
        transicoes = {
            estado_inicial: {expressao['simb']: {estado_final}}
        }
        contador[0] += 2  # Incrementa o contador para garantir nomes únicos para os estados
        return {
            'estados': {estado_inicial, estado_final},
            'transicoes': transicoes
        }
    else:
        op = expressao['op']
        args = expressao['args']
        if op == 'alt':
            afnds = [converter_expressao_para_afnd(arg, contador) for arg in args]
            return unir_afnds(afnds)
        elif op == 'seq':
            afnds = [converter_expressao_para_afnd(arg, contador) for arg in args]
            return concatenar_afnds(afnds)
        elif op == 'kle':
            afnd = converter_expressao_para_afnd(args[0], contador)  # Acesse o primeiro argumento da lista 'args'
            return fecho_kleene_afnd(afnd)



def unir_afnds(afnds):
    novo_estado_inicial = 'q0'
    novo_estado_final = 'qf'
    transicoes = {novo_estado_inicial: {}}
    estados_finais = set()

    for afnd in afnds:
        transicoes[novo_estado_inicial].setdefault('ε', set()).add(afnd['estado_inicial'])
        transicoes.update(afnd['transicoes'])
        estados_finais |= afnd['estados_finais']

    transicoes.update({estado_final: {'ε': {novo_estado_final}} for estado_final in estados_finais})

    return {
        'estado_inicial': novo_estado_inicial,
        'estados_finais': estados_finais,
        'transicoes': transicoes
    }

def concatenar_afnds(afnds):
    estados_finais = set()
    transicoes = {}
    estado_inicial = afnds[0]['estado_inicial']

    # Iterar sobre todos os AFNDs na lista
    for afnd in afnds:
        # Adicionar as transições do AFND atual ao novo AFND
        transicoes.update(afnd['transicoes'])

        # Verificar se o AFND atual tem estados finais
        if 'estados_finais' in afnd:
            # Adicionar os estados finais do AFND atual ao conjunto de estados finais do novo AFND
            estados_finais |= afnd['estados_finais']

    return {
        'estado_inicial': estado_inicial,
        'estados_finais': estados_finais,
        'transicoes': transicoes
    }



def fecho_kleene_afnd(afnd):
    estados = list(afnd['estados'])
    transicoes = afnd['transicoes'].copy()  # Faça uma cópia das transições para não modificar o AFND original

    transicoes = {estados[0]: {'ε':[estados[0], estados[1]]} for estados in estados}
    # Adicione uma transição ε do novo estado inicial para o estado inicial original do AFND
    # transicoes.setdefault(estados[0], {}).setdefault('ε', set()).add(afnd['estado_inicial'])


    # Adicione uma transição ε dos estados finais do AFND para o novo estado final
    # for estado_final in afnd['estados']:
    #     transicoes.setdefault(estado_final, {}).setdefault('ε', set()).add(estados[1])

    return {
        'estado_inicial': estados[0],
        'estados_finais': {estados[1]},
        'transicoes': transicoes
    }





import json

import json

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


def main(caminho_arquivo_entrada, caminho_arquivo_saida):
    expressao_regular = ler_expressao_regular(caminho_arquivo_entrada)
    afnd = converter_expressao_para_afnd(expressao_regular)
    escrever_afnd_json(afnd, caminho_arquivo_saida)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Converte uma expressão regular para um AFND")
    parser.add_argument('caminho_arquivo_entrada', metavar='caminho_arquivo_entrada', type=str,
                        help='O caminho para o arquivo JSON contendo a expressão regular')
    parser.add_argument('--output', metavar='caminho_arquivo_saida', type=str, default='afnd.json',
                        help='O caminho para o arquivo de saída JSON do AFND (default: afnd.json)')
    args = parser.parse_args()
    
    main(args.caminho_arquivo_entrada, args.output)

    print("AFND gerado com sucesso!")
