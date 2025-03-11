import networkx as nx
import matplotlib.pyplot as plt
import time
from itertools import permutations
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
        exist_origem = self.grafo.search(origem)
        exist_destino = self.grafo.search(destino)

        if not exist_origem and not exist_destino:
            return "Origem ou destino não existe \n\n"

        self.fila.append((exist_origem, 0))
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
        if self.search(data) is not None:
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

    def search(self, data, vertice=None):
        if vertice is None:
            vertice = self.head
        if vertice is None:
            return None
        if vertice.data == data:
            return vertice
        if vertice.next is None:
            return None
        return self.search(data, vertice.next)

    def contar_vertices(self):
        count = 0
        vertice = self.head
        while vertice:
            count += 1
            vertice = vertice.next
        return count

    def buscar_peso(self, origem, destino):
        aresta = origem.arestas
        while aresta:
            if aresta.data == destino:
                return aresta.peso
            aresta = aresta.next
        return None

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

    def to_networkx(self):
        G = nx.DiGraph()
        vertice = self.head
        while vertice is not None:
            G.add_node(vertice.data)
            aresta = vertice.arestas
            while aresta is not None:
                G.add_edge(vertice.data, aresta.data.data, weight=aresta.peso)
                aresta = aresta.next
            vertice = vertice.next
        return G

    def draw(self, layout="circular"):
        G = self.to_networkx()

        if layout == "shell":
            pos = nx.shell_layout(G)
        elif layout == "circular":
            pos = nx.circular_layout(G)
        elif layout == "kamada_kawai":
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.spring_layout(G, seed=42, k=0.7)

        plt.figure(figsize=(8, 6))

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=2000,
            edge_color="gray",
            width=2,
            font_size=12,
            font_weight="bold",
            arrows=True,
            arrowstyle="-|>",
            arrowsize=20,
        )

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_size=12, font_color="red"
        )

        plt.show()

    def get_vertices(self):
        vertices = []
        vertice = self.head
        while vertice is not None:
            vertices.append(vertice)
            vertice = vertice.next
        return vertices


class TSP:
    def __init__(self, grafo):
        self.grafo = grafo
        self.melhor_custo = float("inf")
        self.melhor_caminho = []

    def dfs_tsp(self, atual, visitados, caminho, custo_atual, inicio):
        if len(visitados) == self.grafo.contar_vertices():
            retorno = self.grafo.buscar_peso(atual, inicio)
            if retorno is not None:
                custo_total = custo_atual + retorno
                if custo_total < self.melhor_custo:
                    self.melhor_custo = custo_total
                    self.melhor_caminho = caminho + [inicio.data]
            return

        aresta = atual.arestas
        while aresta is not None:
            if aresta.data not in visitados:
                visitados.add(aresta.data)
                self.dfs_tsp(
                    aresta.data,
                    visitados,
                    caminho + [aresta.data.data],
                    custo_atual + aresta.peso,
                    inicio,
                )
                visitados.remove(aresta.data)
            aresta = aresta.next

    def encontrar_melhor_rota(self, inicio):
        vertice_inicial = self.grafo.search(inicio)
        if not vertice_inicial:
            return None, None

        self.dfs_tsp(vertice_inicial, {vertice_inicial}, [inicio], 0, vertice_inicial)

        if self.melhor_custo != float("inf"):
            return self.melhor_custo, self.melhor_caminho
        else:
            return None, None


class TSPBruteForce:
    def __init__(self, grafo):
        self.grafo = grafo

    def calcular_custo_rota(self, rota):
        custo_total = 0
        for i in range(len(rota) - 1):
            origem = self.grafo.search(rota[i])
            destino = self.grafo.search(rota[i + 1])
            peso = self.grafo.buscar_peso(origem, destino)
            if peso is None:
                return float("inf")
            custo_total += peso

        origem = self.grafo.search(rota[-1])
        destino = self.grafo.search(rota[0])
        peso_retorno = self.grafo.buscar_peso(origem, destino)
        if peso_retorno is None:
            return float("inf")
        custo_total += peso_retorno
        return custo_total

    def encontrar_melhor_rota(self, inicio):
        vertices = [vertice.data for vertice in self.grafo.get_vertices()]
        if inicio not in vertices:
            return None, None

        vertices.remove(inicio)

        melhor_custo = float("inf")
        melhor_rota = None

        for perm in permutations(vertices):
            rota = [inicio] + list(perm)
            custo = self.calcular_custo_rota(rota)
            if custo < melhor_custo:
                melhor_custo = custo
                melhor_rota = rota

        return melhor_custo, melhor_rota


