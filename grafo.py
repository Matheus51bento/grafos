import networkx as nx
import matplotlib.pyplot as plt

import pandas as pd

class Grafo:

    def __init__(self):
        self.head = None

    class Vertice:
        def __init__(self, data):
            self.data = data
            self.next = None
            self.arestas = None

    class Aresta:
        def __init__(self, data, peso):
            self.data = data
            self.peso = peso
            self.next = None
    
    def add_vertice(self, data):
        vertice = self.search(data)
        if vertice is not None:
            return None
        if self.head is None:
            self.head = self.Vertice(data)
        else:
            vertice = self.Vertice(data)
            vertice.next = self.head
            self.head = vertice
        

    def add_aresta(self, vertice1, vertice2, peso):
        vertice = self.search(vertice1)
        node_vertice = self.search(vertice2)
        if vertice is None or node_vertice is None:
            return None
        
        if vertice.arestas is None:
            vertice.arestas = self.Aresta(node_vertice, peso)
        else:
            aresta = self.Aresta(node_vertice, peso)
            aresta.next = vertice.arestas
            vertice.arestas = aresta

    def print(self, vertice: Vertice = None):
        if vertice is None:
            if self.head is None:
                return None
            vertice = self.head
        
        if vertice.arestas is not None:
            string = self.print_arestas(vertice.arestas)
            print(f"{vertice.data}: {string}")
        else:
            print(vertice.data)
        if vertice.next is not None:
            self.print(vertice.next)

    def print_arestas(self, aresta: Aresta, string=""):
        if aresta is None:
            return string
        string += f"-> {aresta.data.data} "
        return self.print_arestas(aresta.next, string)

    def search(self, data, vertice: Vertice = None):
        if vertice is None:
            if self.head is None:
                return None
            vertice = self.head
        if vertice.data == data:
            return vertice
        if vertice.next is None:
                return None
        return self.search(data, vertice.next)
    

    def to_networkx(self):
        G = nx.DiGraph(directed=True)
        vertice = self.head
        while vertice is not None:
            G.add_node(vertice.data)
            aresta = vertice.arestas
            while aresta is not None:
                G.add_edge(vertice.data, aresta.data.data)
                aresta = aresta.next
            vertice = vertice.next
        return G

    def draw(self):
        G = self.to_networkx()
        pos = nx.spring_layout(G)

        plt.figure(figsize=(8, 6))
        options = {
            'node_color': 'lightblue',
            'node_size': 2000,
            'width': 3,
            'arrowstyle': '-|>',
            'arrowsize': 20,
        }
        nx.draw_networkx(G, arrows=True, **options)
        plt.show()
        

class ReadCsv:

    def generate_grafo_by_csv(self):
        grafo = Grafo()

        df = pd.read_csv("csv/grafos.csv")

        for index, row in df.iterrows():
            origem = row["Origem"]
            destino = row["Destino"]
            peso = row["Peso"]
            print(f"Origem: {origem}, Destino: {destino}, Peso: {peso}")

            grafo.add_vertice(origem)
            grafo.add_vertice(destino)
            grafo.add_aresta(origem,destino, peso)

        return grafo


if __name__ == "__main__":

    readCsv = ReadCsv()
    grafo = readCsv.generate_grafo_by_csv()
    
    try:
        while True:
            print("1 - Adicionar vertice")
            print("2 - Adicionar aresta")
            print("3 - Imprimir")
            print("4 - Sair")
            op = int(input("Escolha uma opção: "))
            if op == 1:
                data = input("Digite o dado do vertice: ")
                grafo.add_vertice(data)
            elif op == 2:
                node1 = input("Digite o vertice de origem: ")
                node2 = input("Digite o vertice de destino: ")
                grafo.add_aresta(node1, node2)
            elif op == 3:
                print("\nGrafo:")
                grafo.print()
                grafo.draw()
                print()
            elif op == 4:
                break
            else:
                print("Opção inválida")
    except Exception as e:
        print("Erro")
        print(e)