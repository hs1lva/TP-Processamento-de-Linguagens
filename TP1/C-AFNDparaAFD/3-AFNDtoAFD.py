import json
import argparse


def ConverterAFNDParaAFD(automatoAFND):
    #Função para obter conjunto de estados alcansaveis apartir de um conjunto de estado apartir de um simbolo -- del comment
    def EncontrarConjuntoAlcancavel(estadoAtual, simbolo, transicoes):
        # Define o conjunto de estados alcansaveis apartir de um simbolo -- del comment

        # Criamos um set, para garantir que não existem estados repetidos
        conjuntoAlcancavel = set() 
        for estado in estadoAtual:
            if estado in transicoes and simbolo in transicoes[estado]:
                conjuntoAlcancavel.update(transicoes[estado][simbolo])
        return frozenset(conjuntoAlcancavel) # Retorna um frozenset, que é imutavel

    # Função para obter o fecho-ε de um conjunto de estados -- del comment
    def FechoEpsilon(conjunto, transicoes):
        fecho : set = set(conjunto)
        pilha : list = list(conjunto)
        while pilha: # Enquanto existir alguma coisa na pilha
            estado = pilha.pop() # Guarda o ultimo estado e retira esse elemento da pilha
            if estado in transicoes and 'ε' in transicoes[estado]: # Se o estado tiver transições com o simbolo 'ε'
                for proximoEstado in transicoes[estado]['ε']:
                    if proximoEstado not in fecho:
                        fecho.add(proximoEstado)
                        pilha.append(proximoEstado)
        return frozenset(fecho) # Retorna um frozenset, que é imutavel

    # Inicializações -- del comment

    estadosAFND = set(automatoAFND['Q'])
    transicoesAFND = automatoAFND['delta']
    estadoInicialAFND = automatoAFND['q0']
    estadosFinaisAFND = set(automatoAFND['F'])
    estadosAFD = {}
    alfabetoAFD = [simbolo for simbolo in automatoAFND['V'] if simbolo != 'ε']

    # alfabetoAFD = {}
    # for simbolo in automatoAFND['V']:
    #     if simbolo != 'ε':
    #         alfabetoAFD[simbolo] = None


    transicoesAFD = {}
    pilha = []
   
   #Obter o conjunto de estados inicial apartir do fecho epsilon -- del comment
   # Primeiro fazemos o fecho epsilon do estado inicial do AFND
    conjuntoEstadosInicial= FechoEpsilon({estadoInicialAFND}, transicoesAFND)
    estadosAFD[f"N{len(estadosAFD)}"]=conjuntoEstadosInicial # Adicionamos o conjunto de estados inicial ao AFD
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

    # Identifica estados finais do AFD -- del comment
    estadosFinaisAFD = []
    for conjunto in estadosAFD.values():
        if conjunto.intersection(estadosFinaisAFND):
            for estadoAFD, valor in estadosAFD.items():
                if valor == conjunto:
                    estadosFinaisAFD.append(estadoAFD)

    # Constrói o AFD -- del comment
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
        json.dump(afd, ficheiro,ensure_ascii=False, indent=4)

def main():
    # Configuração do parser de argumentos -- del comment
    parser = argparse.ArgumentParser(description="Conversão de AFND para AFD")
    parser.add_argument("ficheiro_json", 
                        help="O caminho para o ficheiro JSON contendo a definição do AFND")
    parser.add_argument('-output', metavar='palavra', type=str,
                        help='Output JSON do AFD')

    # Parse dos argumentos da linha de comando 
    args : argparse.Namespace = parser.parse_args()

    # Ler ficheiro JSON
    automatoAFND :dict = CarregarAutomatoAFND(args.ficheiro_json)
    # Converter AFND para AFD
    automatoAFD : dict = ConverterAFNDParaAFD(automatoAFND)
    # Gravar AFD em ficheiro JSON
    gravar_automato(automatoAFD, args.output)

    #Para testar sem o argParse
    # afnd = ler_afnd("afnd_expressao2.json")
    # afd = converter_afnd_para_afd(afnd)
    # escrever_afd(afd, "afd_expressao2.json")

if __name__ == "__main__":
    main()

# Testar com argparse
# python .\3-AFNDtoAFD.py ..\automatoAFND.json      
