import json
import argparse


def ConverterAFNDParaAFD(automatoAFND):
    #Função para obter conjunto de estados alcansaveis apartir de um conjunto de estado apartir de um simbolo
    def EncontrarConjuntoAlcancavel(estadoAtual, simbolo, transicoes):
        conjuntoAlcancavel = set()
        for estado in estadoAtual:
            if estado in transicoes and simbolo in transicoes[estado]:
                conjuntoAlcancavel.update(transicoes[estado][simbolo])
        return frozenset(conjuntoAlcancavel)

    # Função para obter o fecho-ε de um conjunto de estados
    def FechoEpsilon(conjunto, transicoes):
        fecho = set(conjunto)
        pilha = list(conjunto)
        while pilha:
            estado = pilha.pop()
            if estado in transicoes and 'ε' in transicoes[estado]:
                for proximoEstado in transicoes[estado]['ε']:
                    if proximoEstado not in fecho:
                        fecho.add(proximoEstado)
                        pilha.append(proximoEstado)
        return frozenset(fecho)

    # Inicializações
    estadosAFND = set(automatoAFND['Q'])
    transicoesAFND = automatoAFND['delta']
    estadoInicialAFND = automatoAFND['q0']
    estadosFinaisAFND = set(automatoAFND['F'])
    estadosAFD = {}
    alfabetoAFD = [simbolo for simbolo in automatoAFND['V'] if simbolo != 'ε']
    transicoesAFD = {}
    pilha = []
   
   #Obter o conjunto de estados inicial apartir do fecho epsilon
    conjuntoEstadosInicial= FechoEpsilon({estadoInicialAFND}, transicoesAFND)
    estadosAFD[f"N{len(estadosAFD)}"]=conjuntoEstadosInicial
    pilha.append(conjuntoEstadosInicial)

    while pilha:
        conjuntoEstadosAtual = pilha.pop()
        for simbolo in alfabetoAFD:
            conjuntoEstadosAlcancavel = EncontrarConjuntoAlcancavel(conjuntoEstadosAtual, simbolo, transicoesAFND)
            fechoEpsilonConjuntoEstadosAlcancavel = FechoEpsilon(conjuntoEstadosAlcancavel, transicoesAFND)
            if fechoEpsilonConjuntoEstadosAlcancavel:
                if fechoEpsilonConjuntoEstadosAlcancavel not in estadosAFD.values():
                    estadosAFD[f"N{len(estadosAFD)}"]=fechoEpsilonConjuntoEstadosAlcancavel
                    pilha.append(fechoEpsilonConjuntoEstadosAlcancavel)

                for estadoAFD, valor in estadosAFD.items():
                    if valor == conjuntoEstadosAtual:
                           conjuntoAtualID=estadoAFD
                    if valor == fechoEpsilonConjuntoEstadosAlcancavel:
                           conjuntoAlcancavelID=estadoAFD

                transicoesAFD.setdefault(conjuntoAtualID, {})[simbolo] = conjuntoAlcancavelID

    # Identifica estados finais do AFD
    estadosFinaisAFD = []
    for conjunto in estadosAFD.values():
        if conjunto.intersection(estadosFinaisAFND):
            for estadoAFD, valor in estadosAFD.items():
                if valor == conjunto:
                    estadosFinaisAFD.append(estadoAFD)

    # Constrói o AFD
    afd = {
        "Q": list(estadosAFD.keys()),
        "V": alfabetoAFD,
        "q0": "N0",
        "F": estadosFinaisAFD,
        "delta": transicoesAFD
    }
    return afd


def CarregarAutomatoAFND(caminhoAutomatoAFND):
    with open(caminhoAutomatoAFND, 'r', encoding='utf-8') as ficheiro:
        return json.load(ficheiro)

def ImprimirAutomatoAFD(afd, caminhoAutomatoAFD):
    with open(caminhoAutomatoAFD, 'w' , encoding='utf-8') as ficheiro:
        json.dump(afd, ficheiro,ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Conversor de automato AFND para AFD")
    parser.add_argument("ficheiroAutomatoAFND", help="Ficheiro JSON do automato AFND")
    parser.add_argument("--output", "-o",metavar="ficheiroAutomatoAFD", help="Ficheiro de saida para o automato AFD", default="afd.json")
    args = parser.parse_args()

    automatoAFND = CarregarAutomatoAFND(args.ficheiroAutomatoAFND)
    automatoAFD = ConverterAFNDParaAFD(automatoAFND)
    ImprimirAutomatoAFD(automatoAFD, args.output)

    #Para testar sem o argParse
    # afnd = ler_afnd("afnd_expressao2.json")
    # afd = converter_afnd_para_afd(afnd)
    # escrever_afd(afd, "afd_expressao2.json")

if __name__ == "__main__":
    main()
