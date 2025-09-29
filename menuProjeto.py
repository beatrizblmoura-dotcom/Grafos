# Beatriz Lima de Moura 10416616
# Giovana Simões Franco 10417646
# -----------------------------------------------------------------------------
# Histórico de Alterações:
# 27/09/2025, Giovana, Criação do arquivo fonte menu e main.
# 28/09/2025, Giovana, Alteração para incluir todas as opções requisitadas no
#                       no menu.
# -----------------------------------------------------------------------------

from ProjetoGrafo import TGrafoServicos

def exibir_menu():
    print("\n MAPEAMENTO DE SERVIÇOS PÚBLICOS ")
    print(" Gerenciamento Básico ")
    print(" 1. Ler dados do arquivo")
    print(" 2. Inserir vértice (Distrito ou Serviço)")
    print(" 3. Inserir aresta")
    print(" 4. Remover vértice")
    print(" 5. Remover aresta")
    print(" 6. Gravar dados no arquivo (salva as alterações)")
    print(" 7. Mostrar conteúdo do arquivo de texto")
    print(" 8. Mostrar grafo (representação em memória)")
    
    print("\n Análises de Acesso e Desigualdade ")
    print(" 9. Listar serviços por categoria (ex: todos os hospitais)")
    print("10. Listar serviços por distrito de localização")
    print("11. Encontrar o serviço mais próximo de um distrito")
    print("12. Encontrar distrito com pior acesso a uma categoria de serviço")

    print("\n Outros ")
    print("13. Apresentar conexidade do grafo")
    print("14. Encerrar a aplicação")
    print("======================================================")

def obter_vertice(grafo, mensagem="Digite o índice do vértice: "):
    if grafo.n == 0: print("Erro: O grafo não possui vértices."); return None
    try:
        v = int(input(mensagem))
        if 0 <= v < grafo.n: return v
        else: print(f"Erro: Índice inválido. Insira um valor entre 0 e {grafo.n - 1}."); return None
    except ValueError: print("Erro: O índice deve ser um número inteiro."); return None
def mostrar_conteudo_arquivo():
    nome_arquivo = input("Digite o nome do arquivo para ler (padrão: grafo.txt): ") or "grafo.txt"
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            print(f"\n--- Conteúdo do Arquivo '{nome_arquivo}' ---")
            print(f.read())
            print("------------------------------------------")
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")

