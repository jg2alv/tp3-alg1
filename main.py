# Em toda essa documentacao (comentarios), "distancia" se refere
# ao numero de jogadas da rainha necessario para atingir alguma casa
# no tabuleiro (e nao o numero de casas percorridas)

# Aproximacao: algoritmo guloso: captura sempre o peao mais proximo da rainha
# Eh um teto muito bom: o numero otimo de movimentos sera sempre igual ou menor
# que essa aproximacao
def find_aprox_moves(board, n, m, k):

    # Definicao da classe grafo, contendo
    # - numero de vertices
    # - lista de adjacencia (hashmap id#vertice: id#vertice)
    # - hashmap de ids (mapeia uma casa do tabuleiro num id unico auto-incrementavel)
    # - hadmap de reverse ids (mapeia o id do vertice a casa do tabuleiro)
    # - contador de ids
    # - centro (vertice inicial da rainha)
    # - targets (lista de vertices contendo peoes)
    # - tabuleiro
    class Graph:
        def __init__(self, n, board):
            self.n = n
            self.adjlist = {}
            self.id = {}
            self.revid = {}
            self.counter = 0
            self.center = -1
            self.targets = []
            self.board = board

        # Retorna id[(i,j)] se existir
        # Cria caso create=True
        def get_node(self, i, j, create=True):
            if create and (i,j) not in self.id:
                self.id[(i,j)] = self.counter
                self.revid[self.counter] = (i,j)
                self.counter += 1
            return self.id[(i,j)]
        
        # Retorna revid[idx], ie, a casa do tabuleiro
        # correspondente ao id daquele vertice
        def get_coord(self, idx):
            return self.revid[idx]

        # Adiciona a aresta na lista de adjacencia
        # Usa set para nao duplicar os vertices de incidencia
        def add_edge(self, source, dest):
            if source not in self.adjlist:
                self.adjlist[source] = set()
            self.adjlist[source].add(dest)

            if dest not in self.adjlist:
                self.adjlist[dest] = set()
            self.adjlist[dest].add(source)

        # Adiciona as arestas no grafo como um todo
        # Essa eh a funcao que, a partir do tabuleiro de entrada,
        # constroi o grafo.
        # Posicoes bloqueadas nao possuem vertices correspondentes
        # Posicoes nao bloqueadas tem vertices que se ligam a todos os
        # demais vertices que correspondam a posicoes alcancaveis, pela rainha,
        # em uma unica jogada (a partir da casa de origem)
        def add_edges(self):
            if len(self.adjlist) > 0: return
            
            n = len(self.board)
            m = len(self.board[0])

            for i in range(n):
                for j in range(m):
                    if self.board[i][j] == '-': continue
                    source = self.get_node(i,j)

                    if self.board[i][j] == 'R': self.center = source
                    elif self.board[i][j] == 'P': self.targets.append(source)

                    # Conexao da casa atual com as demais casas acima dela
                    # Andando somente em uma direcao: cima
                    if i > 0:
                        for k in range(i-1, -1, -1):
                            if self.board[k][j] == '-': break
                            dest = self.get_node(k, j)
                            self.add_edge(source, dest)

                    # Conexao da casa atual com as demais casas abaixo dela
                    # Andando somente em uma direcao: baixo
                    if i < n-1:
                        for k in range(i+1, n):
                            if self.board[k][j] == '-': break
                            dest = self.get_node(k, j)
                            self.add_edge(source, dest)

                    # Conexao da casa atual com as demais casas a esquerda dela
                    # Andando somente em uma direcao: esquerda
                    if j > 0:
                        for k in range(j-1, -1, -1):
                            if self.board[i][k] == '-': break
                            dest = self.get_node(i, k)
                            self.add_edge(source, dest)
                    
                    # Conexao da casa atual com as demais casas a direita dela
                    # Andando somente em uma direcao: direita
                    if j < m-1:
                        for k in range(j+1, m):
                            if self.board[i][k] == '-': break
                            dest = self.get_node(i, k)
                            self.add_edge(source, dest)

                    # Conexao da casa atual com as demais casas a esquerda e acima dela (diagonal esq-cima)
                    # Andando em duas direcoes: esquerda e cima
                    k = i-1
                    l = j-1
                    while True:
                        if k < 0 or l < 0: break
                        if self.board[k][l] == '-': break
                        dest = self.get_node(k, l)
                        self.add_edge(source, dest)
                        k -= 1
                        l -= 1

                    # Conexao da casa atual com as demais casas a direita e acima dela (diagonal dir-cima)
                    # Andando em duas direcoes: direita e cima
                    k = i-1
                    l = j+1
                    while True:
                        if k < 0 or l >= m: break
                        if self.board[k][l] == '-': break
                        dest = self.get_node(k, l)
                        self.add_edge(source, dest)
                        k -= 1
                        l += 1

                    # Conexao da casa atual com as demais casas a esquerda e abaixo dela (diagonal esq-baixo)
                    # Andando em duas direcoes: esquerda e baixo
                    k = i+1
                    l = j-1
                    while True:
                        if k >= n or l < 0: break
                        if self.board[k][l] == '-': break
                        dest = self.get_node(k, l)
                        self.add_edge(source, dest)
                        k += 1
                        l -= 1

                    # Conexao da casa atual com as demais casas a direita e abaixo dela (diagonal dir-baixo)
                    # Andando em duas direcoes: direita e baixo
                    k = i+1
                    l = j+1
                    while True:
                        if k >= n or l >= m: break
                        if self.board[k][l] == '-': break
                        dest = self.get_node(k, l)
                        self.add_edge(source, dest)
                        k += 1
                        l += 1

        # Funcao de BFS padrao
        def bfs(self, s, discovered=None):
            if discovered == None:
                discovered = [False] * len(self.adjlist)

            discovered[s] = True
            layers = [[s]]
            i = 0
        
            while layers[i]:
                layers.append([])
                for node in layers[i]:
                    edges = self.adjlist[node]
                    for vertex in edges:
                        if not discovered[vertex]:
                            discovered[vertex] = True
                            layers[i+1].append(vertex)

                i += 1
        
            layers.pop()
            return layers
    
    # Definicao do grafo, adicao das arestas e inicializacao
    # do contador de movimentos
    graph = Graph(n*m, board)
    graph.add_edges()
    moves = 0

    # Para cada peao
    for _ in range(k):
        # Inicialmente, a rainha nao saira do lugar (vertice de destino = -1)
        newqueenpos = -1
        layers = graph.bfs(graph.center)
        # Para cada layer do bfs partindo da posicao atua;
        for i in range(len(layers)):
            layer = layers[i]
            for target in graph.targets:
                # Se ha algum peao naquela layer
                # Capture o peao (rainha se move pra la)
                # Remova-o da lista de peoes
                # Acrescente no contador de movimentos
                # Saida do loop mais interno
                if target in layer:
                    newqueenpos = target
                    graph.targets.remove(target)
                    moves += i
                    break
            # Se algum peao foi capturado na layer atual (eh sempre o peao mais proximo),
            # muda a rainha de posicao e ignore as camadas mais distantes do BFS
            if newqueenpos > -1:
                graph.center = newqueenpos
                break

    # Em cada iteracao do loop mais interno, um peao eh necessariamente capturado
    # Exceto caso os peoes nao sejam alcancaveis a partir da posicao inicial da rainha
    # (caso em que a rainha e/ou os peoes estao cercados por obstaculos e portanto desconectados
    # do resto do grafo)
    # Se algum movimento foi feito, moves > 0 e imprime essa quantidade
    # Caso contrario, moves = 0 e imprime -1
    return moves or -1


