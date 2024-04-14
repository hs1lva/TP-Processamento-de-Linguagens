
## Exemplo de argparser
import argparse

def calculadora(args):
    if args.operador == 'soma':
        return args.numero1 + args.numero2
    elif args.operador == 'subtracao':
        return args.numero1 - args.numero2
    elif args.operador == 'multiplicacao':
        return args.numero1 * args.numero2
    elif args.operador == 'divisao':
        if args.numero2 == 0:
            return "Erro: divisão por 0 não é válido."
        return args.numero1 / args.numero2
    else:
        return "Operador inválido."

def main():
    parser = argparse.ArgumentParser(description='Calculadora')
    parser.add_argument('--operador', type=str, choices=['soma', 'subtracao', 'multiplicacao', 'divisao'],
                        help='Operações permitidas: soma, subtracao, multiplicacao, divisao', required=True)
    
    parser.add_argument('--numero1', type=float, help='Primeiro numero', required=True)
    parser.add_argument('--numero2', type=float, help='Segundo numero', required=True)

    args = parser.parse_args()
    result = calculadora(args)

    print(f"Result: {result}")

if __name__ == "__main__":
    main()
