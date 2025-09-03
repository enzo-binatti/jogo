import pygame
import random
import math
import os
import sys

# Inicializar o Pygame
pygame.init()
pygame.mixer.init()

# Configurações da tela
LARGURA, ALTURA = 1024, 768
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Aventura Espacial - Edição Premium")
relogio = pygame.time.Clock()

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
ROXO = (128, 0, 128)
CIANO = (0, 255, 255)
LARANJA = (255, 165, 0)

# Criar diretório de assets se não existir
if not os.path.exists('assets'):
    os.makedirs('assets')

# Gerar sprites programaticamente (caso não tenha imagens)
def gerar_sprite_nave():
    superficie = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    # Corpo principal da nave
    pygame.draw.polygon(superficie, AZUL, [(32, 0), (10, 50), (54, 50)])
    
    # Detalhes na nave
    pygame.draw.polygon(superficie, CIANO, [(32, 15), (20, 45), (44, 45)])
    pygame.draw.circle(superficie, AMARELO, (32, 25), 5)
    
    # Propulsores
    pygame.draw.rect(superficie, LARANJA, (20, 50, 6, 10))
    pygame.draw.rect(superficie, LARANJA, (38, 50, 6, 10))
    
    return superficie

def gerar_sprite_inimigo(tipo=0):
    superficie = pygame.Surface((48, 48), pygame.SRCALPHA)
    cores = [VERMELHO, ROXO, LARANJA]
    
    if tipo == 0:  # Inimigo básico
        pygame.draw.polygon(superficie, cores[tipo], [(24, 0), (0, 48), (48, 48)])
        pygame.draw.circle(superficie, AMARELO, (24, 15), 8)
    elif tipo == 1:  # Inimigo intermediário
        pygame.draw.polygon(superficie, cores[tipo], [(24, 0), (0, 30), (0, 48), (48, 48), (48, 30)])
        pygame.draw.circle(superficie, CIANO, (24, 15), 6)
    else:  # Inimigo avançado
        pontos = [(24, 0), (10, 20), (0, 40), (15, 48), (33, 48), (48, 40), (38, 20)]
        pygame.draw.polygon(superficie, cores[tipo], pontos)
        pygame.draw.circle(superficie, VERMELHO, (24, 25), 5)
    
    return superficie

def gerar_sprite_tiro():
    superficie = pygame.Surface((8, 20), pygame.SRCALPHA)
    
    # Tiro com gradiente
    for i in range(20):
        alpha = 255 - (i * 12)
        if alpha < 0: alpha = 0
        cor = (255, 255, 200, alpha)
        pygame.draw.rect(superficie, cor, (2, i, 4, 1))
    
    pygame.draw.rect(superficie, CIANO, (0, 0, 8, 4))
    pygame.draw.rect(superficie, AMARELO, (2, 4, 4, 12))
    
    return superficie

def gerar_sprite_powerup(tipo):
    superficie = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    if tipo == 'vida':
        pygame.draw.circle(superficie, VERMELHO, (16, 16), 12)
        pygame.draw.circle(superficie, (255, 150, 150), (16, 16), 8)
        # Símbolo de coração
        pontos = [(16, 8), (22, 14), (16, 24), (10, 14)]
        pygame.draw.polygon(superficie, BRANCO, pontos)
    else:  # 'arma'
        pygame.draw.circle(superficie, VERDE, (16, 16), 12)
        pygame.draw.circle(superficie, (150, 255, 150), (16, 16), 8)
        # Símbolo de arma
        pygame.draw.rect(superficie, BRANCO, (12, 10, 8, 12))
        pygame.draw.rect(superficie, BRANCO, (8, 16, 16, 4))
    
    # Brilho exterior
    pygame.draw.circle(superficie, (255, 255, 255, 50), (16, 16), 16, 2)
    
    return superficie

