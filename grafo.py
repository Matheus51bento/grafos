import pandas as pd


class BFS:
    def __init__(self, grafo):
        self.grafo = grafo
        self.fila = []
        self.visitados = set([])

    def insert_vizinhos_list(self, aresta, saltos):
        if aresta is None:
            return
        self.fila.append((aresta.data, saltos + 1))
        self.visitados.add(aresta.data)
        return self.insert_vizinhos_list(aresta.next, saltos)
    
    def menor_saltos(self, origem, destino):
        exist_origem =  self.grafo.search(origem)
        exist_destino =  self.grafo.search(destino)

        if not exist_origem and  not exist_destino:
            return "Origem ou destino não existe \n\n"
        
        self.fila.append((exist_origem,0))
        self.visitados.add(exist_origem)

        while len(self.fila) > 0:
            vertice_atual, saltos = self.fila.pop(0)

            if vertice_atual == exist_destino:
                return f"Número de saltos: {saltos}\n\n"
            
            self.insert_vizinhos_list(vertice_atual.arestas, saltos)

        return "Nenhum caminho encontrado \n\n"


    

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
            print("4 - BFS")
            print("5 - DFS")
            print("6 - Sair")
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
                print()
            elif op == 4:
                node1 = input("Digite o vertice de origem: ")
                node2 = input("Digite o vertice de destino: ")
                bfs = BFS(grafo)
                print(bfs.menor_saltos(node1,node2))
            elif op == 6:
                break
            else:
                print("Opção inválida")
    except Exception as e:
        print("Erro")
        print(e)