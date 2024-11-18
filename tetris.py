import pygame
import random

# Definindo as constantes do jogo
LARGURA_JOGO = 300  # Largura da tela de jogo em pixels
ALTURA_JOGO = 600  # Altura da tela de jogo em pixels
TAMANHO_CELULA = 30  # Tamanho de cada célula na grade
LINHAS = ALTURA_JOGO // TAMANHO_CELULA  # Número de linhas na grade
COLUNAS = LARGURA_JOGO // TAMANHO_CELULA  # Número de colunas na grade

# Definindo as cores
Cores = {
    'branco': (255, 255, 255),  # Cor branca (usada para desenhar os tetrominós)
    'preto': (0, 0, 0),  # Cor preta (usada para o fundo da tela)
    'azul': (0, 0, 255),  # Cor azul (usada para o tetromino I, por exemplo)
    'verde': (0, 255, 0),  # Cor verde (usada para o tetromino S, por exemplo)
    'vermelho': (255, 0, 0),  # Cor vermelha (usada para o tetromino Z, por exemplo)
    'amarelo': (255, 255, 0),  # Cor amarela (usada para o tetromino O)
    'ciano': (0, 255, 255),  # Cor ciano (usada para o tetromino J)
    'magenta': (255, 0, 255)  # Cor magenta (usada para o tetromino L)
}

# Definindo as formas dos tetrominós (as peças do Tetris)
formas = [
    [[1, 1, 1, 1]],  # Forma I
    [[1, 1, 1], [0, 1, 0]],  # Forma T
    [[1, 1], [1, 1]],  # Forma O
    [[0, 1, 1], [1, 1, 0]],  # Forma S
    [[1, 1, 0], [0, 1, 1]],  # Forma Z
    [[1, 1, 1], [1, 0, 0]],  # Forma L
    [[1, 1, 1], [0, 0, 1]]   # Forma J
]

class Forma:
    """Classe base para as formas dos tetrominós."""

    def __init__(self, forma):
        self.forma = forma  # A forma da peça (matriz 2x2 ou 3x3, etc.)
        self.x = COLUNAS // 2 - len(self.forma[0]) // 2  # Posição inicial no eixo X (centro da tela)
        self.y = 0  # Posição inicial no eixo Y (topo da tela)

    def rotacionar(self):
        """Rotaciona a forma 90 graus no sentido anti-horário."""
        # Transposta da matriz (invertendo linhas e colunas)
        self.forma = [list(row) for row in zip(*self.forma)]
        # Inverte as colunas para garantir rotação anti-horária
        self.forma = [row[::-1] for row in self.forma]

class Tetromino(Forma):
    """Classe que representa um tetromino específico, que é uma forma aleatória."""

    def __init__(self):
        forma = random.choice(formas)  # Escolhe uma forma aleatória
        super().__init__(forma)  # Chama o construtor da classe base Forma