def gerar_sprite_explosao(tamanho):
    superficie = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    
    # Explosão com partículas
    centro = tamanho // 2
    raio = tamanho // 2
    
    # Núcleo da explosão
    pygame.draw.circle(superficie, (255, 255, 200), (centro, centro), raio // 3)
    
    # Partículas
    for i in range(15):
        angulo = random.uniform(0, 2 * math.pi)
        distancia = random.uniform(raio // 3, raio)
        x = centro + int(math.cos(angulo) * distancia)
        y = centro + int(math.sin(angulo) * distancia)
        tamanho_part = random.randint(2, 6)
        cor = random.choice([(255, 200, 0), (255, 100, 0), (255, 50, 0)])
        pygame.draw.circle(superficie, cor, (x, y), tamanho_part)
    
    return superficie

def gerar_fundo_estrelas():
    superficie = pygame.Surface((LARGURA, ALTURA))
    superficie.fill(PRETO)
    
    # Estrelas básicas
    for i in range(200):
        x = random.randint(0, LARGURA - 1)
        y = random.randint(0, ALTURA - 1)
        tamanho = random.randint(1, 3)
        brilho = random.randint(150, 255)
        pygame.draw.circle(superficie, (brilho, brilho, brilho), (x, y), tamanho)
    
    # Estrelas brilhantes
    for i in range(20):
        x = random.randint(0, LARGURA - 1)
        y = random.randint(0, ALTURA - 1)
        tamanho = random.randint(2, 4)
        cor = random.choice([(255, 255, 200), (200, 200, 255), (255, 200, 200)])
        pygame.draw.circle(superficie, cor, (x, y), tamanho)
        pygame.draw.circle(superficie, BRANCO, (x, y), 1)
    
    # Nebulosa
    for i in range(5):
        x = random.randint(0, LARGURA - 1)
        y = random.randint(0, ALTURA - 1)
        raio = random.randint(50, 200)
        cor = random.choice([(30, 10, 50), (10, 30, 50), (50, 10, 30)])
        for r in range(raio, 0, -5):
            alpha = max(0, 100 - (raio - r) * 2)
            s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*cor, alpha), (r, r), r)
            superficie.blit(s, (x - r, y - r))
    
    return superficie

# Carregar sprites
nave_img = gerar_sprite_nave()
inimigo_imgs = [gerar_sprite_inimigo(i) for i in range(3)]
tiro_img = gerar_sprite_tiro()
powerup_imgs = {
    'vida': gerar_sprite_powerup('vida'),
    'arma': gerar_sprite_powerup('arma')
}
explosao_imgs = [gerar_sprite_explosao(64) for _ in range(5)]
fundo_estrelas = gerar_fundo_estrelas()

# Efeitos de partículas
class Particula:
    def __init__(self, x, y, cor, velocidade=1, tamanho=2, vida=30):
        self.x = x
        self.y = y
        self.cor = cor
        self.velocidade = velocidade
        self.tamanho = tamanho
        self.vida = vida
        self.vida_max = vida
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * random.uniform(0.5, 2) * velocidade
        self.vy = math.sin(angle) * random.uniform(0.5, 2) * velocidade
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1
        self.tamanho = max(0, self.tamanho * (self.vida / self.vida_max))
        return self.vida <= 0
    
    def draw(self, surface):
        alpha = 255 * (self.vida / self.vida_max)
        s = pygame.Surface((self.tamanho*2, self.tamanho*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.cor, alpha), (self.tamanho, self.tamanho), self.tamanho)
        surface.blit(s, (int(self.x - self.tamanho), int(self.y - self.tamanho)))

class SistemaParticulas:
    def __init__(self):
        self.particulas = []
    
    def add_particulas(self, x, y, cor, count=10, velocidade=1, tamanho=2, vida=30):
        for _ in range(count):
            self.particulas.append(Particula(x, y, cor, velocidade, tamanho, vida))
    
    def update(self):
        for particula in self.particulas[:]:
            if particula.update():
                self.particulas.remove(particula)
    
    def draw(self, surface):
        for particula in self.particulas:
            particula.draw(surface)

