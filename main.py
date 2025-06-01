import pandas as pd
from BinaryTree import BinaryTree

binaryTree = BinaryTree(dbUrl='./database.json')

def searchByArea(area):
    result = binaryTree.search(area=area)
    if result is not None:
      print('\n')
      print(f"Área '{area}' encontrada na árvore.")
      print('\n')
      df = pd.DataFrame({
            'Área': [area],
            'Pontos': [result[area]],
            'Animais': [', '.join(result['animals'])]
        })
      print(df)
    else:
        print(f"Área '{area}' não encontrada na árvore.")

def searchByValue(value):
    result = binaryTree.search(value=value)
    if result is not None:
        rows = []
        print(f"Valor '{value}' encontrado na árvore.")
        print('\n')
        for area_name, info in result.items():
            rows.append({
                'Área': area_name,
                'Pontos': info['TotalPoints'],
                'Animais': ', '.join(info['animals'])
            })
        df = pd.DataFrame(rows)
        print(df)
    else:
        print(f"Valor '{value}' não encontrado na árvore.")

def main_menu():
    while True:
        print("\n=== Menu de Pesquisa na Árvore Binária ===")
        print("1 - Buscar por Área")
        print("2 - Buscar por Valor")
        print("3 - Visualizar árvore")
        print("0 - Sair")
        
        choice = input("Escolha uma opção: ").strip()
        
        if choice == '1':
            area = input("Digite o nome da área (ex: Rio de Janeiro): ").strip()
            searchByArea(area)
        elif choice == '2':
            value_str = input("Digite o valor numérico a buscar: ").strip()
            if value_str.isdigit():
                value = int(value_str)
                print('\n')
                searchByValue(value)
                print('\n')
            else:
                print("Por favor, digite um número válido.")
        elif choice == '3':
            try:
                binaryTree.visualize()
                input('Pressione Enter para continuar...')
            except Exception as e:
                print(f'Não foi possível visualizar a árvore: {e}')
        elif choice == '0':
            print("Saindo... Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main_menu()