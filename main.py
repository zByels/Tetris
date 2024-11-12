import pygame
import random

# Definindo constantes
LARGURA_JOGO = 300
ALTURA_JOGO = 600
TAMANHO_CELULA = 30
LINHAS = ALTURA_JOGO // TAMANHO_CELULA
COLUNAS = LARGURA_JOGO // TAMANHO_CELULA

# Definindo as cores
Cores = {
    'branco': (255, 255, 255),
    'preto': (0, 0, 0),
    'azul': (0, 0, 255),
    'verde': (0, 255, 0),
    'vermelho': (255, 0, 0),
    'amarelo': (255, 255, 0),
    'ciano': (0, 255, 255),
    'magenta': (255, 0, 255)
}

# Definindo as formas dos tetrominós
formas = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

class Forma:
    """Classe base para formas de tetrominós."""
    def __init__(self, forma):
        self.forma = forma
        self.x = COLUNAS // 2 - len(self.forma[0]) // 2
        self.y = 0

    def rotacionar(self):
        """Rotaciona a forma 90 graus."""
        self.forma = [list(row) for row in zip(*self.forma[::-1])]

class Tetromino(Forma):
    """Classe que representa um tetromino específico."""
    def __init__(self):
        forma = random.choice(formas)
        super().__init__(forma)

class Grade:
    """Classe que representa a grade do jogo."""
    def __init__(self):
        self.grade = [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]

    def adicionar_tetromino(self, tetromino):
        """Adiciona um tetromino à grade."""
        for i, linha in enumerate(tetromino.forma):
            for j, valor in enumerate(linha):
                if valor:
                    self.grade[tetromino.y + i][tetromino.x + j] = 1

    def desenhar(self, tela):
        """Desenha a grade na tela."""
        for i in range(LINHAS):
            for j in range(COLUNAS):
                if self.grade[i][j]:
                    pygame.draw.rect(tela, Cores['branco'], (j * TAMANHO_CELULA, i * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    def verificar_colisao(self, tetromino):
        """Verifica se o tetromino colide com a grade."""
        for i, linha in enumerate(tetromino.forma):
            for j, valor in enumerate(linha):
                if valor:
                    if (tetromino.y + i >= LINHAS) or (tetromino.x + j < 0) or (tetromino.x + j >= COLUNAS) or (self.grade[tetromino.y + i][tetromino.x + j]):
                        return True
        return False

    def remover_linhas_completas(self):
        """Remove linhas completas da grade."""
        linhas_removidas = 0
        for i in range(LINHAS - 1, -1, -1):
            if all(self.grade[i]):
                del self.grade[i]
                self.grade.insert(0, [0 for _ in range(COLUNAS)])
                linhas_removidas += 1
        return linhas_removidas

class Jogo:
    """Classe principal do jogo Tetris."""
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_JOGO, ALTURA_JOGO))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grade = Grade()
        self.tetromino = Tetromino()
        self.jogando = True

    def rodar(self):
        """Loop principal do jogo."""
        while self.jogando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.jogando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_LEFT:
                        self.tetromino.x -= 1
                        if self.grade.verificar_colisao(self.tetromino):
                            self.tetromino.x += 1
                    if evento.key == pygame.K_RIGHT:
                        self.tetromino.x += 1
                        if self.grade.verificar_colisao(self.tetromino):
                            self.tetromino.x -= 1
                    if evento.key == pygame.K_DOWN:
                        self.tetromino.y += 1
                        if self.grade.verificar_colisao(self.tetromino):
                            self.tetromino.y -= 1
                    if evento.key == pygame.K_UP:
                        self.tetromino.rotacionar()
                        if self.grade.verificar_colisao(self.tetromino):
                            self.tetromino.rotacionar()  # Rotaciona de volta se colidir

            self.tetromino.y += 1
            if self.grade.verificar_colisao(self.tetromino):
                self.tetromino.y -= 1
                self.grade.adicionar_tetromino(self.tetromino)
                self.grade.remover_linhas_completas()
                self.tetromino = Tetromino()
                if self.grade.verificar_colisao(self.tetromino):
                    self.jogando = False  # Fim do jogo se o novo tetromino colidir

            self.tela.fill(Cores['preto'])
            self.grade.desenhar(self.tela)

            # Desenhar o tetromino atual
            for i, linha in enumerate(self.tetromino.forma):
                for j, valor in enumerate(linha):
                    if valor:
                        pygame.draw.rect(self.tela, Cores['branco'], ((self.tetromino.x + j) * TAMANHO_CELULA, (self.tetromino.y + i) * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

            pygame.display.flip()
            self.clock.tick(10)  # Controla a velocidade do jogo

if __name__ == "__main__":
    jogo = Jogo()
    jogo.rodar()
    pygame.quit()