# Classes do jogo
class Jogador:
    def __init__(self, todos_sprites, sistemas_particulas):
        self.image = nave_img
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA // 2
        self.rect.bottom = ALTURA - 50
        self.velocidade = 8
        self.vidas = 3
        self.pontuacao = 0
        self.powerup_tempo = 0
        self.powerup_ativo = False
        self.ultimo_tiro = pygame.time.get_ticks()
        self.tempo_recarga = 250
        self.todos_sprites = todos_sprites
        self.sistemas_particulas = sistemas_particulas
        self.invulneravel = False
        self.invulneravel_tempo = 0
    
    def update(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
            # Partículas do propulsor
            self.sistemas_particulas.add_particulas(
                self.rect.centerx + 15, self.rect.bottom, 
                LARANJA, 2, 2, 3, 15
            )
        if teclas[pygame.K_RIGHT] and self.rect.right < LARGURA:
            self.rect.x += self.velocidade
            # Partículas do propulsor
            self.sistemas_particulas.add_particulas(
                self.rect.centerx - 15, self.rect.bottom, 
                LARANJA, 2, 2, 3, 15
            )
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidade
            # Partículas do propulsor
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.bottom, 
                LARANJA, 3, 3, 4, 20
            )
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTURA:
            self.rect.y += self.velocidade
            # Partículas do propulsor traseiro
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.top, 
                AZUL, 2, 1, 2, 10
            )
            
        # Partículas contínuas dos propulsores
        self.sistemas_particulas.add_particulas(
            self.rect.centerx + 15, self.rect.bottom, 
            LARANJA, 1, 2, 2, 10
        )
        self.sistemas_particulas.add_particulas(
            self.rect.centerx - 15, self.rect.bottom, 
            LARANJA, 1, 2, 2, 10
        )
            
        if self.powerup_ativo and pygame.time.get_ticks() > self.powerup_tempo:
            self.powerup_ativo = False
            self.tempo_recarga = 250
            
        # Gerenciar invulnerabilidade
        if self.invulneravel:
            if pygame.time.get_ticks() > self.invulneravel_tempo:
                self.invulneravel = False
            # Piscar quando invulnerável
            if pygame.time.get_ticks() % 200 < 100:
                self.image.set_alpha(128)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

    def atirar(self, tiros):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.tempo_recarga:
            self.ultimo_tiro = agora
            tiros.append(Tiro(self.rect.centerx, self.rect.top, 0, self.todos_sprites, self.sistemas_particulas))
            
            # Efeito de partículas ao atirar
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.top, 
                CIANO, 5, 3, 2, 15
            )
            
            if self.powerup_ativo:
                tiros.append(Tiro(self.rect.centerx, self.rect.top, -1, self.todos_sprites, self.sistemas_particulas))
                tiros.append(Tiro(self.rect.centerx, self.rect.top, 1, self.todos_sprites, self.sistemas_particulas))

    def powerup(self):
        self.powerup_ativo = True
        self.powerup_tempo = pygame.time.get_ticks() + 5000
        self.tempo_recarga = 100
        
        # Efeito visual de power-up
        for _ in range(20):
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.centery,
                VERDE, 1, 2, 4, 30
            )

    def tomar_dano(self):
        if not self.invulneravel:
            self.vidas -= 1
            self.invulneravel = True
            self.invulneravel_tempo = pygame.time.get_ticks() + 2000  # 2 segundos de invulnerabilidade
            
            # Efeito de partículas ao tomar dano
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.centery,
                VERMELHO, 20, 3, 4, 40
            )
            
            return self.vidas <= 0
        return False

