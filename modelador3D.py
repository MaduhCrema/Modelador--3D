import pygame
import math
import time
# Inicialização do Pygame
pygame.init()

# Configurações da tela, lembrando que o Y é invertido menor em cima e maior embaixo
largura, altura = 800, 600
tela_principal = pygame.display.set_mode((largura, altura))
tela_slice = pygame.display.set_mode((largura, altura))

# Listas
objetos = []
vertice_aux = []
vertices_objeto = []
arestas_objeto = []
vertices_objt_fatiado = []
arestas_objet_fatiado = []
objetos_fatiados = []

# Variaveis
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
    vertices_objeto.append(Vertice(x, y, z))
    vertice_aux.append(Vertice(x, y, z))
    if len(vertice_aux) == 2:
        aresta_aux = Aresta(vertice_aux[0], vertice_aux[1])
        arestas_objeto.append(aresta_aux)
        # Adiciona à última lista de arestas de objetos, ou cria um novo objeto se a lista de objetos estiver vazia
        if objetos:
            objetos[-1][1].append(aresta_aux)
        else:
            objetos.append((vertices_objeto.copy(), arestas_objeto.copy()))
        vertice_aux[0] = vertice_aux[1]
        vertice_aux.pop(1)

#função que representa as vertice do objeto
def drawVertices(tela):
    for vertice in vertices_objeto:
        pygame.draw.circle(tela, (0, 0, 0), (vertice.x, vertice.y), 3)  # Desenha um círculo preto

#função que representa as arestas do objeto
def drawEdges(tela, lista_de_arestas):
    for aresta_objeto in lista_de_arestas:
        ponto1 = (aresta_objeto.vertice_inicial.x, aresta_objeto.vertice_inicial.y)
        ponto2 = (aresta_objeto.vertice_final.x, aresta_objeto.vertice_final.y)
        pygame.draw.line(tela, (0, 0, 0), ponto1, ponto2, 1)
        
def rotateObject(objeto, theta):
    print("Rotação do objeto:")
    for vertice in objeto:  # Rotaciona cada vértice
        createVertice(rotatePoint(vertice.x, vertice.y, vertice.z, theta))
        
def rotatePoint(x, y, z, theta):
    print(x,y,z,theta)
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    new_x = x * cos_theta - y * sin_theta
    new_y = x * sin_theta + y * cos_theta
    return new_x, new_y, z

def drawSlices(objeto, num_fatias):
    print("drawing slices")
    print("vertices:")
    for vertice in objeto[0]:
        print(vertice)
    print("arestas:")
    for aresta in objeto[1]:
        print(aresta)
    for i in range(num_fatias):            
        theta = math.radians(360 / num_fatias)  # Calcule o ângulo de rotação para cada fatia
        rotateObject(objeto, theta)  # Rotacione o objeto
        


def limpaListas():
    vertices_objeto.clear()
    arestas_objeto.clear() 
    vertice_aux.clear() 

#Função que pega os cliques
def handleCanvasClick(event):
    if event.button == 1:  # Botão esquerdo
        rect = tela_principal.get_rect()
        x = event.pos[0] - rect.left
        y = event.pos[1] - rect.top

        # Z é fixo, pois a projeção será paralela (não sei por que escolhi 10, saiu do meu coração?)
        z = 10
        # Criar vértices
        createVertice(x, y, z)

    if event.button == 3:  # Botão direito
        #coloca a aresta final para fechar o objeto
        aresta_aux = Aresta (vertices_objeto[-1], vertices_objeto[0])
        arestas_objeto.append(aresta_aux)
    
        #coloca as infos na lista de objetos criados
        objeto = vertices_objeto.copy(), arestas_objeto.copy()
        objetos.append(objeto)
        
        print("Objeto criado")
        for vertices, arestas in objetos:
            print("Vertices:")
            for vertice in vertices:
                print(vertice)
            print("Arestas:")
            for aresta in arestas:
                print(aresta)

        drawSlices(objeto, num_fatias_desejado)
        time.sleep(2)
        limpaListas()
        
        

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

    tela_principal.fill(cor_branca)
    tela_slice.fill(cor_branca)

    for x in range(0, largura, 17):  
        for y in range(0, altura, 17):  
            pygame.draw.circle(tela_principal, (0, 0, 0), (x, y), 1)  

    for x in range(0, largura, 17):  
        for y in range(0, altura, 17):  
            pygame.draw.circle(tela_slice, (0, 0, 0), (x, y), 1)  
    #desenha as vertices e depois apaga
    drawVertices(tela_principal)

    # Desenhe as arestas de cada objeto separadamente
    for vertices, arestas in objetos:
        drawEdges(tela_principal, arestas)

    pygame.display.flip()

pygame.quit()
