import pygame
import numpy as pd
import math
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
num_total_vertices = 0
num_fatias_desejado = 10

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
    num_total_vertices =+ 1

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
        pygame.draw.circle(tela, (0, 0, 0), (vertice.x, vertice.y), 3)  # Desenha um círculo preto

#função que representa as arestas do objeto
def drawEdges():
    for i in range(len(vertices_objeto) - 1):
        pygame.draw.line(tela, (0, 0, 0), (vertices_objeto[i].x, vertices_objeto[i].y),
                         (vertices_objeto[i + 1].x, vertices_objeto[i + 1].y), 1)
        
def rotateObject(objeto, theta):
    for vertice in objeto[0]:  # Rotaciona cada vértice
        vertice.x, vertice.y, _ = rotatePoint(vertice.x, vertice.y, vertice.z, theta)

def rotatePoint(x, y, z, theta):
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    new_x = x * cos_theta - y * sin_theta
    new_y = x * sin_theta + y * cos_theta
    return new_x, new_y, z

def drawSlices(objeto, num_fatias):
    for i in range(num_fatias):
        theta = math.radians(360 / num_fatias)  # Calcule o ângulo de rotação para cada fatia
        rotateObject(objeto, theta)  # Rotacione o objeto
        drawEdges()  # Desenhe as arestas do objeto após cada rotação

        
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
        aresta_aux = Aresta (vertices_objeto[num_total_vertices-1], vertices_objeto[0])
        arestas_objeto.append(aresta_aux)
        objeto = vertices_objeto.copy(), arestas_objeto.copy()
        objetos.append(objeto)
        #limpa as listas para o proximo objeto
      #  vertices_objeto.clear()
       # arestas_objeto.clear()

        print("Objeto criado")
        for vertices, arestas in objetos:
            print("Vertices:")
            for vertice in vertices:
                print(vertice)
            print("Arestas:")
            for aresta in arestas:
                print(aresta)

        drawSlices(objeto, num_fatias_desejado)
        vertices_objeto.clear()
        arestas_objeto.clear()

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

    # Preenche a tela com o fundo branco
    tela.fill(cor_branca)

    # Desenha os pontos pretos para criar o fundo pontilhado
    for x in range(0, largura, 17):  # Desenha pontos horizontalmente com um intervalo de 10 pixels
        for y in range(0, altura, 17):  # Desenha pontos verticalmente com um intervalo de 10 pixels
            pygame.draw.circle(tela, (0, 0, 0), (x, y), 1)  # Desenha um ponto preto de tamanho 1 em (x, y)

    # Desenha os vértices
    drawVertices()

    # Desenha as arestas
    drawEdges()

    # Atualize os elementos do jogo aqui
    pygame.display.flip()  # Atualize a tela

pygame.quit()

## dividir a figura em fatias
##transformar esse objeto com o numero determiado de fatias: O número de fatias usadas na revolução foi igual a 30 em torno do objeto, ou
#seja, a cada 360º/30 = 12º cria-se uma nova seção/fatia no objeto.
##a técnica wireframe com ocultação de superfícies(pintar a face mais longe para a mais perto(pintor) apenas nas faces 
#que estão visiveis(algoritmo de visibilidade pelo calculo da normal))
## O numero de fatia influencia na quantidade de arestas sobrepostas, tendo mais intersecções dificulta no cálculo da ocultação de fatia
## o numero de fatias influencia no algoritmo de pinto de forma que se houver mais fatias haverá mais sobreposições entre as faces na hora de pintar