def find_min_moves(board, queen, pawns, n, m, k):
    # Inicialmente, calcula a distancia para qualquer casa do
    # tabuleiro a partir da posicao inicial queen=(x,y)
    # Retorna uma matriz nxm contendo a distancia minima para
    # alcancar cada posicao do tabuleiro
    # Etapa de pre-computacao
    def possible_moves(board, queen, n, m):
        # Inicializa a matriz com -1 e a posicao atual da rainha como 0
        # Adiciona a posicao inicial na fila e define as 8 direcoes possiveis
        dist = [[-1]*m for _ in range(n)]
        dist[queen[0]][queen[1]] = 0
        queue = []
        queue.append(queen)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Explora cada posicao
        while queue:
            x, y = queue.pop(0)
            # Anda nas 8 direcoes ate o fim do tabuleiro/ achar obstaculos
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                while 0 <= nx < n and 0 <= ny < m and board[nx][ny] != '-':
                    # Atualiza a matriz caso a distancia armazenada seja -1
                    if dist[nx][ny] == -1:
                        dist[nx][ny] = dist[x][y] + 1
                        queue.append((nx, ny))
                    nx += dx
                    ny += dy
        return dist

    # Algoritmo Held-Karp: resolve o problema de visitar todos os peoes no
    # menor numero de jogadas, partido da rainha e movendo-se de peao em peao
    # sem precisar retornar ao inicio (variacao do TSP)
    # `dist` eh a matriz computada abaixo, guarda as distancias entre a rainha (0)
    # e os peoes (de 1 ate k)
    def held_karp(dist, k):
        # Inicializacao da matriz dp
        # Representa o custo minimo para visitar todos os peoes do subconjunto
        # mask e terminar no peao i. Inicialmente infinito para todo muno
        # `mask` eh uma bitmask de `k` bits (1=visitado, 0=nao visitado)
        # dp eh matriz 2^k x k
        dp = [[float('inf')]*k for _ in range(1<<k)]
        
        # Comeca com a rainha (dist[0][i+1] eh a distancia da rainha ate peao i)
        # No estado inicial, apenas um peao foi visitado, pois i-esimo bit ligado
        # (terminando nele)
        for i in range(k):
            dp[1<<i][i] = dist[0][i+1]

        # Considera cada subconjunto mask de peoes visitados (sao 2^k desses subconjuntos)
        for mask in range(1<<k):
            # Para cada peao u:
            for u in range(k):
                # Se u nao foi visitado, ignora
                if not (mask & (1 << u)): continue
                # Tenta visitar um novo peao v
                for v in range(k):
                    # Se v ja foi visitado, ignora
                    if mask & (1 << v): continue
                    # Atualiza o menor custo para o novo conjunto de peoes terminando em v
                    # dist[u+1][v+1] eh a distancia de peao_u -> peao_v (indices deslocados por 1
                    # pois 0 eh a rainha)
                    dp[mask | (1 << v)][v] = min(dp[mask | (1 << v)][v], dp[mask][u] + dist[u+1][v+1])

        # Por fim, uma mask=2^k-1 representa todos os peoes visitados
        # Tenta todos os finais possiveis tendo visitado todos os peoes
        # retorna o menor
        # Checa se a resposta nao eh "muito negativa" (retorna -1 se for menor que -1)
        # ou o custo se nao for o caso
        ans = min(dp[(1<<k)-1][i] for i in range(k))
        if ans < -1: return -1
        else: return ans

    # `points` guarda uma colecao dos pontos importantes (rainha e peoes)
    # Para cada ponto, computa, com o possible_moves, a matriz de distancias
    # para ir daquele ponto ate qualquer outro
    # `distances` tambem eh uma matriz
    # distances[i][j] guarda o numero minimo de jogadas da rainha para
    # ir de points[i] ate points[j]
    # Essa matriz eh enviada como entrada pro algoritmo de Held-Karp, que precisa
    # do custo de ir de qualquer ponto ate qualquer outro
    points = [queen] + pawns
    distances = []
    for p in points:
        dist = possible_moves(board, p, n, m)
        line = []
        for q in points:
            line.append(dist[q[0]][q[1]])
        distances.append(line)

    return held_karp(distances, k)


# Leitura da entrada, construcao do tabuleiro
# Identificacao da localizacao da rainha e dos peoes
# Imprime na tela o resultado final
def main():
    n, m, k = tuple(map(int, input().split(' ')))
    board = [[''] * m] * n 
    queen = ()
    pawns = []

    for i in range(n):
        board[i] = list(input())
        for j in range(m):
            if board[i][j] == 'P':
                pawns.append((i, j))
            elif board[i][j] == 'R':
                queen = (i, j)

    print(find_min_moves(board, n, m, k))
    
if __name__ == '__main__':
    main()