class Grade:
    """Classe que representa a grade onde os tetrominós são desenhados e armazenados."""

    def __init__(self):
        # Inicializa a grade com células vazias (0 representa vazio)
        self.grade = [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]

    def adicionar_tetromino(self, tetromino):
        """Adiciona um tetromino na grade."""
        for i, linha in enumerate(tetromino.forma):
            for j, valor in enumerate(linha):
                if valor:  # Se o valor na célula do tetromino for 1 (parte da forma)
                    self.grade[tetromino.y + i][tetromino.x + j] = 1  # Adiciona na posição correspondente na grade

    def desenhar(self, tela):
        """Desenha a grade na tela."""
        for i in range(LINHAS):
            for j in range(COLUNAS):
                if self.grade[i][j]:  # Se a célula da grade estiver preenchida
                    pygame.draw.rect(tela, Cores['branco'], (j * TAMANHO_CELULA, i * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    def verificar_colisao(self, tetromino):
        """Verifica se o tetromino colide com algo na grade (outros tetrominós ou as bordas)."""
        for i, linha in enumerate(tetromino.forma):
            for j, valor in enumerate(linha):
                if valor:
                    if (tetromino.y + i >= LINHAS) or (tetromino.x + j < 0) or (tetromino.x + j >= COLUNAS) or (self.grade[tetromino.y + i][tetromino.x + j]):
                        return True  # Se houver colisão, retorna True
        return False  # Se não houver colisão, retorna False

    def remover_linhas_completas(self):
        """Remove as linhas completas e as empurra para baixo."""
        linhas_removidas = 0
        for i in range(LINHAS - 1, -1, -1):
            if all(self.grade[i]):  # Se a linha estiver completamente preenchida
                del self.grade[i]  # Remove a linha
                self.grade.insert(0, [0 for _ in range(COLUNAS)])  # Insere uma nova linha vazia no topo
                linhas_removidas += 1
        return linhas_removidas  # Retorna o número de linhas removidas

class Jogo:
    """Classe principal que controla o fluxo do jogo Tetris."""

    def __init__(self):
        pygame.init()  # Inicializa o pygame
        self.tela = pygame.display.set_mode((LARGURA_JOGO, ALTURA_JOGO))  # Define o tamanho da tela
        pygame.display.set_caption("Tetris")  # Define o título da janela
        self.clock = pygame.time.Clock()  # Define o relógio para controlar a velocidade do jogo
        self.grade = Grade()  # Cria uma grade de jogo
        self.tetromino = Tetromino()  # Cria o primeiro tetromino
        self.jogando = True  # Variável para controlar o estado do jogo

    def rodar(self):
        """Loop principal do jogo."""
        while self.jogando:
            for evento in pygame.event.get():  # Verifica eventos de entrada (como teclas pressionadas)
                if evento.type == pygame.QUIT:
                    self.jogando = False  # Encerra o jogo se a janela for fechada
                if evento.type == pygame.KEYDOWN:  # Se uma tecla for pressionada
                    if evento.key == pygame.K_LEFT:
                        self.tetromino.x -= 1  # Move o tetromino para a esquerda
                        if self.grade.verificar_colisao(self.tetromino):
                            self.tetromino.x += 1  # Se houver colisão, desfaz o movimento
                    if evento.key == pygame.K_RIGHT:
                        self.tetromino.x += 1  # Move o tetromino para a direita
                        if self.grade.verificar_colisao(self.tetromino):
                            self.tetromino.x -= 1  # Se houver colisão, desfaz o movimento
                    if evento.key == pygame.K_DOWN:
                        self.tetromino.y += 1  # Move o tetromino para baixo
                        if self.grade.verificar_colisao(self.tetromino):
                            self.tetromino.y -= 1  # Se houver colisão, desfaz o movimento
                    if evento.key == pygame.K_UP:
                        self.tetromino.rotacionar()  # Rotaciona o tetromino
                        if self.grade.verificar_colisao(self.tetromino):
                            self.tetromino.rotacionar()  # Se houver colisão, desfaz a rotação

            self.tetromino.y += 1  # Move o tetromino para baixo automaticamente
            if self.grade.verificar_colisao(self.tetromino):  # Se colidir
                self.tetromino.y -= 1  # Desfaz o movimento
                self.grade.adicionar_tetromino(self.tetromino)  # Adiciona o tetromino na grade
                self.grade.remover_linhas_completas()  # Remove linhas completas
                self.tetromino = Tetromino()  # Cria um novo tetromino
                if self.grade.verificar_colisao(self.tetromino):  # Se o novo tetromino colidir
                    self.jogando = False  # Fim do jogo

            self.tela.fill(Cores['preto'])  # Preenche a tela com a cor preta
            self.grade.desenhar(self.tela)  # Desenha a grade na tela

            # Desenha o tetromino atual
            for i, linha in enumerate(self.tetromino.forma):
                for j, valor in enumerate(linha):
                    if valor:
                        pygame.draw.rect(self.tela, Cores['branco'], ((self.tetromino.x + j) * TAMANHO_CELULA, (self.tetromino.y + i) * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

            pygame.display.flip()  # Atualiza a tela
            self.clock.tick(10)  # Controla a velocidade do jogo (10 frames por segundo)

if __name__ == "__main__":
    jogo = Jogo()  # Cria uma instância do jogo
    jogo.rodar()  # Inicia o loop do jogo
    pygame.quit()  # Encerra o pygame ao final do jogo
