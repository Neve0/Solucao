#PROVA OBI 2021 NÍVEL SENIOR - FASE 3
#QUESTÃO: DONA MINHOCA

# Por se tratar de um problema envolvendo objetos relacionados entre si, no caso do problema, as salas são relacionadas entre elas através de túneis, o uso de 
#grafos se mostra uma boa alternativa.
# A primeira parte do problema pede que se determine o número de salas que compõem o ciclo de maior de comprimento. Esse problema pode ser adaptado 
#para a teoria dos grafos da seguinte maneira: Dado um grafo(casa) e escolhido um vértice(sala) arbitrário, que sera denominado vértice origem, pertencente 
#ao grafo, determine o vértice mais distante do vértice origem e sua distância.
# A segunda parte do problema pede que se descubra de quantas formas o ciclo de maior comprimento pode ser construído no grafo. 
#No sentido de grafos entende-se que dado um grafo e a maior distância que um vértice está de outro, é suficiênte contar quantas vezes outros vértices 
#estão a essa mesma distância de outros.

#Criação do grafo: 

#Como o vértice terá atributos como id, color e dist, optei por usar classes pela simplicidade e organização.
# Para fins de simplicidade em relação ao manuséio dos inputs, os vértices adjacentes são representandos através de um dicionário no qual 
#a chave é o id do vértice adjacente. 
class vertex:
    def __init__(self, id):
        self.id = id
        self.adj = {}
        self.color = None
        self.dist = 1

    def addAdj(self, id_adj, weight=0):
        self.adj[id_adj] = weight

    def __iter__(self):
        return self.adj.keys()

#O grafo será representando através de um dicionário no qual a chave é o id do vértice e o objeto guardado na chave é o próprio objeto vertex
graph = {}

num_salas = int(input()) - 1
count = 0

#O dicionário dict_list guardará a tupla (vértice_origem, vértice_destino) e a distância entre eles será a chave do dicionário, estamos interessados na 
#chave de maior valor já que esta guarda as combinações entre vértices de maior distância.
dict_dist = {}

while count < num_salas:
    idVertex, idVertex_adj = input().split()
    if idVertex not in graph.keys():
        graph[idVertex] = vertex(idVertex)

    if idVertex_adj not in graph.keys():
        graph[idVertex_adj] = vertex(idVertex_adj)

    graph[idVertex].addAdj(idVertex_adj)
    graph[idVertex_adj].addAdj(idVertex)

    count += 1

# Resolução do problema:

# Como o problema envolve o cálculo de distâncias em um grafo sem peso, escolhi implementar o algoritimo denominado "busca em largura (breadth-first search)" 
#já que este calcula a distância que um vértice origem está de todos os outros vértices do grafo com base unicamente no número de vértices entre eles. 
#Tratando os vértices como salas da casa da minhoca notamos como a função do algoritimo se encaixa na resolução do problema.
# Durante a execução do algoritimo,logo após calcularmos a distância na qual um vértice do grafo está do vértice origem escolhido no argumento da função, 
#armazenamos a distância do vértice no dicionário dict_list.
# Ao final da execução do algoritimo o dicionário dict_list terá todas as combinaçôes de distância do vértice de origem a outros vértices.

def BFS(grafo, source_vertex):
    for vertex in graph.values():
        vertex.color = 'white'
        vertex.dist = 0
    
    source_vertex.dist = 1
    fila = []
    fila.append(source_vertex)
    while fila != []:
        vertex = fila.pop(0)

        for id_adjVertex in vertex.adj.keys():
            adj_vertex = graph[id_adjVertex]
            if adj_vertex.color == "white":
                adj_vertex.dist = vertex.dist + 1
                if adj_vertex.dist not in dict_dist.keys():
                    dict_dist[adj_vertex.dist] = []

                dict_dist[adj_vertex.dist].append((int(source_vertex.id), int(adj_vertex.id)))

                fila.append(adj_vertex)

        vertex.color = "black"


#Como não há especeficação de onde devemos começar a contrução do tunel, teremos de calcular todas as possíbilades de combinações de distância, para 
#isso executaremos o algoritimo BFS usando todos os vértices do grafo como vértcies de origem.
#Ao final do loop o dicionário dict_list irá conter todas as combinações de distâncias possíveis na forma de lista de tuplas, como dito acima estamos 
#interessados nas combinações de maior distância.
for vertex in graph.values():
    BFS(graph, vertex)

#Para acessar as combinações relembro que na construção do dicionário dict_dist as chaves são as distâncias de vértices, logo para acessarmos as 
#combinações de maior distância basta transformar as chaves do dicionário em uma lista e armazenamos o maior valor da lista. 
max_key = max(dict_dist.keys())

#Um dos problemas da metodologia adotada na resolução do problema está na criação de duplicatas, por exemplo, suponha que a maior distância em um grafo de 
#5 vértices nomeados de 1 a 5 é 3 e que as combinações corretas são (1,3) e (5,2) se vizualizarmos o dicionário dict_dist encontrariamos os seguintes 
#valores (1,3), (3,1) (5,2) e (2,5) esse tipo de "duplicata inversa" é indejesejado já que o problema considera as distâncias (1,3) (3,1) como sendo uma 
#única combinação.
#Uma solução simples para esse problema seria obter o tamanho da lista e dividir por 2 isso resultaria no número correto de combinações que criam o ciclo 
#de maior comprimento
#A solução adotada aqui foi transformar a lista em um frozenset, já que o objeto frozenset remove duplicatas do tipo (1,0) e (1,0), mas também duplicatas 
#do tipo (1,0) e (0,1), e depois reverter o objeto denovo para uma lista de tuplas.

dict_dist[max_key] = set(map(frozenset, dict_dist[max_key]))
dict_dist[max_key] = list(map(tuple, dict_dist[max_key]))


print(max_key) #maior distância possível; chave de maior valor do dicionário dict_dist
print(len(dict_dist[max_key])) #número de combinações possíveis; número de combinações no dicionário de chave max_key