class Inimigo:
    def __init__(self, nivel, todos_sprites, sistemas_particulas):
        self.tipo = min(nivel // 2, 2)  # Tipo baseado no nível
        self.image = inimigo_imgs[self.tipo]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(LARGURA - self.rect.width)
        self.rect.y = random.randrange(-150, -50)
        self.speedy = random.randrange(1, 3 + nivel // 2)
        self.speedx = random.randrange(-2 - nivel // 2, 2 + nivel // 2)
        self.nivel = nivel
        self.todos_sprites = todos_sprites
        self.sistemas_particulas = sistemas_particulas
        self.vida = 1 + self.tipo  # Inimigos mais fortes têm mais vida
        self.raio_visao = 300 + self.tipo * 100  # Raio de perseguição
        
        # Partículas de propulsão
        self.particula_timer = 0

    def update(self, jogador_x, jogador_y):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        # Partículas de propulsão
        self.particula_timer += 1
        if self.particula_timer >= 5:
            self.particula_timer = 0
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.bottom,
                (200, 100, 100), 1, 1, 2, 20
            )
        
        # IA: perseguir jogador se estiver dentro do raio de visão
        dx = jogador_x - self.rect.centerx
        dy = jogador_y - self.rect.centery
        distancia = math.sqrt(dx*dx + dy*dy)
        
        if distancia < self.raio_visao and self.tipo > 0:
            # Suavizar o movimento de perseguição
            fator = 0.05 + self.tipo * 0.02
            self.rect.x += dx * fator
            self.rect.y += dy * fator
        elif self.tipo == 2:  # Inimigos avançados têm movimento sinuoso
            self.rect.x += math.sin(pygame.time.get_ticks() * 0.001 + self.rect.y * 0.1) * 2
        
        # Se sair da tela, reaparece em cima
        if self.rect.top > ALTURA + 10 or self.rect.left < -50 or self.rect.right > LARGURA + 50:
            self.rect.x = random.randrange(LARGURA - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4 + self.nivel // 2)

    def tomar_dano(self, dano=1):
        self.vida -= dano
        
        # Efeito de partículas ao tomar dano
        self.sistemas_particulas.add_particulas(
            self.rect.centerx, self.rect.centery,
            (255, 200, 100), 10, 2, 3, 25
        )
        
        return self.vida <= 0

class Tiro:
    def __init__(self, x, y, direcao, todos_sprites, sistemas_particulas):
        self.image = tiro_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        self.direcao = direcao
        self.todos_sprites = todos_sprites
        self.sistemas_particulas = sistemas_particulas
        self.particula_timer = 0

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.direcao * 5
        
        # Partículas de rastro
        self.particula_timer += 1
        if self.particula_timer >= 2:
            self.particula_timer = 0
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.bottom,
                CIANO, 1, 1, 2, 15
            )
        
        # Se sair da tela, marca para remoção
        return self.rect.bottom < 0

class PowerUp:
    def __init__(self, x, y, tipo, todos_sprites, sistemas_particulas):
        self.type = tipo
        self.image = powerup_imgs[tipo]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = 2
        self.todos_sprites = todos_sprites
        self.sistemas_particulas = sistemas_particulas
        self.oscillate = 0

    def update(self):
        self.rect.y += self.speedy
        
        # Oscilação para efeito visual
        self.oscillate += 0.1
        self.rect.x += math.sin(self.oscillate) * 0.5
        
        # Partículas de brilho
        if random.random() < 0.1:
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.centery,
                VERDE if self.type == 'arma' else VERMELHO, 
                3, 1, 2, 30
            )
        
        return self.rect.top > ALTURA  # Retorna True se saiu da tela

# Função para mostrar texto com efeito
def mostrar_texto(surface, texto, tamanho, x, y, cor=BRANCO, sombra=True):
    fonte = pygame.font.SysFont("Arial", tamanho)
    
    if sombra:
        texto_sombra = fonte.render(texto, True, (0, 0, 0))
        sombra_rect = texto_sombra.get_rect()
        sombra_rect.midtop = (x + 2, y + 2)
        surface.blit(texto_sombra, sombra_rect)
    
    texto_surface = fonte.render(texto, True, cor)
    texto_rect = texto_surface.get_rect()
    texto_rect.midtop = (x, y)
    surface.blit(texto_surface, texto_rect)

# Função para desenhar barra de vida com estilo
def desenhar_barra_vida(surface, x, y, porcentagem, largura=100, altura=15):
    # Fundo
    pygame.draw.rect(surface, (50, 50, 50), (x, y, largura, altura))
    
    # Vida
    fill = max(0, (porcentagem / 100) * largura)
    if fill > 0:
        # Gradiente de cor
        for i in range(int(fill)):
            cor_progresso = i / fill
            r = int(255 * (1 - cor_progresso) + 0 * cor_progresso)
            g = int(0 * (1 - cor_progresso) + 255 * cor_progresso)
            pygame.draw.rect(surface, (r, g, 0), (x + i, y, 1, altura))
    
    # Borda
    pygame.draw.rect(surface, BRANCO, (x, y, largura, altura), 2)
    
    # Detalhes internos
    for i in range(0, largura, 5):
        pygame.draw.line(surface, (100, 100, 100), (x + i, y), (x + i, y + altura), 1)

# Função para mostrar tela de início com efeitos
def mostrar_tela_inicio(sistemas_particulas):
    tela.fill(PRETO)
    tela.blit(fundo_estrelas, (0, 0))
    
    # Adicionar partículas para efeito
    for _ in range(5):
        x = random.randint(0, LARGURA)
        y = random.randint(0, ALTURA)
        sistemas_particulas.add_particulas(x, y, CIANO, 10, 2, 3, 50)
    
    sistemas_particulas.update()
    sistemas_particulas.draw(tela)
    
    # Título com efeito
    mostrar_texto(tela, "AVENTURA ESPACIAL", 72, LARGURA // 2, ALTURA // 4, CIANO)
    mostrar_texto(tela, "Edição Premium", 36, LARGURA // 2, ALTURA // 4 + 70, AMARELO)
    
    # Instruções
    mostrar_texto(tela, "Setas para mover, Espaço para atirar", 28, LARGURA // 2, ALTURA // 2)
    mostrar_texto(tela, "Colete power-ups para melhorar sua nave", 24, LARGURA // 2, ALTURA // 2 + 40)
    mostrar_texto(tela, "Pressione qualquer tecla para começar", 22, LARGURA // 2, ALTURA * 3/4)
    
    pygame.display.flip()
    
    esperando = True
    while esperando:
        relogio.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYUP:
                esperando = False

# Função para mostrar tela de game over com estilo
def mostrar_game_over(pontuacao, nivel, sistemas_particulas):
    tela.fill(PRETO)
    tela.blit(fundo_estrelas, (0, 0))
    
    # Adicionar partículas para efeito
    for _ in range(10):
        x = random.randint(0, LARGURA)
        y = random.randint(0, ALTURA)
        sistemas_particulas.add_particulas(x, y, VERMELHO, 15, 2, 4, 60)
    
    sistemas_particulas.update()
    sistemas_particulas.draw(tela)
    
    mostrar_texto(tela, "FIM DE JOGO", 80, LARGURA // 2, ALTURA // 4, VERMELHO)
    mostrar_texto(tela, f"Pontuação: {pontuacao}", 40, LARGURA // 2, ALTURA // 2 - 30)
    mostrar_texto(tela, f"Nível alcançado: {nivel}", 40, LARGURA // 2, ALTURA // 2 + 20)
    mostrar_texto(tela, "Pressione qualquer tecla para jogar novamente", 24, LARGURA // 2, ALTURA * 3/4)
    
    pygame.display.flip()
    
    esperando = True
    while esperando:
        relogio.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYUP:
                esperando = False

# Função para mostrar tela de nível completo
def mostrar_nivel_completo(nivel, sistemas_particulas):
    tela.fill(PRETO)
    tela.blit(fundo_estrelas, (0, 0))
    
    # Adicionar partículas para efeito
    for _ in range(15):
        x = random.randint(0, LARGURA)
        y = random.randint(0, ALTURA)
        sistemas_particulas.add_particulas(x, y, VERDE, 20, 2, 4, 70)
    
    sistemas_particulas.update()
    sistemas_particulas.draw(tela)
    
    mostrar_texto(tela, "NÍVEL COMPLETO!", 64, LARGURA // 2, ALTURA // 3, VERDE)
    mostrar_texto(tela, f"Próximo nível: {nivel + 1}", 48, LARGURA // 2, ALTURA // 2)
    mostrar_texto(tela, "Preparando-se para o próximo desafio...", 28, LARGURA // 2, ALTURA * 2/3)
    
    pygame.display.flip()
    pygame.time.delay(2500)  # 2.5 segundos

# Inicialização do jogo
sistemas_particulas = SistemaParticulas()
mostrar_tela_inicio(sistemas_particulas)

# Loop principal do jogo
game_over = False
executando = True
nivel = 1
inimigos_por_nivel = 8

while executando:
    if game_over:
        mostrar_game_over(jogador.pontuacao, nivel, sistemas_particulas)
        game_over = False
        nivel = 1
        inimigos_por_nivel = 8
    
    # Inicializar listas de objetos
    todos_sprites = []
    inimigos = []
    tiros = []
    powerups = []
    
    # Criar jogador
    jogador = Jogador(todos_sprites, sistemas_particulas)
    todos_sprites.append(jogador)
    
    # Criar inimigos
    for i in range(inimigos_por_nivel):
        inimigo = Inimigo(nivel, todos_sprites, sistemas_particulas)
        inimigos.append(inimigo)
        todos_sprites.append(inimigo)
    
    # Timer para power-ups
    poder_spawn_timer = 0
    
    # Loop do nível
    rodando = True
    while rodando:
        relogio.tick(60)
        
        # Processar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                executando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogador.atirar(tiros)
        
        # Atualizar jogador
        teclas = pygame.key.get_pressed()
        jogador.update(teclas)
        
        # Atualizar sistemas de partículas
        sistemas_particulas.update()
        
        # Atualizar inimigos
        for inimigo in inimigos[:]:
            inimigo.update(jogador.rect.centerx, jogador.rect.centery)
            
            # Verificar colisão com jogador
            if jogador.rect.colliderect(inimigo.rect):
                if jogador.tomar_dano():
                    game_over = True
                    rodando = False
        
        # Atualizar tiros
        for tiro in tiros[:]:
            if tiro.update():  # Se retornar True, saiu da tela
                tiros.remove(tiro)
                continue
                
            # Verificar colisão com inimigos
            for inimigo in inimigos[:]:
                if tiro.rect.colliderect(inimigo.rect):
                    if inimigo.tomar_dano():  # Se retornar True, inimigo morreu
                        jogador.pontuacao += 100 + inimigo.tipo * 50
                        inimigos.remove(inimigo)
                        
                        # Efeito de explosão
                        sistemas_particulas.add_particulas(
                            inimigo.rect.centerx, inimigo.rect.centery,
                            LARANJA, 30, 3, 5, 50
                        )
                        
                        # Chance de dropar power-up
                        if random.random() > 0.7:
                            tipo = random.choice(['vida', 'arma'])
                            powerup = PowerUp(inimigo.rect.centerx, inimigo.rect.centery, 
                                            tipo, todos_sprites, sistemas_particulas)
                            powerups.append(powerup)
                            todos_sprites.append(powerup)
                    
                    if tiro in tiros:
                        tiros.remove(tiro)
                    break
        
        # Atualizar power-ups
        poder_spawn_timer += 1
        if poder_spawn_timer >= 900:  # 15 segundos em 60 FPS
            poder_spawn_timer = 0
            tipo = random.choice(['vida', 'arma'])
            powerup = PowerUp(random.randint(50, LARGURA-50), -30, 
                            tipo, todos_sprites, sistemas_particulas)
            powerups.append(powerup)
            todos_sprites.append(powerup)
            
        for powerup in powerups[:]:
            if powerup.update():  # Se saiu da tela
                powerups.remove(powerup)
                todos_sprites.remove(powerup)
                continue
                
            # Verificar colisão com jogador
            if jogador.rect.colliderect(powerup.rect):
                if powerup.type == 'vida':
                    jogador.vidas += 1
                elif powerup.type == 'arma':
                    jogador.powerup()
                
                # Efeito de coleta
                sistemas_particulas.add_particulas(
                    powerup.rect.centerx, powerup.rect.centery,
                    VERDE if powerup.type == 'arma' else VERMELHO, 
                    20, 2, 4, 40
                )
                
                powerups.remove(powerup)
                todos_sprites.remove(powerup)
        
        # Verificar se nível completo
        if len(inimigos) == 0:
            mostrar_nivel_completo(nivel, sistemas_particulas)
            rodando = False
        
        # Desenhar / renderizar
        tela.blit(fundo_estrelas, (0, 0))
        
        # Desenhar todos os objetos
        for sprite in todos_sprites:
            tela.blit(sprite.image, sprite.rect)
        
        # Desenhar partículas
        sistemas_particulas.draw(tela)
        
        # Desenhar HUD
        desenhar_barra_vida(tela, 20, 20, jogador.vidas * 33.3)
        mostrar_texto(tela, f"Vidas: {jogador.vidas}", 24, 70, 40)
        
        mostrar_texto(tela, f"Pontuação: {jogador.pontuacao}", 24, LARGURA // 2, 20)
        mostrar_texto(tela, f"Nível: {nivel}", 24, LARGURA - 70, 20)
        
        # Mostrar power-up ativo
        if jogador.powerup_ativo:
            tempo_restante = max(0, (jogador.powerup_tempo - pygame.time.get_ticks()) // 1000)
            mostrar_texto(tela, f"Power-up: {tempo_restante}s", 20, LARGURA - 70, 50, VERDE)
        
        # Atualizar tela
        pygame.display.flip()