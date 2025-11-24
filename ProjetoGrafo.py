# Beatriz Lima de Moura 10416616
# Giovana Simões Franco 10417646
# -----------------------------------------------------------------------------
# Histórico de Alterações:
# 27/09/2025, Beatriz e Giovana, Adicionadas funcionalidades para a Parte 1
# do projeto:
#       - Suporte a rótulos de vértices e tipo de grafo.
#       - Métodos para inserir vértice, salvar e carregar de arquivo.
#       - Ajuste para grafos não-orientados.
# 27/09/2025, Beatriz, Adicionadas funcionalidades para grafo não-orientado
# 28/09/2025, Giovana, Refatoração para suportar dados complexos nos vértices
#           e pesos múltiplos (distância e tempo) nas arestas.
# 28/09/2025, Giovana, Mudanças nas funções que lidam com o arquivo para estar
#           alinhado com nosso arquivo grafo.txt
# 23/11/2025,Beatriz, Adicionadas funcionalidades de Análise Avançada (Itens 14-17)
# -----------------------------------------------------------------------------

import heapq
from collections import deque, Counter

class TGrafoServicos:
    def __init__(self, n=0):
        self.n = n; self.m = 0
        # A matriz de adjacência armazena dicionários de pesos (ou float('inf'))
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
                    # Partes esperadas: [índice, rotulo, categoria, distrito, endereco]
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
                    # Partes esperadas: [v, w, dist, tempo]
                    v, w, dist, tempo = int(partes[0]), int(partes[1]), float(partes[2]), float(partes[3])
                    # InsereA original faz a verificação de inf e conta as arestas
                    self.insereA(v, w, dist, tempo)
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
                    # Acessa o peso usando a chave_peso ('distancia' ou 'tempo')
                    peso_aresta = self.adj[u][v][chave_peso]
                    if dist[u] + peso_aresta < dist[v]:
                        dist[v] = dist[u] + peso_aresta; pred[v] = u
                        heapq.heappush(pq, (dist[v], v))
        return dist, pred

    # ----------------------------------------------------------------------
    # MÉTODOS AUXILIARES E DE ANÁLISE AVANÇADA (PARTE 3)
    # ----------------------------------------------------------------------
    
    def get_indices_distritos(self):
        """
        Retorna os índices dos vértices que representam os 8 distritos.
        Assume que os 8 primeiros nós são os distritos para manter o código limpo,
        baseado na estrutura típica desse tipo de modelagem.
        """
        return list(range(min(8, self.n)))


    # ----------------------------------------------------------------------
    # ITEM 14: MATRIZ DE CAMINHOS MÍNIMOS (Base para Acessibilidade)
    # ----------------------------------------------------------------------

    def matriz_caminhos_minimos(self, chave_peso='distancia'):
        """
        Calcula o Caminho Mínimo entre Todos os Pares (APSP) de distritos 
        para todos os vértices do grafo, usando múltiplas execuções do Dijkstra.
        
        Retorna: um dicionário {origem_idx: distancias_array}
        """
        distritos_indices = self.get_indices_distritos()
        matriz_distancias = {}

        # O(|V_distritos| * (|E| + |V| log |V|))
        for i in distritos_indices:
            # Reutiliza o Dijkstra para calcular a menor distância de 'i' a todos os nós
            distancias, _ = self.dijkstra(i, chave_peso)
            matriz_distancias[i] = distancias
        
        return matriz_distancias
        
    def apresenta_matriz_caminhos_minimos(self, chave_peso='distancia'):
        """Apresenta um resumo da matriz calculada."""
        self.matriz_caminhos_minimos(chave_peso)
        print(f"\n--- Item 14: Matriz de Caminhos Mínimos Calculada (Chave: {chave_peso.capitalize()}) ---")
        print("A Matriz de Caminhos Mínimos entre Todos os Distritos e Todos os Serviços foi gerada com sucesso.")
        print("Ela é a base de dados para as análises de Centralidade (Item 15) e pior acesso de forma robusta.")
        print("-" * 70)


    # ----------------------------------------------------------------------
    # ITEM 15: CENTRALIDADE DE PROXIMIDADE (Quantificação de Desigualdade)
    # ----------------------------------------------------------------------
    
    def centralidade_de_proximidade_distritos(self, chave_peso='distancia'):
        """
        Calcula a Centralidade de Proximidade (Closeness Centrality) para os distritos.
        
        Retorna: lista de tuplas (rotulo_distrito, farness, centralidade).
        """
        # 1. Obter a matriz de distâncias
        matriz_distancias = self.matriz_caminhos_minimos(chave_peso)
        resultados = []

        for origem_idx, distancias in matriz_distancias.items():
            # 2. Calcular Farness: Soma total das distâncias para todos os nós alcançáveis
            farness = sum(d for d in distancias if d != float('inf') and d > 0)
            
            # 3. Número de nós alcançados (N)
            num_alcancados = len([d for d in distancias if d != float('inf') and d > 0])
            
            if num_alcancados > 0:
                # 4. Centralidade: (N - 1) / Farness (N é o número de vértices - 1)
                # No nosso caso, estamos usando o número de nós alcançados (num_alcancados)
                centralidade = num_alcancados / farness
            else:
                centralidade = 0.0 
            
            rotulo = self.vertices[origem_idx]['rotulo']
            resultados.append((rotulo, farness, centralidade))

        # 5. Ordena pelo pior acesso (maior Farness)
        resultados.sort(key=lambda x: x[1], reverse=True) 
        return resultados

    def apresenta_centralidade_proximidade(self, chave_peso='distancia'):
        """Formata e imprime os resultados da Centralidade de Proximidade."""
        resultados = self.centralidade_de_proximidade_distritos(chave_peso)
        
        print(f"\n--- Item 15: Análise de Desigualdade (Baseado em {chave_peso.capitalize()}) ---")
        print("Rank | Distrito | Farness (Soma Dist.) | Centralidade (Acessib.)")
        print("-" * 65)
        
        for rank, (rotulo, farness, centralidade) in enumerate(resultados, 1):
            status_acesso = "PIOR ACESSO GERAL" if rank == 1 else ("MELHOR ACESSO GERAL" if rank == len(resultados) else "")
            print(f"{rank:4} | {rotulo:8} | {farness:20.2f} | {centralidade:22.4f} | {status_acesso}")
        print("Centralidade: (Maior valor = Melhor Acesso, Menor valor = Pior Acesso)")
        print("-" * 65)


    # ----------------------------------------------------------------------
    # ITEM 17: ÁRVORE GERADORA MÍNIMA (Eficiência da Infraestrutura)
    # ----------------------------------------------------------------------
    
    def arvore_geradora_minima(self, chave_peso='distancia'):
        """
        Implementa o algoritmo de Prim para encontrar a Árvore Geradora Mínima (AGM).
        """
        if self.n == 0: return 0, []
        
        dist = [float('inf')] * self.n
        pred = [-1] * self.n 
        visitados = [False] * self.n
        dist[0] = 0 
        pq = [(0, 0)] # (custo, vertice)
        
        custo_total = 0
        arestas_agm = []
        
        while pq:
            d, u = heapq.heappop(pq)
            
            if visitados[u]: continue
            visitados[u] = True
            custo_total += d
            
            if pred[u] != -1:
                arestas_agm.append((pred[u], u, d))
                
            for v in range(self.n):
                if self.adj[u][v] != float('inf') and not visitados[v]:
                    peso_aresta = self.adj[u][v][chave_peso]
                    if peso_aresta < dist[v]:
                        dist[v] = peso_aresta
                        pred[v] = u
                        heapq.heappush(pq, (dist[v], v))
                        
        if len(arestas_agm) != self.n - 1 and self.n > 1 and len(self.componentes_conexas()) > 1:
            # Se o grafo é desconexo, a AGM só é calculada para uma componente
            return float('inf'), [] 
        
        return custo_total, arestas_agm

    def apresenta_agm(self, chave_peso='distancia'):
        """Formata e imprime os resultados da Árvore Geradora Mínima."""
        custo, arestas = self.arvore_geradora_minima(chave_peso)
        
        print(f"\n--- Item 17: Análise de Eficiência da Infraestrutura (Baseado em {chave_peso.capitalize()}) ---")
        
        if len(self.componentes_conexas()) > 1:
             print("O grafo é desconexo. AGM calculada apenas para a componente mais próxima do nó 0.")
             print("Resultado da AGM é uma sub-rede mínima.")

        if custo == float('inf'):
            print("Não foi possível calcular a AGM. O grafo não é conexo e tem múltiplos nós isolados.")
            return

        print(f"Custo Total Mínimo da Rede (AGM): {custo:.2f} {chave_peso.capitalize()}")
        print(f"O custo total da AGM serve como referência do custo mais eficiente para conectar todos os {self.n} pontos.")
        print("-" * 70)


    # ----------------------------------------------------------------------
    # ITEM 16: PONTOS DE ARTICULAÇÃO (Robustez e Serviços Críticos)
    # ----------------------------------------------------------------------
    
    def pontos_de_articulacao(self):
        """
        Encontra os Pontos de Articulação (vértices cruciais) no grafo usando DFS.
        """
        if self.n == 0: return []
        
        visitado = [False] * self.n
        d = [0] * self.n # Discovery time
        low = [0] * self.n # Low-link value
        pai = [-1] * self.n
        is_ap = [False] * self.n
        timer = 0
        pontos_encontrados = set()

        def dfs(u):
            nonlocal timer
            visitado[u] = True
            timer += 1
            d[u] = low[u] = timer
            filhos = 0
            
            for v in range(self.n):
                if self.adj[u][v] != float('inf'):
                    if v == pai[u]: continue
                    
                    if visitado[v]:
                        low[u] = min(low[u], d[v])
                    else:
                        pai[v] = u
                        filhos += 1
                        dfs(v)
                        
                        low[u] = min(low[u], low[v])
                        
                        # Condição 1: u é a raiz da DFS e tem 2 ou mais filhos
                        if pai[u] == -1 and filhos > 1:
                            is_ap[u] = True
                        # Condição 2: u não é a raiz e low[v] >= d[u]
                        if pai[u] != -1 and low[v] >= d[u]:
                            is_ap[u] = True
            
            if is_ap[u]: pontos_encontrados.add(u)
            
        # Percorre todas as componentes
        for i in range(self.n):
            if not visitado[i]:
                dfs(i)
                
        # Converte índices para rótulos para apresentação
        rotulos_ap = [self.vertices[i]['rotulo'] for i in pontos_encontrados]
        return rotulos_ap

    def apresenta_pontos_articulacao(self):
        """Formata e imprime os resultados dos Pontos de Articulação."""
        pontos = self.pontos_de_articulacao()
        
        print(f"\n--- Item 16: Análise de Robustez: Pontos de Articulação (Serviços Críticos) ---")
        if not pontos:
            print("Não foram encontrados Pontos de Articulação.")
            print("A remoção de um único serviço ou distrito não isolaria partes da rede de acesso.")
        else:
            print(f"Foram encontrados {len(pontos)} Pontos de Articulação (Vértices Críticos):")
            print("🚨 Estes são serviços (ou distritos) vitais. Sua remoção causaria a desconexão de partes da rede. 🚨")
            print("-" * 70)
            for i, rotulo in enumerate(pontos):
                print(f"  {i+1}. {rotulo}")
        print("-" * 70)

    # ----------------------------------------------------------------------
    # Métodos de Análise Estrutural existentes
    # ----------------------------------------------------------------------

    def graus(self):
        """Retorna o grau de cada vértice (quantidade de vizinhos conectados)."""
        graus = []
        for i in range(self.n):
            g = sum(1 for j in range(self.n) if self.adj[i][j] != float('inf'))
            graus.append(g)
        return graus

    def grau_maximo_minimo_medio(self):
        """Retorna grau máximo, mínimo e grau médio do grafo."""
        graus = self.graus()
        if not graus:
            return 0, 0, 0.0
        return max(graus), min(graus), sum(graus) / len(graus)

    def distribuicao_dos_graus(self):
        """Retorna um dicionário onde a chave é o grau e o valor é a quantidade de vértices com esse grau."""
        return dict(Counter(self.graus()))

    def componentes_conexas(self):
        """Retorna todas as componentes conexas do grafo (listas de vértices)."""
        if self.n == 0:
            return []
        visitados = set()
        componentes = []
        from collections import deque

        for i in range(self.n):
            if i in visitados:
                continue
            comp = []
            fila = deque([i])
            visitados.add(i)
            while fila:
                u = fila.popleft()
                comp.append(u)
                for v in range(self.n):
                    if self.adj[u][v] != float('inf') and v not in visitados:
                        visitados.add(v)
                        fila.append(v)
            componentes.append(comp)
        return componentes

    def grafo_conexo(self):
        """Retorna True se o grafo é conexo; False caso contrário."""
        return self.n > 0 and len(self.componentes_conexas()) == 1

    def grafo_euleriano(self):
        """Retorna True se o grafo possui ciclo euleriano (todos os graus pares)."""
        if self.n == 0 or not self.grafo_conexo():
            return False
        return all(g % 2 == 0 for g in self.graus())

    def possui_trilha_euleriana(self):
        """Retorna True se o grafo possui trilha euleriana (0 ou 2 vértices ímpares)."""
        if self.n == 0 or not self.grafo_conexo():
            return False
        impares = sum(1 for g in self.graus() if g % 2 == 1)
        return impares in (0, 2)

    def coloracao_gulosa(self, ordem=None):
        """Aplica coloração gulosa e retorna (lista_de_cores, número_de_cores_usadas)."""
        if self.n == 0:
            return [], 0
        if ordem is None:
            ordem = list(range(self.n))
        cores = [-1] * self.n

        for u in ordem:
            cores_usadas = set()
            for v in range(self.n):
                if self.adj[u][v] != float('inf') and cores[v] != -1:
                    cores_usadas.add(cores[v])
            cor = 0
            while cor in cores_usadas:
                cor += 1
            cores[u] = cor

        return cores, max(cores) + 1

    def numero_cromatico_estimado(self):
        """Retorna estimativa do número cromático utilizando coloração gulosa por grau decrescente."""
        if self.n == 0:
            return 0
        graus = self.graus()
        ordem = sorted(range(self.n), key=lambda x: graus[x], reverse=True)
        _, num_cores = self.coloracao_gulosa(ordem)
        return num_cores

    def grafo_regular(self):
        """Verifica se o grafo é k-regular (todos os vértices com mesmo grau)."""
        graus = self.graus()
        if not graus:
            return True, 0
        k = graus[0]
        return (all(d == k for d in graus), k if all(d == k for d in graus) else None)


    def satisfaz_teorema_1(self):
        """Verifica condição para Hamiltonianidade (suficiente)."""
        if self.n < 3:
            return False
        graus = self.graus()
        for u in range(self.n):
            for v in range(u + 1, self.n):
                if self.adj[u][v] == float('inf'):
                    if graus[u] + graus[v] < self.n:
                        return False
        return True

    def satisfaz_teorema_2(self):
        """Teorema 2 : grau mínimo >= |V|/2."""
        if self.n < 3:
            return False
        return min(self.graus()) >= (self.n / 2)

    def ciclo_hamiltoniano_backtracking(self, limite=18):
        """Tenta encontrar um ciclo Hamiltoniano por backtracking (somente para n <= limite)."""
        if self.n == 0 or self.n > limite:
            return None
        n = self.n
        visitados = [False] * n
        caminho = []

        def bt(u, profundidade):
            caminho.append(u)
            visitados[u] = True
            if profundidade == n:
                if self.adj[caminho[-1]][caminho[0]] != float('inf'):
                    return True
                visitados[u] = False
                caminho.pop()
                return False
            for v in range(n):
                if not visitados[v] and self.adj[u][v] != float('inf'):
                    if bt(v, profundidade + 1):
                        return True
            visitados[u] = False
            caminho.pop()
            return False

        for inicio in range(n):
            caminho.clear()
            visitados = [False] * n
            if bt(inicio, 1):
                return caminho[:]
        return None

    def caminho_hamiltoniano_backtracking(self, limite=18):
        """Tenta encontrar um caminho Hamiltoniano (não precisa fechar ciclo)."""
        if self.n == 0 or self.n > limite:
            return None
        n = self.n
        visitados = [False] * n
        caminho = []

        def bt(u, profundidade):
            caminho.append(u)
            visitados[u] = True
            if profundidade == n:
                return True
            for v in range(n):
                if not visitados[v] and self.adj[u][v] != float('inf'):
                    if bt(v, profundidade + 1):
                        return True
            visitados[u] = False
            caminho.pop()
            return False

        for inicio in range(n):
            caminho.clear()
            visitados = [False] * n
            if bt(inicio, 1):
                return caminho[:]
        return None

    def gerar_relatorio(self):
        """Gera texto com análise completa do grafo."""
        linhas = []

        linhas.append(f"Relatório do Grafo: {self.n} vértices, {self.m} arestas.\n")

        # Componentes
        componentes = self.componentes_conexas()
        linhas.append(f"Componentes conexas: {len(componentes)}")

        # Graus
        gmax, gmin, gmed = self.grau_maximo_minimo_medio()
        linhas.append(f"Grau máximo: {gmax}, mínimo: {gmin}, médio: {gmed:.2f}")
        linhas.append(f"Distribuição dos graus: {self.distribuicao_dos_graus()}")

        # Regularidade
        reg, k = self.grafo_regular()
        linhas.append(f"Grafo regular: {'Sim, k = ' + str(k) if reg else 'Não'}")

        # Euler
        linhas.append(f"Ciclo euleriano: {'Sim' if self.grafo_euleriano() else 'Não'}")
        linhas.append(f"Trilha euleriana: {'Sim' if self.possui_trilha_euleriana() else 'Não'}")

        # Coloração
        cores, num_cores = self.coloracao_gulosa()
        linhas.append(f"Coloração gulosa utiliza {num_cores} cores.")

        # Hamilton
        linhas.append(f"Satisfaz 1 (Ore): {'Sim' if self.satisfaz_teorema_1() else 'Não'}")
        linhas.append(f"Satisfaz 2 (Dirac): {'Sim' if self.satisfaz_teorema_2() else 'Não'}")

        if self.n <= 18:
            ciclo = self.ciclo_hamiltoniano_backtracking()
            if ciclo:
                linhas.append(f"Ciclo Hamiltoniano encontrado: {ciclo}")
            else:
                caminho = self.caminho_hamiltoniano_backtracking()
                if caminho:
                    linhas.append(f"Caminho Hamiltoniano encontrado: {caminho}")
                else:
                    linhas.append("Nenhum ciclo/caminho Hamiltoniano encontrado por backtracking.")
        else:
            linhas.append("Grafo grande para backtracking (n > 18).")

        return "\n".join(linhas)