class DFS:
    def __init__(self):
        self.visitados = []
        self.custo_maximo = 0
        self.caminho_maximo = []

    def dfs_menor_custo(self, grafo, origem, destino, custo_atual, caminho_atual):
        self.visitados.append(origem)
        if origem == destino:
            if custo_atual > self.custo_maximo:
                self.custo_maximo = custo_atual
                self.caminho_maximo = caminho_atual

        aresta = origem.arestas
        while aresta is not None:
            if aresta.data not in self.visitados:
                self.dfs_menor_custo(
                    grafo,
                    aresta.data,
                    destino,
                    custo_atual + aresta.peso,
                    caminho_atual + [aresta.data],
                )
            aresta = aresta.next

        self.visitados.remove(origem)

class Dijkstra:
    def __init__(self, grafo):
        self.grafo = grafo

    def encontrar_caminho_mais_curto(self, origem, destino):
        origem_vertice = self.grafo.search(origem)
        destino_vertice = self.grafo.search(destino)
        if not origem_vertice or not destino_vertice:
            return "Origem ou destino não existe \n\n"

        distancias = {vertice.data: float('inf') for vertice in self.grafo.get_vertices()}
        distancias[origem] = 0

        caminho_anterior = {}
        nao_visitados = [vertice.data for vertice in self.grafo.get_vertices()]

        while nao_visitados:
            vertice_atual = nao_visitados.pop(0)
            vertice_atual_obj = self.grafo.search(vertice_atual)
            aresta = vertice_atual_obj.arestas
  
            while aresta:
                vizinho = aresta.data.data
                peso = aresta.peso
                nova_distancia = distancias[vertice_atual] + peso
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    caminho_anterior[vizinho] = vertice_atual

                aresta = aresta.next

        caminho = []
        vertice_atual = destino
        while vertice_atual in caminho_anterior:
            caminho.insert(0, vertice_atual)
            vertice_atual = caminho_anterior[vertice_atual]
        caminho.insert(0, origem)

        return f"Distância: {distancias[destino]}, Caminho: {caminho}\n\n"


class ReadCsv:
    def generate_grafo_by_csv(self):
        grafo = Grafo()
        # df = pd.read_csv("csv/caixeiro.csv")
        df = pd.read_csv("csv/disjkstra.csv")
        for _, row in df.iterrows():
            grafo.add_vertice(row["Origem"])
            grafo.add_vertice(row["Destino"])
            grafo.add_aresta(row["Origem"], row["Destino"], row["Peso"])

            # grafo.add_aresta(row["Destino"], row["Origem"], row["Peso"])

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
            print("6 - Caixeiro viajante")
            print("7 - Dijkstra")
            print("8 - Sair")
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
                print(bfs.menor_saltos(node1, node2))
            elif op == 5:
                origem = input("Digite o vertice de origem: ")
                destino = input("Digite o vertice de destino: ")
                dfs = DFS()
                dfs.dfs_menor_custo(
                    grafo,
                    grafo.search(origem),
                    grafo.search(destino),
                    0,
                    [grafo.search(origem)],
                )
                print(f"Custo máximo: {dfs.custo_maximo}")
                print(
                    f"Caminho máximo: {[vertice.data for vertice in dfs.caminho_maximo]}"
                )

            elif op == 6:
                inicio = input("Digite o vértice de início: ")
                start_time = time.time()
                tsp = TSP(grafo)
                custo, caminho = tsp.encontrar_melhor_rota(inicio)
                if caminho:
                    print(f"Melhor caminho encontrado: {caminho} com custo {custo}")
                else:
                    print("Não foi possível encontrar uma solução.")
                print(f"Tempo de execução: {time.time() - start_time:.8f} segundos")

                print("\nUsando força bruta:")
                start_time = time.time()
                tsp_brute_force = TSPBruteForce(grafo)
                custo, rota = tsp_brute_force.encontrar_melhor_rota(inicio)
                if rota:
                    print(f"Melhor rota encontrada: {rota} com custo {custo}")
                else:
                    print("Não foi possível encontrar uma solução.")
                print(f"Tempo de execução: {time.time() - start_time:.8f} segundos")

                # grafo.draw()
            elif op == 7:
                origem = input("Digite o vertice de origem: ")
                destino = input("Digite o vertice de destino: ")
                dijkstra = Dijkstra(grafo)
                print(dijkstra.encontrar_caminho_mais_curto(origem, destino))

            elif op == 8:
                break

            else:
                print("Opção inválida")

    except Exception as e:
        print("Erro")
        print(e)
