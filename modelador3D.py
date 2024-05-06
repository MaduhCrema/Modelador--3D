import pygame

# Inicialização do Pygame
pygame.init()

# Configurações da tela, lembrando que o Y é invertido menor em cima e maior embaixo
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))

# Listas
objetos = []
vertice_aux = []
vertices_objeto = []
arestas_objeto = []

# Estrutura do objeto
class Vertice:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.edge = None  # Uma referência para uma aresta incidente

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

class Aresta:
    def __init__(self, vertice1, vertice2):
        self.vertice_inicial = vertice1  # Vértice inicial da aresta
        self.vertice_final = vertice2  # Vértice final da aresta

    def __str__(self):
        return f"Aresta de {self.vertice_inicial} para {self.vertice_final}"

def createVertice(x, y, z):
    # O vertice_aux é para auxiliar a criação das arestas, sempre pegando o vértice final da outra aresta para ser o inicial da próxima
    vertices_objeto.append(Vertice(x, y, z))
    print("VÉRTICES:")
    for vertice in vertices_objeto:
        print(vertice)

    vertice_aux.append(Vertice(x, y, z))
    # Se houver dois vértices, cria uma aresta
    if len(vertice_aux) == 2:
        aresta_aux = Aresta(vertice_aux[0], vertice_aux[1])
        arestas_objeto.append(aresta_aux)
        print("ARESTAS")
        for aresta in arestas_objeto:
            print(aresta)
        # Considera que o vértice 2 vai para a posição 0 e a posição 1 é excluída para receber o próximo vértice
        vertice_aux[0] = vertice_aux[1]
        vertice_aux.pop(1)

#função que representa as vertice do objeto
def drawVertices():
    for vertice in vertices_objeto:
        pygame.draw.circle(tela, (0, 0, 0), (vertice.x, vertice.y), 2)  # Desenha um círculo preto

#função que representa as arestas do objeto
def drawEdges():
    for i in range(len(vertices_objeto) - 1):
        pygame.draw.line(tela, (0, 0, 0), (vertices_objeto[i].x, vertices_objeto[i].y),
                         (vertices_objeto[i + 1].x, vertices_objeto[i + 1].y), 1)
        
#Função que pega os cliques
def handleCanvasClick(event):
    if event.button == 1:  # Botão esquerdo
        rect = tela.get_rect()
        x = event.pos[0] - rect.left
        y = event.pos[1] - rect.top

        # Z é fixo, pois a projeção será paralela (não sei por que escolhi 10, saiu do meu coração?)
        z = 10
        # Criar vértices
        createVertice(x, y, z)
    if event.button == 3:  # Botão direito
        objeto = vertices_objeto.copy(), arestas_objeto.copy()
        objetos.append(objeto)
        vertices_objeto.clear()
        arestas_objeto.clear()
        print("Objeto criado")
        for vertices, arestas in objetos:
            print("Vertices:")
            for vertice in vertices:
                print(vertice)
            print("Arestas:")
            for aresta in arestas:
                print(aresta)



##############Rodando as funções#################
# Cor de fundo (branco)
cor_branca = (255, 255, 255)

# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            handleCanvasClick(evento)

    # Preenche a tela com a cor branca
    tela.fill(cor_branca)

    # Desenha os vértices
    drawVertices()

    # Desenha as arestas
    drawEdges()

    # Atualize os elementos do jogo aqui
    pygame.display.flip()  # Atualize a tela

pygame.quit()