def main():
    grafo = TGrafoServicos()
    
    while True:
        exibir_menu()
        try:
            opcao = int(input("Escolha uma opção: "))

            if opcao == 1: # Ler arquivo
                nome_arquivo = input("Nome do arquivo (padrão: grafo.txt): ") or "grafo.txt"
                grafo.carregaDoArquivo(nome_arquivo)

            elif opcao == 2: # Inserir vértice
                rotulo = input("Nome do ponto: "); categoria = input("Categoria: ")
                distrito = input("Distrito onde está localizado: "); endereco = input("Endereço: ")
                grafo.insereV(rotulo, categoria, distrito, endereco)

            elif opcao == 3: # Inserir aresta
                v1 = obter_vertice(grafo, "Índice do primeiro vértice: ")
                if v1 is not None:
                    v2 = obter_vertice(grafo, "Índice do segundo vértice: ")
                    if v2 is not None and v1 != v2:
                        dist = float(input("Distância em km: ")); tempo = float(input("Tempo em minutos: "))
                        grafo.insereA(v1, v2, dist, tempo)

            elif opcao == 4: # Remover vértice
                v = obter_vertice(grafo, "Índice do vértice a ser removido: ")
                if v is not None: grafo.removeVertice(v)

            elif opcao == 5: # Remover aresta
                v1 = obter_vertice(grafo, "Índice do primeiro vértice da aresta: ")
                if v1 is not None:
                    v2 = obter_vertice(grafo, "Índice do segundo vértice da aresta: ")
                    if v2 is not None: grafo.removeA(v1, v2)

            elif opcao == 6: # Gravar arquivo
                nome_arquivo = input("Nome do arquivo (padrão: grafo.txt): ") or "grafo.txt"
                grafo.gravaNoArquivo(nome_arquivo)

            elif opcao == 7: # Mostrar conteúdo do arquivo
                mostrar_conteudo_arquivo()

            elif opcao == 8: # Mostrar grafo
                grafo.show()

            elif opcao == 9: # Listar por categoria
                cat_busca = input("Qual categoria você quer listar? (ex: Hospital): ").lower()
                print(f"\n Serviços da Categoria '{cat_busca.capitalize()}' ")
                encontrados = False
                for i, v in enumerate(grafo.vertices):
                    if v['categoria'].lower() == cat_busca:
                        print(f"Índice {i}: {v['rotulo']} (Local: {v['distrito']}) (Endereço: {v['endereco']}) ")
                        encontrados = True
                if not encontrados: print("Nenhum serviço encontrado para esta categoria.")

            elif opcao == 10: # Listar por distrito
                dist_busca = input("Listar serviços de qual distrito? (ex: Sé): ").lower()
                print(f"\n--- Serviços Localizados no Distrito '{dist_busca.capitalize()}' ---")
                encontrados = False
                for i, v in enumerate(grafo.vertices):
                    if v['distrito'].lower() == dist_busca and v['categoria'].lower() != 'distrito':
                        print(f"Índice {i}: {v['rotulo']} ({v['categoria']})")
                        encontrados = True
                if not encontrados: print("Nenhum serviço encontrado neste distrito.")

            elif opcao == 11: # Encontrar serviço mais próximo
                distritos = {i: v for i, v in enumerate(grafo.vertices) if v['categoria'].lower() == 'distrito'}
                if not distritos: print("Nenhum 'Distrito' cadastrado para ser a origem."); continue
                print("Distritos disponíveis:", ", ".join([f"{i}:{v['rotulo']}" for i,v in distritos.items()]))
                
                origem_idx = obter_vertice(grafo, "Índice do distrito de origem: ")
                if origem_idx is not None and origem_idx in distritos:
                    cat_servico = input("Qual tipo de serviço você procura? (ex: Hospital): ").lower()
                    chave_peso = 'tempo' if input("Buscar pelo menor (1) Distância ou (2) Tempo? ") == '2' else 'distancia'
                    
                    melhor_peso = float('inf'); melhor_servico_idx = -1
                    for j in range(grafo.n):
                        if grafo.adj[origem_idx][j] != float('inf') and grafo.vertices[j]['categoria'].lower() == cat_servico:
                            peso_atual = grafo.adj[origem_idx][j][chave_peso]
                            if peso_atual < melhor_peso:
                                melhor_peso = peso_atual; melhor_servico_idx = j
                    
                    if melhor_servico_idx == -1:
                        print(f"Nenhum serviço da categoria '{cat_servico.capitalize()}' encontrado.")
                    else:
                        unidade = "min" if chave_peso == 'tempo' else "km"
                        print("\n--- Resultado da Busca ---")
                        print(f"O '{cat_servico.capitalize()}' mais próximo de '{grafo.vertices[origem_idx]['rotulo']}' é:")
                        print(f"==> '{grafo.vertices[melhor_servico_idx]['rotulo']}' com {melhor_peso:.2f} {unidade}.")

            elif opcao == 12: # Encontrar distrito com pior acesso
                cat_servico = input("Analisar pior acesso para qual categoria? (ex: Hospital): ").lower()
                chave_peso = 'tempo' if input("Analisar por (1) Distância ou (2) Tempo? ") == '2' else 'distancia'
                unidade = "min" if chave_peso == 'tempo' else "km"

                distritos = {i: v for i, v in enumerate(grafo.vertices) if v['categoria'].lower() == 'distrito'}
                if not distritos: print("Nenhum 'Distrito' cadastrado para analisar."); continue

                pior_acesso_geral = -1; distrito_com_pior_acesso = None

                print("\n Análise de Desigualdade de Acesso ")
                for d_idx, d_info in distritos.items():
                    melhor_acesso_local = float('inf')
                    for s_idx in range(grafo.n):
                        if grafo.adj[d_idx][s_idx] != float('inf') and grafo.vertices[s_idx]['categoria'].lower() == cat_servico:
                            peso_atual = grafo.adj[d_idx][s_idx][chave_peso]
                            if peso_atual < melhor_acesso_local:
                                melhor_acesso_local = peso_atual
                    
                    if melhor_acesso_local == float('inf'):
                        print(f"Distrito '{d_info['rotulo']}' não tem acesso a nenhum '{cat_servico.capitalize()}'.")
                    else:
                        print(f"Melhor acesso para '{d_info['rotulo']}': {melhor_acesso_local:.2f} {unidade}")
                        if melhor_acesso_local > pior_acesso_geral:
                            pior_acesso_geral = melhor_acesso_local
                            distrito_com_pior_acesso = d_info['rotulo']
        
                print("\n Conclusão ")
                if distrito_com_pior_acesso:
                    print(f"O distrito com o serviço mais distante (pior acesso) é '{distrito_com_pior_acesso}',")
                    print(f"cujo {cat_servico} mais próximo está a {pior_acesso_geral:.2f} {unidade}.")
                else:
                    print("Não foi possível determinar o pior acesso (verifique se há serviços e conexões).")

            elif opcao == 13: # Conexidade
                print("\n (i) Análise de Conexidade ")
                resultado = grafo.verificar_conexidade()
                print(f"Resultado: {resultado}")
                print("(Grafo reduzido não se aplica a grafos não-direcionados)")

            elif opcao == 14: # Encerrar
                print("Encerrando a aplicação...")
                break
            
            else:
                print("Opção inválida.")
        
        except (ValueError, IndexError): print("Erro de entrada. Verifique os valores digitados.")
        except Exception as e: print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()
