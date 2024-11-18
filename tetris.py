import pygame
import random

# Definindo as constantes de configuração do jogo
LARGURA_JOGO = 300  # Largura da tela do jogo
ALTURA_JOGO = 600   # Altura da tela do jogo
TAMANHO_CELULA = 30  # Tamanho de cada célula (ou bloco) do tetromino
LINHAS = ALTURA_JOGO // TAMANHO_CELULA  # Número de linhas da grade
COLUNAS = LARGURA_JOGO // TAMANHO_CELULA  # Número de colunas da grade

# Definindo as cores utilizadas no jogo (em formato RGB)
Cores = {
    'branco': (255, 255, 255),  # Cor branca
    'preto': (0, 0, 0),         # Cor preta
    'azul': (0, 0, 255),        # Cor azul
    'verde': (0, 255, 0),       # Cor verde
    'vermelho': (255, 0, 0),    # Cor vermelha
    'amarelo': (255, 255, 0),   # Cor amarela
    'ciano': (0, 255, 255),     # Cor ciano
    'magenta': (255, 0, 255)    # Cor magenta
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
    def __init__(self, forma):
        # A forma do tetromino é passada como argumento
        self.forma = forma
        # Inicializa a posição do tetromino no centro do tabuleiro
        self.x = COLUNAS // 2 - len(self.forma[0]) // 2
        self.y = 0  # O tetromino começa no topo da tela

    def rotacionar(self):
        """Rotaciona a forma 90 graus no sentido anti-horário."""
        # Transpõe a matriz e inverte as colunas para realizar a rotação
        self.forma = [list(row) for row in zip(*self.forma)]
        self.forma = [row[::-1] for row in self.forma]

class Tetromino(Forma):
    """Classe que representa um tetromino específico."""
    def __init__(self):
        # Escolhe uma forma aleatória de tetromino
        forma = random.choice(formas)
        super().__init__(forma)  # Chama o construtor da classe base

class Grade:
    """Classe que representa a grade onde o jogo ocorre."""
    def __init__(self):
        # Inicializa a grade como uma matriz de zeros (sem peças)
        self.grade = [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]

    def adicionar_tetromino(self, tetromino):
        """Adiciona um tetromino à grade após ele ter alcançado o fundo."""
        for i, linha in enumerate(tetromino.forma):
            for j, valor in enumerate(linha):
                if valor:
                    self.grade[tetromino.y + i][tetromino.x + j] = 1

    def desenhar(self, tela):
        """Desenha a grade na tela, mostrando as peças presentes."""
        for i in range(LINHAS):
            for j in range(COLUNAS):
                if self.grade[i][j]:
                    # Desenha um quadrado vermelho para cada célula ocupada
                    pygame.draw.rect(tela, Cores['vermelho'], (j * TAMANHO_CELULA, i * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    def verificar_colisao(self, tetromino):
        """Verifica se o tetromino colide com a grade ou ultrapassa os limites."""
        for i, linha in enumerate(tetromino.forma):
            for j, valor in enumerate(linha):
                if valor:
                    # Verifica se a célula está fora dos limites ou se há outra peça ocupando a célula
                    if (tetromino.y + i >= LINHAS) or (tetromino.x + j < 0) or (tetromino.x + j >= COLUNAS) or (self.grade[tetromino.y + i][tetromino.x + j]):
                        return True
        return False

    def remover_linhas_completas(self):
        """Remove as linhas completas e as reposiciona."""
        linhas_removidas = 0
        for i in range(LINHAS - 1, -1, -1):  # Começa da última linha
            if all(self.grade[i]):
                del self.grade[i]  # Remove a linha completa
                self.grade.insert(0, [0 for _ in range(COLUNAS)])  # Insere uma nova linha no topo
                linhas_removidas += 1
        return linhas_removidas

class Jogo:
    """Classe principal que controla o loop do jogo Tetris."""
    def __init__(self):
        pygame.init()
        # Inicializa a tela do jogo com as dimensões especificadas
        self.tela = pygame.display.set_mode((LARGURA_JOGO, ALTURA_JOGO))
        pygame.display.set_caption("Tetris")  # Define o título da janela
        self.clock = pygame.time.Clock()
        self.grade = Grade()  # Cria a grade onde os tetrominós vão cair
        self.tetromino = Tetromino()  # Cria um novo tetromino aleatório
        self.jogando = True  # O jogo começa em execução

    def rodar(self):
        """Loop principal do jogo."""
        while self.jogando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    # Se o jogador fechar a janela, o jogo termina
                    self.jogando = False

            # Verificando se alguma tecla foi pressionada para mover ou rotacionar o tetromino
            teclas = pygame.key.get_pressed()  # Obtemos o estado de todas as teclas
            if teclas[pygame.K_LEFT]:
                self.tetromino.x -= 1
                if self.grade.verificar_colisao(self.tetromino):
                    self.tetromino.x += 1  # Desfaz o movimento se houver colisão
            if teclas[pygame.K_RIGHT]:
                self.tetromino.x += 1
                if self.grade.verificar_colisao(self.tetromino):
                    self.tetromino.x -= 1  # Desfaz o movimento se houver colisão
            if teclas[pygame.K_DOWN]:
                self.tetromino.y += 1
                if self.grade.verificar_colisao(self.tetromino):
                    self.tetromino.y -= 1  # Desfaz o movimento se houver colisão
            if teclas[pygame.K_UP]:
                self.tetromino.rotacionar()
                if self.grade.verificar_colisao(self.tetromino):
                    self.tetromino.rotacionar()  # Desfaz a rotação se houver colisão

            # O tetromino desce automaticamente a cada frame
            self.tetromino.y += 1
            if self.grade.verificar_colisao(self.tetromino):
                self.tetromino.y -= 1  # Desfaz o movimento de queda se houver colisão
                self.grade.adicionar_tetromino(self.tetromino)  # Adiciona o tetromino na grade
                self.grade.remover_linhas_completas()  # Remove as linhas completas
                self.tetromino = Tetromino()  # Cria um novo tetromino
                if self.grade.verificar_colisao(self.tetromino):
                    # Se o novo tetromino colidir imediatamente, o jogo termina
                    self.jogando = False

            # Preenche o fundo da tela com a cor preta
            self.tela.fill(Cores['preto'])
            self.grade.desenhar(self.tela)  # Desenha a grade na tela

            # Desenha o tetromino atual
            for i, linha in enumerate(self.tetromino.forma):
                for j, valor in enumerate(linha):
                    if valor:
                        # Desenha cada célula do tetromino
                        pygame.draw.rect(self.tela, Cores['branco'], ((self.tetromino.x + j) * TAMANHO_CELULA, (self.tetromino.y + i) * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

            # Atualiza a tela
            pygame.display.flip()
            # Controla a velocidade do jogo (frames por segundo)
            self.clock.tick(5)

# Inicializa e executa o jogo
if __name__ == "__main__":
    jogo = Jogo()
    jogo.rodar()  # Inicia o loop principal do jogo
    pygame.quit()  # Finaliza o pygame quando o jogo terminar
