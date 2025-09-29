# Beatriz Lima de Moura 10416616
# Giovana Simões Franco 10417646
# -----------------------------------------------------------------------------
# Histórico de Alterações:
# 27/09/2025, Beatriz e Giovana, Adicionadas funcionalidades para a Parte 1
# do projeto:
#       - Suporte a rótulos de vértices e tipo de grafo.
#       - Métodos para inserir vértice, salvar e carregar de arquivo.
#       - Ajuste para grafos não-orientados.
# 27/09/2025, Beatriz, Adicionadas funcionalidades para grafo não-orientado
# 28/09/2025, Giovana, Refatoração para suportar dados complexos nos vértices
#           e pesos múltiplos (distância e tempo) nas arestas.
# 28/09/2025, Giovana, Mudanças nas funções que lidam com o arquivo para estar
#           alinhado com nosso arquivo grafo.txt
# -----------------------------------------------------------------------------

import heapq
from collections import deque

class TGrafoServicos:
    def __init__(self, n=0):
        self.n = n; self.m = 0
        self.adj = [[float('inf') for _ in range(n)] for _ in range(n)]
        self.vertices = []
        self.direcionado = False
        self.tipo_grafo = 2

    def insereV(self, rotulo, categoria, distrito, endereco):
        # Silencioso para não poluir o carregamento do arquivo
        for i in range(self.n): self.adj[i].append(float('inf'))
        self.n += 1
        novo_vertice_info = {
            "rotulo": rotulo, "categoria": categoria, "distrito": distrito, "endereco": endereco
        }
        self.vertices.append(novo_vertice_info)
        self.adj.append([float('inf')] * self.n)
        return self.n - 1
    
    def insereV_com_print(self, rotulo, categoria, distrito, endereco):
        # Versão com print para uso no menu
        self.insereV(rotulo, categoria, distrito, endereco)
        print(f"Vértice {self.n - 1} ('{rotulo}') inserido com sucesso.")

    def insereA(self, v, w, distancia, tempo):
        if not (0 <= v < self.n and 0 <= w < self.n): print("Erro: Vértice inválido."); return
        if self.adj[v][w] == float('inf'):
            pesos = {"distancia": float(distancia), "tempo": float(tempo)}
            self.adj[v][w] = pesos; self.adj[w][v] = pesos
            self.m += 1
            print(f"Aresta entre '{self.vertices[v]['rotulo']}' e '{self.vertices[w]['rotulo']}' inserida.")
    
    def gravaNoArquivo(self, nome_arquivo="grafo.txt"):
        try:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(f"{self.tipo_grafo}\n")
                f.write(f"{self.n}\n")
                f.write("# --- Vértices (índice; rotulo; categoria; distrito; endereco) ---\n")
                for i, v_info in enumerate(self.vertices):
                    f.write(f"{i}; {v_info['rotulo']}; {v_info['categoria']}; {v_info['distrito']}; {v_info['endereco']}\n")
                f.write(f"{self.m}\n")
                f.write("# --- Arestas (v1; v2; distancia; tempo) ---\n")
                for i in range(self.n):
                    for j in range(i + 1, self.n):
                        if self.adj[i][j] != float('inf'):
                            pesos = self.adj[i][j]
                            f.write(f"{i}; {j}; {pesos['distancia']}; {pesos['tempo']}\n")
            print(f"Grafo salvo em '{nome_arquivo}' com sucesso.")
        except Exception as e: print(f"Erro ao salvar o arquivo: {e}")

    # --- MÉTODO CORRIGIDO ---
    def carregaDoArquivo(self, nome_arquivo="grafo.txt"):
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                self.__init__()
                
                self.tipo_grafo = int(f.readline().strip())
                self.direcionado = self.tipo_grafo >= 4

                num_vertices_declarado = int(f.readline().strip())
                
                # Loop corrigido para ignorar comentários corretamente
                vertices_lidos = 0
                while vertices_lidos < num_vertices_declarado:
                    linha = f.readline()
                    if not linha: break # Fim do arquivo
                    linha = linha.strip()
                    if not linha or linha.startswith('#'):
                        continue # Pula linhas vazias/comentários sem contar como vértice
                    
                    partes = [p.strip() for p in linha.split(';')]
                    self.insereV(partes[1], partes[2], partes[3], partes[4]) # Usa a versão silenciosa
                    vertices_lidos += 1
                
                num_arestas_declarado = int(f.readline().strip())

                # Loop corrigido para arestas também
                arestas_lidas = 0
                while arestas_lidas < num_arestas_declarado:
                    linha = f.readline()
                    if not linha: break # Fim do arquivo
                    linha = linha.strip()
                    if not linha or linha.startswith('#'):
                        continue
                    
                    partes = [p.strip() for p in linha.split(';')]
                    v, w, dist, tempo = int(partes[0]), int(partes[1]), float(partes[2]), float(partes[3])
                    if self.adj[v][w] == float('inf'):
                        pesos = {"distancia": dist, "tempo": tempo}
                        self.adj[v][w] = pesos; self.adj[w][v] = pesos; self.m += 1
                    arestas_lidas += 1

            print(f"Grafo carregado de '{nome_arquivo}' com sucesso. Tipo: {self.tipo_grafo}, {self.n} vértices, {self.m} arestas.")
        except Exception as e: print(f"Erro ao processar o arquivo: {e}")
    
    # (O restante dos métodos como removeA, show, etc. permanecem os mesmos)
    def removeA(self, v, w):
        if not (0 <= v < self.n and 0 <= w < self.n): print("Erro: Vértice inválido."); return
        if self.adj[v][w] != float('inf'):
            self.adj[v][w] = float('inf'); self.adj[w][v] = float('inf')
            self.m -= 1
            print(f"Aresta entre '{self.vertices[v]['rotulo']}' e '{self.vertices[w]['rotulo']}' removida.")
        else: print("Erro: Aresta não existe.")

    def removeVertice(self, v):
        if not (0 <= v < self.n): print("Erro: Vértice inválido!"); return
        self.m -= sum(1 for i in range(self.n) if self.adj[v][i] != float('inf'))
        self.adj.pop(v)
        for linha in self.adj: linha.pop(v)
        rotulo_removido = self.vertices.pop(v)['rotulo']
        self.n -= 1
        print(f"Vértice {v} ('{rotulo_removido}') e suas arestas foram removidos.")

    def show(self):
        print(f"\n--- Exibindo Grafo (Tipo: {self.tipo_grafo}, Vértices: {self.n}, Arestas: {self.m}) ---")
        print("\n--- Vértices ---")
        for i, v in enumerate(self.vertices):
            print(f"Índice {i}: {v['rotulo']} ({v['categoria']}) | Distrito: {v['distrito']} | Endereço: {v['endereco']}")
        print("\n--- Arestas (v1, v2): {distância, tempo} ---")
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.adj[i][j] != float('inf'):
                    pesos = self.adj[i][j]
                    print(f"({i}, {j}): Dist: {pesos['distancia']:.2f} km, Tempo: {pesos['tempo']:.1f} min")
        print("------------------------------------------\n")

    def verificar_conexidade(self):
        if self.n == 0: return "Grafo Vazio"
        visitados, fila = {0}, deque([0])
        while fila:
            u = fila.popleft()
            for v in range(self.n):
                if self.adj[u][v] != float('inf') and v not in visitados:
                    visitados.add(v); fila.append(v)
        return "Grafo Conexo" if len(visitados) == self.n else f"Grafo Desconexo"

    def dijkstra(self, origem, chave_peso='distancia'):
        if not (0 <= origem < self.n): print("Erro: Vértice inválido!"); return None, None
        dist, pred = [float('inf')] * self.n, [None] * self.n; dist[origem] = 0
        pq = [(0, origem)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]: continue
            for v in range(self.n):
                if self.adj[u][v] != float('inf'):
                    peso_aresta = self.adj[u][v][chave_peso]
                    if dist[u] + peso_aresta < dist[v]:
                        dist[v] = dist[u] + peso_aresta; pred[v] = u
                        heapq.heappush(pq, (dist[v], v))
        return dist, pred
