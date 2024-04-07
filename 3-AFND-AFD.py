import json
import graphviz
import argparse


def carregar_automato(ficheiro_definicao : str) -> dict:
    # Carrega o automato a partir do ficheiro JSON
    with open(ficheiro_definicao, 'r') as ficheiro:
        return json.load(ficheiro)

def validaAutomato(automato: dict) -> dict:
    # Verifica se é dicionario
    if not isinstance(automato, dict):
        exit("O ficheiro JSON deve ser um dicionário.")


    # Verifica se automato tem estados finais
    if automato['F'] == '':
        exit("O automato não tem estados finais definidos.")
    #Verifica se estados finais existem no automato
    if not all(estado in automato['delta'].keys() for estado in automato['F']):
        exit("O automato não tem todos os estados finais definidos.")
        
    # Verifica se automato tem estados
    # Se não tiver nenhum, adiciona os estados. Se tiver verifica se tem todos
    if not automato['Q']:
        automato['Q'] = sorted(list(set(automato['delta'].keys())))
    else:
        # Verifica se Q tem todos os estados que estão em delta
        if not all(estado in automato['delta'].keys() for estado in automato['Q']):
            exit(f"O automato não tem todos os estados definidos.")
    
    # Verifica V 
    if not automato['V']:
        automato['V'] = []
        for transitions in automato['delta'].values():
            for transition in transitions.keys():
                automato['V'].append(transition)
        automato['V'] = sorted(list(set(automato['V'])))

    if 'ε' in automato['V']:
        exit("O automato não é AFD, porque o simbolo 'ε' está em V.")#verificar se paramos o programa ou se apenas avisamos o user
        pass

    # Verifica se existe mais do que 1 transicao para o mesmo simbolo
    for transitions in automato['delta'].values():
        for destinations in transitions.values():
            if isinstance(destinations, list) and len(destinations) > 1:
                exit("O automato é AFND, porque existe mais do que uma transição para o mesmo simbolo.")

    return automato

def gerar_grafo(automato: dict) -> graphviz.Digraph:

    # Cria o grafo
    grafo: graphviz.Digraph = graphviz.Digraph(format='png')
    # Adiciona os estados ao grafo
    for estado in automato['Q']:
        if estado in automato['F']:
            grafo.node(estado, shape='doublecircle')
        else:
            grafo.node(estado, shape='circle')

    # Adiciona as transições ao grafo
    for estado, trans in automato['delta'].items():
        for simbolo, prox_estado in trans.items():
            grafo.edge(estado, prox_estado, label=simbolo)

    return grafo

def gravar_automato(automato: dict, ficheiro_automato: str) -> None:
    with open(ficheiro_automato, 'w') as ficheiro:
        json.dump(automato, ficheiro, indent=4)


def converter_afnd_afd(automato: dict) -> dict:
    afd : dict = {
        'Q': [],
        'V': [],
        'q0': 'n0',
        'F': [],
        'delta': {}
    }
    
    pass

def main():
    parser : argparse.ArgumentParser = argparse.ArgumentParser(description="Implementação de AFD")
    parser.add_argument('ficheiro_json', metavar='ficheiro_json', type=str,
                        help='O caminho para o ficheiro JSON contendo a definição do AFD')
    parser.add_argument('-graphviz', action='store_true',
                        help='Gerar a representação gráfica do grafo')
    parser.add_argument('-output', metavar='palavra', type=str,
                        help='Output JSON do AFD')

    args : argparse.Namespace = parser.parse_args()

    automato : dict = carregar_automato(args.ficheiro_json)
    #automato = validaAutomato(automato)

    if args.graphviz:
        grafo : graphviz.Digraph = gerar_grafo(automato)
        #verificar se é necessario gerar um ficheiro txt com estes dados
        print(grafo.source)  # Imprime a representação do grafo em formato DOT
        grafo.render('automatoAFD', view=True)  # Guarda e mostra o grafo em formato PNG

    if args.output:
        afd : dict = converter_afnd_afd(automato)
        gravar_automato(afd, args.output)

if __name__ == "__main__":
    main()
