import json
import argparse
import graphviz

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

def reconhecer_palavra(automato : dict, palavra : str) -> tuple[bool, list, str]:
    estado_atual : str = automato['q0']
    caminho : list = [estado_atual]

    for char in palavra:
        try:
            prox_estado : str = automato['delta'][estado_atual][char]
            caminho.append(prox_estado)
            estado_atual = prox_estado
        except KeyError:
            return False, caminho, f"Não há transição do estado {estado_atual} com o símbolo '{char}'."

    if estado_atual in automato['F']:
        return True, caminho, None
    else:
        return False, caminho, f"O estado {estado_atual} não é um estado final."

def main():
    parser : argparse.ArgumentParser = argparse.ArgumentParser(description="Implementação de AFD")
    parser.add_argument('ficheiro_json', metavar='ficheiro_json', type=str,
                        help='O caminho para o ficheiro JSON contendo a definição do AFD')
    parser.add_argument('-graphviz', action='store_true',
                        help='Gerar a representação gráfica do grafo')
    parser.add_argument('-rec', metavar='palavra', type=str,
                        help='Reconhecer uma palavra')

    args : argparse.Namespace = parser.parse_args()

    automato : dict = carregar_automato(args.ficheiro_json)
    automato = validaAutomato(automato)

    if args.graphviz:
        grafo : graphviz.Digraph = gerar_grafo(automato)
        #verificar se é necessario gerar um ficheiro txt com estes dados
        print(grafo.source)  # Imprime a representação do grafo em formato DOT
        grafo.render('automatoAFD', view=True)  # Guarda e mostra o grafo em formato PNG

    if args.rec:
        reconhecido, caminho, erro = reconhecer_palavra(automato, args.rec)
        if reconhecido:
            print(f"A palavra '{args.rec}' é reconhecida.")
            print("Caminho percorrido:", ' -> '.join(caminho))
        else:
            print(f"A palavra '{args.rec}' não é reconhecida.")
            print("Situação de erro:", erro)

if __name__ == "__main__":
    main()

# venv/scripts/activate
# Terminal ----> python3 1-AFD.py automato.json -graphviz (criar grafo png)
# Terminal ----> python3 1-AFD.py automato.json -rec 101 (reconhecer palavra)