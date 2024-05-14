import pygame
import math
import time
# Inicialização do Pygame
pygame.init()

# Configurações da tela, lembrando que o Y é invertido menor em cima e maior embaixo
largura, altura = 800, 600
tela_principal = pygame.display.set_mode((largura, altura))
# Criação da tela de slice
largura_slice, altura_slice = 900, 700  # Ajuste conforme necessário
tela_slice = None

# Listas
objetos = []
vertice_aux = []
vertices_objeto = []
arestas_objeto = []
objeto_fatiado =[]
objeto_transformado = []

# Variaveis
num_fatias_desejado = 4
VRP = [80, 50 ,10] 
P = [20, 25, 10]
Y = [0, 1, 0]
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
# Função para normalizar um vetor
def normalize(v):
    magnitude = math.sqrt(sum(coord ** 2 for coord in v))
    return tuple(coord / magnitude for coord in v)

# Função para calcular o vetor N
def calcular_vetor_N(VRP, P):
    return tuple(P[i] - VRP[i] for i in range(3))

# Função para calcular o vetor V
def calcular_vetor_V(Y, N):
    Y = normalize(Y)  # Normaliza o vetor Y se necessário
    produto_escalar = sum(Y[i] * N[i] for i in range(3))
    return tuple(Y[i] - produto_escalar * N[i] for i in range(3))

def cross_product(V, N):
    # Calcula o produto cruzado entre os vetores V e N
    return [V[1]*N[2] - V[2]*N[1], V[2]*N[0] - V[0]*N[2], V[0]*N[1] - V[1]*N[0]]

# Passo 1: Translação do VRP para a origem do SRU
def translate_to_origin(objeto, VRP):
    translated_objeto = []
    
    # Calcula as coordenadas do VRP em relação ao SRU
    x0, y0, z0 = VRP
    
    # Translação das coordenadas do objeto para mover o VRP para a origem do SRU
    for fatia in objeto:
        fatia_transladada = []
        for vertice in fatia:
            x = vertice[0]  # Acessa o atributo x do vértice
            y = vertice[1]  # Acessa o atributo y do vértice
            z = vertice[2]  # Acessa o atributo z do vértice
            translated = (int(x) - x0, int(y) - y0, int(z) - z0)
            fatia_transladada.append(translated)
        translated_objeto.append(fatia_transladada)
        
    return translated_objeto

# Passo 2: Aplicação de rotações para alinhar os eixos do SRC com os eixos do SRU
def calculate_rotation_matrix(N, V):
    # Calcula o vetor U perpendicular a ambos V e N
    U = cross_product(V, N)
    # Normaliza os vetores
    U = normalize(U)
    V = normalize(V)
    N = normalize(N)
    #print("U,N E V NORMALIZADOS")
    #print(U, N, V)
    # Calcula a matriz de rotação composta
    R = [
        [U[0], U[1], U[2], 0],
        [V[0], V[1], V[2], 0],
        [N[0], N[1], N[2], 0],
        [0, 0, 0, 1]
    ]
    return R


# Passo 3: Aplicação da matriz de transformação composta
def apply_transformation_matrix(objeto, matrix):
    # Aplica a matriz de transformação a todas as coordenadas do objeto
    transformed_objeto = []
    for vertice in objeto:
        # Converte para coordenadas homogêneas
        vertice_homogeneo = (vertice[0], vertice[1], vertice[2], 1)
        # Multiplica a matriz de transformação pela coordenada homogênea
        new_vertice = [
            sum(matrix[i][j] * vertice_homogeneo[j] for j in range(4))
            for i in range(4)
        ][:3]  # Descarta o componente homogêneo
        transformed_objeto.append(new_vertice)
    return transformed_objeto

def matT(VRP):
    VRP_x, VRP_y, VRP_z = VRP
    T = [
        [1, 0, 0, -VRP_x],
        [0, 1, 0, -VRP_y],
        [0, 0, 1, -VRP_z],
        [0, 0, 0, 1]
    ]
    return T

def MultMat(T, R):
    M = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                M[i][j] += T[i][k] * R[k][j]
    return M




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

def drawEdgesFatiado(surface, fatias):
    for fatia in fatias:
        # Itera sobre os vértices na fatia
        for aresta in fatia[1]:
            ponto1 = (aresta[0][0], aresta[0][1])
            ponto2 = (aresta[1][0], aresta[1][1])
            # Desenha a aresta
            pygame.draw.line(surface, (255, 0, 0), ponto1, ponto2, 2)

def rotatePoint(x, y, z, theta):
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    new_x = x * cos_theta - y * sin_theta
    new_y = x * sin_theta + y * cos_theta
   # print("valores do ponto rotacionado:")
   # print(new_x, new_y, z)
    return new_x, new_y, z   

def rotateObject(objeto, theta):
    vertices_rotacionados = []  # Lista para armazenar os vértices rotacionados
    
    for vertice in objeto[0]:  # Rotaciona cada vértice 
        x = vertice.x  # coordenada x do vértice
        y = vertice.y  # coordenada y do vértice
        z = vertice.z  # coordenada z do vértice

        # Rotaciona o vértice e adiciona à lista de vértices rotacionados
        vertice_rotacionado = rotatePoint(x, y, z, theta)
        vertices_rotacionados.append(vertice_rotacionado)
        
    return vertices_rotacionados

