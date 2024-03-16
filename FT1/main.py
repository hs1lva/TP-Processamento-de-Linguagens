import pandas as pd

def guardar_notas() -> None:
    notas_UCS: dict = {
        "AMS": 10,
        "POO": 11,
        "AAD": 12,
        "Fisica": 13,
        "PES": 14
    }
    media: float = sum(notas_UCS.values()) / len(notas_UCS)
    print("Média das notas:", media)
    with open("notas_UCS.txt", "w") as file:
        for ucs, nota in notas_UCS.items():
            file.write(f"{ucs}: {nota}\n")
        file.write(f"Média: {media}")

def ler_exportar_excel() -> None:
    notas_UCS_lidas: dict = {}
    with open("notas_UCS.txt", "r") as file:
        for line in file:
            if ":" in line:
                ucs, nota = line.strip().split(": ")
                notas_UCS_lidas[ucs] = int(nota)
            elif "Média" in line:
                media_lida: float = float(line.split(": ")[1])
    df_notas_UCS: pd.DataFrame = pd.DataFrame(list(notas_UCS_lidas.items()), columns=["UCS", "Nota"])
    df_notas_UCS.to_excel("notas_UCS.xlsx", index=False)
    print("Dados exportados para notas_UCS.xlsx")

def criar_dic_listas() -> None:
    carros: dict = {
        "Toyota": ["Corolla", "Yaris", "Rav4"],
        "Volkswagen": ["Golf", "Polo", "Passat"],
        "Ford": ["Fiesta", "Focus", "Mustang"],
        "BMW": ["X3", "3 Series", "5 Series"],
        "Mercedes-Benz": ["C-Class", "E-Class", "S-Class"]
    }
    carros_com_ano: dict = {}
    for marca, modelos in carros.items():
        modelos_com_ano: list = [(modelo, 2020) for modelo in modelos]  # Ano de lançamento fictício
        carros_com_ano[marca] = modelos_com_ano
    for marca, modelos_com_ano in carros_com_ano.items():
        print(marca + ":")
        for modelo, ano in modelos_com_ano:
            print(f"   {modelo} - Ano de lançamento: {ano}")

def menu() -> None:
    while True:
        print("\nMenu:")
        print("1. Guardar notas e calcular média")
        print("2. Exportar notas para Excel")
        print("3. Criar dicionário de listas de carros")
        print("4. Sair")
        escolha: str = input("Escolha uma opção: ")

        if escolha == "1":
            guardar_notas()
        elif escolha == "2":
            ler_exportar_excel()
        elif escolha == "3":
            criar_dic_listas()
        elif escolha == "4":
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

if __name__ == "__main__":
    menu()
