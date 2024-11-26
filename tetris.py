import pygame
import random

# Definindo as constantes de configuração do jogo
LARGURA_JOGO = 300  # Largura da tela do jogo
ALTURA_JOGO = 600   # Altura da tela do jogo
TAMANHO_CELULA = 30  # Tamanho de cada célula (ou bloco) do tetromino
LINHAS = ALTURA_JOGO // TAMANHO_CELULA  # Número de linhas da grade
COLUNAS = LARGURA_JOGO // TAMANHO_CELULA  # Número de colunas da grade

# Definindo as cores utilizando uma classe Cor
class Cor:
    """Classe que representa uma cor em formato RGB."""
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def get(self):
        """Retorna a cor em formato RGB."""
        return (self.r, self.g, self.b)

# Definindo as cores para cada tetromino
Cores = {
    'I': Cor(0, 255, 255),  # Ciano
    'T': Cor(128, 0, 128),  # Roxo
    'O': Cor(255, 255, 255),  # Branco
    'S': Cor(0, 255, 0),    # Verde
    'Z': Cor(255, 0, 0),    # Vermelho
    'L': Cor(255, 165, 0),  # Laranja
    'J': Cor(0, 0, 255),    # Azul
    'F': Cor(0,0,0)         # Preta
}

# Definindo as formas dos tetrominós (as peças do jogo)
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
    def __init__(self, forma, cor):
        self.forma = forma
        self.cor = cor  # Cor associada à peça
        self.x = COLUNAS // 2 - len(self.forma[0]) // 2
        self.y = 0  # O tetromino começa no topo da tela

    def rotacionar(self):
        """Rotaciona a forma 90 graus no sentido anti-horário."""
        self.forma = [list(row) for row in zip(*self.forma)]
        self.forma = [row[::-1] for row in self.forma]

class Tetromino(Forma):
    """Classe que representa um tetromino específico."""
    def __init__(self):
        forma_index = random.randint(0, len(formas) - 1)
        forma = formas[forma_index]
        cor = list(Cores.values())[forma_index]  # Associa a cor com a forma
        super().__init__(forma, cor)  # Chama o construtor da classe base

class Grade:
    """Classe que representa a grade onde o jogo ocorre."""
    def __init__(self):
        self.grade = [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]

    def adicionar_tetromino(self, tetromino):
        """Adiciona um tetromino à grade após ele ter alcançado o fundo."""
        for i, linha in enumerate(tetromino.forma):
            for j, valor in enumerate(linha):
                if valor:
                    self.grade[tetromino.y + i][tetromino.x + j] = tetromino.cor  # Armazena a cor no lugar da célula

    def desenhar(self, tela):
        """Desenha a grade na tela, mostrando as peças presentes."""
        for i in range(LINHAS):
            for j in range(COLUNAS):
                if self.grade[i][j]:
                    pygame.draw.rect(tela, self.grade[i][j].get(),
                                     (j * TAMANHO_CELULA, i * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    def verificar_colisao(self, tetromino):
        """Verifica se o tetromino colide com a grade ou ultrapassa os limites."""
        for i, linha in enumerate(tetromino.forma):
            for j, valor in enumerate(linha):
                if valor:
                    if (tetromino.y + i >= LINHAS) or (tetromino.x + j < 0) or (tetromino.x + j >= COLUNAS) or (self.grade[tetromino.y + i][tetromino.x + j]):
                        return True
        return False

    def remover_linhas_completas(self):
        """Remove as linhas completas e as reposiciona."""
        linhas_removidas = 0
        for i in range(LINHAS - 1, -1, -1):  # Começa da última linha
            if all(self.grade[i]):
                del self.grade[i]
                self.grade.insert(0, [0 for _ in range(COLUNAS)])
                linhas_removidas += 1
        return linhas_removidas

class Jogo:
    """Classe principal que controla o loop do jogo Tetris."""
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_JOGO, ALTURA_JOGO))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grade = Grade()
        self.tetromino = Tetromino()
        self.jogando = False  # Jogo começa pausado até clicar no botão play

    def mostrar_tela_inicio(self):
        """Exibe a tela de início com apenas o botão Play."""
        font = pygame.font.SysFont(None, 55)
        play_button_rect = pygame.Rect(LARGURA_JOGO // 2 - 50, ALTURA_JOGO // 2, 100, 50)

        while not self.jogando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if play_button_rect.collidepoint(evento.pos):
                        self.jogando = True

            self.tela.fill(Cores['F'].get())  # Fundo preto
            pygame.draw.rect(self.tela, Cores['S'].get(), play_button_rect)  # Botão Play verde
            play_text = font.render("Play", True, (0, 0, 0))  # Texto "Play" em preto
            self.tela.blit(play_text, play_text.get_rect(center=play_button_rect.center))
            pygame.display.flip()
            self.clock.tick(30)

    def rodar(self):
        """Loop principal do jogo."""
        while True:
            if not self.jogando:
                self.mostrar_tela_inicio()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Verifica se a tecla Space foi pressionada (não se está sendo mantida pressionada)
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        # Faz o "drop" do tetromino até o fundo
                        while not self.grade.verificar_colisao(self.tetromino):
                            self.tetromino.y += 1
                        self.tetromino.y -= 1

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT]:
                self.tetromino.x -= 1
                if self.grade.verificar_colisao(self.tetromino):
                    self.tetromino.x += 1
            if teclas[pygame.K_RIGHT]:
                self.tetromino.x += 1
                if self.grade.verificar_colisao(self.tetromino):
                    self.tetromino.x -= 1
            if teclas[pygame.K_DOWN]:
                self.tetromino.y += 1
                if self.grade.verificar_colisao(self.tetromino):
                    self.tetromino.y -= 1
            if teclas[pygame.K_UP]:
                self.tetromino.rotacionar()
                if self.grade.verificar_colisao(self.tetromino):
                    self.tetromino.rotacionar()

            # Queda automática do tetromino
            self.tetromino.y += 1
            if self.grade.verificar_colisao(self.tetromino):
                self.tetromino.y -= 1
                self.grade.adicionar_tetromino(self.tetromino)
                self.grade.remover_linhas_completas()
                self.tetromino = Tetromino()
                if self.grade.verificar_colisao(self.tetromino):
                    pygame.time.delay(500)  # Pausa um pouco antes de encerrar o jogo
                    pygame.quit()
                    exit()  # Fecha o jogo quando o jogador perde

            self.tela.fill(Cores['F'].get())
            self.grade.desenhar(self.tela)

            # Desenhando o tetromino atual com sua cor
            for i, linha in enumerate(self.tetromino.forma):
                for j, valor in enumerate(linha):
                    if valor:
                        pygame.draw.rect(self.tela, self.tetromino.cor.get(),
                                         ((self.tetromino.x + j) * TAMANHO_CELULA, (self.tetromino.y + i) * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

            pygame.display.flip()
            self.clock.tick(5)  # Controla a velocidade do jogo

# Inicializa e executa o jogo
if __name__ == "__main__":
    jogo = Jogo()
    jogo.rodar()
    pygame.quit()
