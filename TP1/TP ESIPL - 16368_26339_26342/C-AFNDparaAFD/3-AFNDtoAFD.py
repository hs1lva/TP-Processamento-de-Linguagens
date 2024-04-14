import json
import argparse

# Recebe um conjunto de estados, um símbolo e um dicionário de transições, e retorna um conjunto de estados alcançáveis
def AFNDtoAFD(automatoAFND : dict) -> dict:

    def encontrar_conjunto(estadoAtual, simbolo, transicoes) -> frozenset:# 'Daqui, até onde posso ir?'
        # Criamos um set, para garantir que não existem estados repetidos
        conjuntoAlcancavel : set = set() 
        for estado in estadoAtual:
            if estado in transicoes and simbolo in transicoes[estado]:
                conjuntoAlcancavel.update(transicoes[estado][simbolo])
        return frozenset(conjuntoAlcancavel)# Retorna um frozenset, que é imutavel



    # A função recebe um conjunto de estados, e um dicionário de transições, e retorna o fecho-ε desse conjunto de estados
    def fecho_epsilon(conjunto : set, transicoes : dict) -> frozenset:
        fecho : set = set(conjunto)

        # Expande recursivamente o fecho épsilon de um estado, 
        #adicionando estados alcançáveis através de transições épsilon a um dado conjunto.
        def expandir_fecho(estado : str):
            if estado in transicoes and 'ε' in transicoes[estado]: # Se o estado tiver transições com o simbolo 'ε'
                for proximoEstado in transicoes[estado]['ε']: # Para cada estado alcançável por uma transição épsilon
                    if proximoEstado not in fecho: # Se o estado ainda não foi visitado
                        fecho.add(proximoEstado) # Adiciona o estado ao fecho
                        expandir_fecho(proximoEstado) # Chama a função recursivamente

        for estado in conjunto:
            expandir_fecho(estado)

        return frozenset(fecho)


    def construir_AFD(listaEstadosAtuais):
        # Declara que as variáveis estão fora do escopo da função, mas podem ser modificadas
        nonlocal estadosAFD, stack, transicoesAFD
        for simbolo in alfabetoAFD:
            listaEstadosAlcancavel : frozenset = encontrar_conjunto(listaEstadosAtuais, simbolo, transicoesAFND)
            listaFechoEpsilon : frozenset = fecho_epsilon(listaEstadosAlcancavel, transicoesAFND)
            if listaFechoEpsilon:
                if listaFechoEpsilon not in estadosAFD.values():
                    estadosAFD[f"N{len(estadosAFD)}"] = listaFechoEpsilon # Adiciona o novo conjunto de estados ao AFD
                    stack.append(listaFechoEpsilon)
                for estado, valor in estadosAFD.items(): # Para cada estado nos estados AFD
                    if valor == listaEstadosAtuais: # Verifica se o valor do conjunto atual é igual ao conjunto do estado
                        conjuntoAtual = estado 
                    if valor == listaFechoEpsilon: 
                        conjuntoAlcancavel = estado
                transicoesAFD.setdefault(conjuntoAtual, {})[simbolo] = conjuntoAlcancavel

        if stack:
            construir_AFD(stack.pop())


    transicoesAFND : dict = automatoAFND['delta']
    estadoInicialAFND : dict = automatoAFND['q0']
    estadosFinaisAFND : set = set(automatoAFND['F'])
    estadosAFD : dict = {}
    alfabetoAFD : list = [simbolo for simbolo in automatoAFND['V'] if simbolo != 'ε']
    transicoesAFD : dict = {}
    stack : list = []

    conjuntoEstadosInicial : frozenset = fecho_epsilon({estadoInicialAFND}, transicoesAFND)
    estadosAFD[f"N{len(estadosAFD)}"] = conjuntoEstadosInicial # Cria o novo estado no AFD
    stack.append(conjuntoEstadosInicial)

    construir_AFD(stack.pop())
    
    estadosFinaisAFD = []
    for estado, conjunto in estadosAFD.items():
        if conjunto.intersection(estadosFinaisAFND):
            estadosFinaisAFD.append(estado)


    afd = {
        "Q": list(estadosAFD.keys()),
        "V": alfabetoAFD,
        "q0": "N0",
        "F": estadosFinaisAFD,
        "delta": transicoesAFD
    }
    return afd

# Carrega um autómato de um ficheiro JSON
def carrega_automato(ficheiro_automato : str) -> dict:
    with open(ficheiro_automato, 'r', encoding='utf-8') as ficheiro:
        return json.load(ficheiro)

# Grava um autómato num ficheiro JSON
def gravar_automato(afd, ficheiro_automato : str) -> None:
    with open(ficheiro_automato, 'w' , encoding='utf-8') as ficheiro:
        json.dump(afd, ficheiro, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Conversão de AFND para AFD")
    parser.add_argument("ficheiro_json", 
                        help="O caminho para o ficheiro JSON contendo a definição do AFND")
    parser.add_argument('-output', metavar='palavra', type=str,
                        help='Output JSON do AFD')

    args : argparse.Namespace = parser.parse_args()

    automatoAFND : dict = carrega_automato(args.ficheiro_json)
    automatoAFD : dict = AFNDtoAFD(automatoAFND)
    gravar_automato(automatoAFD, args.output)

if __name__ == "__main__":
    main()
