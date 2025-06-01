import json
from graphviz import Digraph
import pandas as pd
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
    
    def __str__(self):
        return str(self.data)

class BinaryTree:
    def __init__(self, data=None, dbUrl=None):
        self.root = None
        self.areas = {}

        if dbUrl:
            self._load_from_db(dbUrl)
        elif data:
            self.root = Node(data)
    
    def _load_from_db(self, dbUrl):
        with open(dbUrl, 'r') as db_file:
            data = json.load(db_file)
            
            # Montar dados para DataFrame
            rows = []
            for area_name, area_data in data.items():
                animals = area_data['animals']
                total_points = sum(animals.values())
                animal_list = list(animals.keys())
                self.areas[area_name] = {
                    'TotalPoints': total_points,
                    'animals': animal_list
                }
                self.insert(total_points)

                rows.append({
                    'Área': area_name,
                    'Total de Pontos': total_points,
                    'Animais': ', '.join(animal_list)
                })

            # Criar e imprimir o DataFrame
            df = pd.DataFrame(rows)
            print("\nDados carregados do banco:")
            print(df)

    def insert(self, value):
        parent = None
        current = self.root

        while current:
            parent = current
            
            if value < current.data:
                current = current.left
            else:
                current = current.right

        new_node = Node(value)
        if parent is None:
            self.root = new_node
        elif value < parent.data:
            parent.left = new_node
        else:
            parent.right = new_node

    def search(self, area=None, value=None):
        if area:
            specific_area = self.areas.get(area)
            if specific_area:
                node = self._search(specific_area['TotalPoints'], self.root)
                if node:
                    return {
                        area: node.data,
                        'animals': specific_area['animals']
                    }
                else:
                    return None  
            else:
                return None  
        
        elif value is not None:
            node = self._search(value, self.root)
            if node:
                matching_areas = {
                    name: info
                    for name, info in self.areas.items()
                    if info['TotalPoints'] == value
                }
                return matching_areas if matching_areas else None
            else:
                return None  
        
        else:
            return None  

    def _search(self, value, node):
        if node is None:
            return None
        if node.data == value:
            return node
        elif value < node.data:
            return self._search(value, node.left)
        else:
            return self._search(value, node.right)
          
    def visualize(self, filename='binary_tree', view=True):
        dot = Digraph(comment='Binary Tree')

        def add_nodes_edges(node):
            if node is None:
                return
            dot.node(str(id(node)), str(node.data))

            if node.left:
                dot.edge(str(id(node)), str(id(node.left)), label='L')
                add_nodes_edges(node.left)
            if node.right:
                dot.edge(str(id(node)), str(id(node.right)), label='R')
                add_nodes_edges(node.right)

        add_nodes_edges(self.root)
        dot.render(filename, format='png', view=view)