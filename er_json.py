import json

def converter_er_para_json(expressao_regular):
    if len(expressao_regular) == 1:
        return {"simb": expressao_regular}
    else:
        operadores = {'|': 'alt', '.': 'seq', '*': 'kle'}
        if expressao_regular[0] == '(' and expressao_regular[-1] == ')':
            expressao_regular = expressao_regular[1:-1]
        for operador, op in operadores.items():
            nivel = 0
            for i, c in enumerate(reversed(expressao_regular)):
                if c == ')':
                    nivel += 1
                elif c == '(':
                    nivel -= 1
                elif nivel == 0 and c == operador:
                    return {
                        "op": op,
                        "args": [
                            converter_er_para_json(expressao_regular[:len(expressao_regular)-i-1]),
                            converter_er_para_json(expressao_regular[len(expressao_regular)-i:])
                        ]
                    }
        if expressao_regular[0] == '(' and expressao_regular[-1] == ')':
            expressao_regular = expressao_regular[1:-1]
        return converter_er_para_json(expressao_regular[1:])  # Remove o primeiro caractere e tenta novamente

def salvar_json(data, caminho_arquivo):
    with open(caminho_arquivo, 'w') as arquivo:
        json.dump(data, arquivo, indent=4)

#expressao_regular = "a|(ab*)"
expressao_regular = "a*"

json_data = converter_er_para_json(expressao_regular)
salvar_json(json_data, 'expressao_regular.json')
