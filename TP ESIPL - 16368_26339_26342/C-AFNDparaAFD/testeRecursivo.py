import json
import argparse

def ConverterAFNDParaAFD(automatoAFND):
    # Função para obter conjunto de estados alcansaveis a partir de um conjunto de estado a partir de um símbolo
    def EncontrarConjuntoAlcancavel(estadoAtual, simbolo, transicoes):
        conjuntoAlcancavel = set() 
        for estado in estadoAtual:
            if estado in transicoes and simbolo in transicoes[estado]:
                conjuntoAlcancavel.update(transicoes[estado][simbolo])
        return frozenset(conjuntoAlcancavel)

    # Função para obter o fecho-ε de um conjunto de estados
    def FechoEpsilon(conjunto, transicoes):
        fecho = set(conjunto)

        def expandir_fecho(estado):
            if estado in transicoes and 'ε' in transicoes[estado]:
                for proximoEstado in transicoes[estado]['ε']:
                    if proximoEstado not in fecho:
                        fecho.add(proximoEstado)
                        expandir_fecho(proximoEstado)

        for estado in conjunto:
            expandir_fecho(estado)

        return frozenset(fecho)


    # Função auxiliar para construir o AFD recursivamente
    def ConstruirAFD(conjuntoEstadosAtual):
        nonlocal estadosAFD, pilha, transicoesAFD
        for simbolo in alfabetoAFD:
            conjuntoEstadosAlcancavel = EncontrarConjuntoAlcancavel(conjuntoEstadosAtual, simbolo, transicoesAFND)
            fechoEpsilonConjuntoEstadosAlcancavel = FechoEpsilon(conjuntoEstadosAlcancavel, transicoesAFND)
            if fechoEpsilonConjuntoEstadosAlcancavel:
                if fechoEpsilonConjuntoEstadosAlcancavel not in estadosAFD.values():
                    estadosAFD[f"N{len(estadosAFD)}"] = fechoEpsilonConjuntoEstadosAlcancavel
                    pilha.append(fechoEpsilonConjuntoEstadosAlcancavel)
                for estadoAFD, valor in estadosAFD.items():
                    if valor == conjuntoEstadosAtual:
                        conjuntoAtualID = estadoAFD
                    if valor == fechoEpsilonConjuntoEstadosAlcancavel:
                        conjuntoAlcancavelID = estadoAFD
                transicoesAFD.setdefault(conjuntoAtualID, {})[simbolo] = conjuntoAlcancavelID
        if pilha:
            ConstruirAFD(pilha.pop())

    # Inicializações
    estadosAFND = set(automatoAFND['Q'])
    transicoesAFND = automatoAFND['delta']
    estadoInicialAFND = automatoAFND['q0']
    estadosFinaisAFND = set(automatoAFND['F'])
    estadosAFD = {}
    alfabetoAFD = [simbolo for simbolo in automatoAFND['V'] if simbolo != 'ε']
    transicoesAFD = {}
    pilha = []

    conjuntoEstadosInicial = FechoEpsilon({estadoInicialAFND}, transicoesAFND)
    estadosAFD[f"N{len(estadosAFD)}"] = conjuntoEstadosInicial
    pilha.append(conjuntoEstadosInicial)

    ConstruirAFD(pilha.pop())

    estadosFinaisAFD = [estado for estado, conjunto in estadosAFD.items() if conjunto.intersection(estadosFinaisAFND)]

    afd = {
        "Q": list(estadosAFD.keys()),
        "V": alfabetoAFD,
        "q0": "N0",
        "F": estadosFinaisAFD,
        "delta": transicoesAFD
    }
    return afd

def CarregarAutomatoAFND(caminhoAutomatoAFND) -> dict:
    with open(caminhoAutomatoAFND, 'r', encoding='utf-8') as ficheiro:
        return json.load(ficheiro)

def gravar_automato(afd, caminhoAutomatoAFD) -> None:
    with open(caminhoAutomatoAFD, 'w' , encoding='utf-8') as ficheiro:
        json.dump(afd, ficheiro, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Conversão de AFND para AFD")
    parser.add_argument("ficheiro_json", 
                        help="O caminho para o ficheiro JSON contendo a definição do AFND")
    parser.add_argument('-output', metavar='palavra', type=str,
                        help='Output JSON do AFD')

    args = parser.parse_args()

    automatoAFND = CarregarAutomatoAFND(args.ficheiro_json)
    automatoAFD = ConverterAFNDParaAFD(automatoAFND)
    gravar_automato(automatoAFD, args.output)

if __name__ == "__main__":
    main()