def drawSlices(objeto, num_fatias):
    fatias = []

    for i in range(num_fatias):
        theta_fatia = math.radians(360 / num_fatias * i)
        objeto_fatia = (
            [vertice for vertice in objeto[0]],
            [aresta for aresta in objeto[1]]
        )
        fatiado = rotateObject(objeto_fatia, theta_fatia)
    
        fatiado_com_arestas = []
        #forma as arestas do objeto fatiado
        for j in range(len(fatiado) - 1):
            vertice_atual = fatiado[j]
            vertice_proximo = fatiado[j + 1]
            aresta = (vertice_atual, vertice_proximo)
            print(j)
            fatiado_com_arestas.append(aresta)
            #colcoa a ultima vertice e a primeira como aresta
            if j == len(fatiado) - 2:
                vertice_atual = fatiado[j + 1]
                vertice_proximo = fatiado[0]
                aresta = (vertice_atual, vertice_proximo)
                fatiado_com_arestas.append(aresta)                
        fatias.append((fatiado, fatiado_com_arestas))

    return fatias

def limpaListas():
    vertices_objeto.clear()
    arestas_objeto.clear() 
    vertice_aux.clear() 

#Função que pega os cliques
def handleCanvasClick(event):
    if event.button == 1:  # Botão esquerdo
        rect = tela_principal.get_rect()
        x = int(event.pos[0] - rect.left)
        y = int(event.pos[1] - rect.top)

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
        
       # print("Objeto criado")
        for vertices, arestas in objetos:
            print("Vertices:")
            for vertice in vertices:
                print(vertice)
            print("Arestas:")
            for aresta in arestas:
                print(aresta)

        #fatia os objetos
        objeto_new = drawSlices(objeto, num_fatias_desejado)
        print("NOVO fatiado")   
        print(objeto_new)
        for fatia in objeto_new:
            vertices_fatia = fatia[0]
            arestas_fatia = fatia[1]
            
            print("Vértices da fatia:")
            for vertice in vertices_fatia:
                print(vertice)
            
            print("Arestas da fatia:")
            for aresta in arestas_fatia:
                vertice_inicial = aresta[0]
                vertice_final = aresta[1]
                print(f"Aresta: {vertice_inicial} -> {vertice_final}")

        objeto_fatiado.append(objeto_new)

        limpaListas()

        #tela que printa o objeto fatiado
        global tela_slice
        tela_slice = pygame.display.set_mode((largura_slice, altura_slice))
        pygame.display.set_caption("Tela de Slice")                      
        time.sleep(2)        
        
        # Chamar a função para transladar para a origem e calcular N e V
        #objeto_transladado = translate_to_origin(objeto_new, VRP)
        # Imprimir vértices do objeto transladado
        #print("Vértices do objeto transladado:")
        #for i, fatia in enumerate(objeto_transladado):
        #    print(f"Fatia {i+1}:") 
           # Imprimir vértices da fatia
        #    print("Vértices:")
        #    for vertice in fatia:
        #        print(vertice)

        N = calcular_vetor_N(VRP, P)
        V = calcular_vetor_V(Y, N)
        #print("N e V")
        #print(N, V)
        R = calculate_rotation_matrix(N, V)
        T = matT(VRP)
        M = MultMat(T, R)
        coordenadas_dos_vértices = [vertice for fatia in objeto_new for vertice in fatia[0]]
        objeto_transformado = apply_transformation_matrix(coordenadas_dos_vértices, M)
        print("Coordenadas dos vértices transformados:")
        for vertice in objeto_transformado:
            print(vertice)


        #objeto_transformado = apply_transformation_matrix(objeto_transladado,rotation_matrix)
        

        # Imprimir vértices do objeto transformado
        #print("Vértices do objeto transformado:")
        #for vertice in objeto_transformado:
        #    print(vertice)
    
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

    for x in range(0, largura, 17):  
        for y in range(0, altura, 17):  
            pygame.draw.circle(tela_principal, (0, 0, 0), (x, y), 1)  

    # Desenha as arestas do objeto original na tela principal
    for vertices, arestas in objetos:
        drawEdges(tela_principal, arestas)

    # Desenha as vertices na tela principal
    drawVertices(tela_principal)

    if tela_slice is not None:
        tela_slice.fill(cor_branca)

        for x in range(0, largura_slice, 17):  
            for y in range(0, altura_slice, 17):  
                pygame.draw.circle(tela_slice, (0, 0, 0), (x, y), 1)  

        # Desenha as arestas do objeto fatiado na tela de slice
        for fatia in objeto_fatiado:
            drawEdgesFatiado(tela_slice, fatia)

        pygame.display.flip()
    else:
        pygame.display.flip()

pygame.quit()



       

pygame.quit()


## dividir a figura em fatias
##transformar esse objeto com o numero determiado de fatias: O número de fatias usadas na revolução foi igual a 30 em torno do objeto, ou
#seja, a cada 360º/30 = 12º cria-se uma nova seção/fatia no objeto.
#Converter as coordenadas de tela para as coordenadas de camera
# Calcular o z(zprp?) para saber o z de cada pixel de acordo com a posição da camera
# Com o z é possivel fazer o calculo de distancia com o z, e utilizar o calculo de visibilidade pelo calculo da normal, para a ocultação de superfícies
