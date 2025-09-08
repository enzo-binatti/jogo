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
pygame.display.set_caption("Space Dark LED")
relogio = pygame.time.Clock()

# Cores no tema dark LED
PRETO = (0, 0, 0)
CINZA_ESCURO = (10, 10, 20)
AZUL_LED = (0, 150, 255)
ROXO_LED = (180, 0, 255)
VERDE_LED = (0, 255, 150)
VERMELHO_LED = (255, 20, 20)
AMARELO_LED = (255, 255, 0)
CIANO_LED = (0, 255, 255)

# Carregar imagens — versão robusta
def carregar_imagem(nome_arquivo, tamanho=None):
    try:
        if not os.path.exists(nome_arquivo):
            print(f"⚠️ Arquivo não encontrado: {nome_arquivo} — usando fallback")
            superficie = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.circle(superficie, (255, 0, 0), (32, 32), 32)  # Indica erro
            if tamanho:
                superficie = pygame.transform.scale(superficie, tamanho)
            return superficie

        imagem = pygame.image.load(nome_arquivo).convert_alpha()
        if tamanho:
            imagem = pygame.transform.scale(imagem, tamanho)
        print(f"🖼️ {nome_arquivo} carregado com sucesso!")
        return imagem

    except Exception as e:
        print(f"❌ Erro ao carregar {nome_arquivo}: {e}")
        superficie = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.circle(superficie, (255, 0, 0), (32, 32), 32)
        if tamanho:
            superficie = pygame.transform.scale(superficie, tamanho)
        return superficie

# Verificar arquivos no início
print("🔍 Verificando arquivos...")
for arquivo in ["vida.png", "X 3.png", "nave.png", "inimigo 1.png", "inimigo 2.png", "inimigo 3.png"]:
    if os.path.exists(arquivo):
        print(f"✅ {arquivo} encontrado!")
    else:
        print(f"❌ {arquivo} NÃO encontrado!")

# Carregar sprites das imagens
nave_img = carregar_imagem("nave.png", (100, 100))
inimigo1_img = carregar_imagem("inimigo 1.png", (70, 70))
inimigo2_img = carregar_imagem("inimigo 2.png", (70, 70))
inimigo3_img = carregar_imagem("inimigo 3.png", (70, 70))

# Carregar power-ups — usando os nomes REAIS que você enviou
vida_img = carregar_imagem("vida.png", (60, 60))        # Coração
arma_img = carregar_imagem("X 3.png", (60, 60))        # "X 3" — note o espaço!

# Fallback manual se o carregamento falhou (verificado pelo círculo vermelho)
if vida_img.get_size() == (64, 64) and vida_img.get_at((32,32)) == (255,0,0,255):
    print("🛠️ Gerando fallback para vida.png")
    vida_img = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(vida_img, (255, 0, 0), (16, 12), 8)
    pygame.draw.circle(vida_img, (255, 0, 0), (24, 12), 8)
    pygame.draw.polygon(vida_img, (255, 0, 0), [(16, 28), (8, 12), (24, 12)])

if arma_img.get_size() == (64, 64) and arma_img.get_at((32,32)) == (255,0,0,255):
    print("🛠️ Gerando fallback para X 3.png")
    arma_img = pygame.Surface((32, 32), pygame.SRCALPHA)
    fonte = pygame.font.SysFont("Arial", 20, bold=True)
    texto = fonte.render("x3", True, (255, 255, 0))
    arma_img.blit(texto, (5, 5))

powerup_imgs = {
    'vida': vida_img,
    'arma': arma_img
}

# Gerar outros sprites com tema LED
def gerar_sprite_tiro_led():
    superficie = pygame.Surface((10, 24), pygame.SRCALPHA)
    
    # Tiro com gradiente mais realista
    for i in range(24):
        alpha = 200 - (i * 8)
        if alpha < 0: alpha = 0
        cor = (0, 150, 255, alpha)
        pygame.draw.rect(superficie, cor, (3, i, 4, 1))
    
    # Contorno mais suave
    pygame.draw.rect(superficie, (0, 100, 200), (2, 4, 6, 16), 1)
    
    # Luz interna
    pygame.draw.rect(superficie, (0, 100, 255, 100), (3, 4, 4, 16))
    
    return superficie

def gerar_fundo_estrelas_led():
    superficie = pygame.Surface((LARGURA, ALTURA))
    superficie.fill(CINZA_ESCURO)
    
    # Estrelas mais realistas (pontos brancos com variação de tamanho)
    for i in range(200):
        x = random.randint(0, LARGURA - 1)
        y = random.randint(0, ALTURA - 1)
        tamanho = random.randint(1, 2)
        brilho = random.randint(150, 255)
        pygame.draw.circle(superficie, (brilho, brilho, brilho), (x, y), tamanho)
    
    # Algumas estrelas coloridas (menos que antes)
    for i in range(10):
        x = random.randint(0, LARGURA - 1)
        y = random.randint(0, ALTURA - 1)
        tamanho = random.randint(2, 3)
        cor = random.choice([AZUL_LED, ROXO_LED])
        pygame.draw.circle(superficie, cor, (x, y), tamanho)
    
    # Nebulosa sutil
    for i in range(5):
        x = random.randint(0, LARGURA)
        y = random.randint(0, ALTURA)
        raio = random.randint(50, 150)
        cor = random.choice([(30, 30, 50), (40, 20, 60), (20, 40, 60)])
        for r in range(raio, 0, -5):
            alpha = 10 - (r/raio * 10)
            if alpha > 0:
                s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*cor, alpha), (r, r), r)
                superficie.blit(s, (x-r, y-r))
    
    return superficie

# Carregar sprites LED restantes
tiro_img = gerar_sprite_tiro_led()
fundo_estrelas = gerar_fundo_estrelas_led()

# Efeitos de partículas LED
class ParticulaLED:
    def __init__(self, x, y, cor, velocidade=1, tamanho=2, vida=30, trail=False):
        self.x = x
        self.y = y
        self.cor = cor
        self.velocidade = velocidade
        self.tamanho = tamanho
        self.vida = vida
        self.vida_max = vida
        self.trail = trail
        self.trail_points = []
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * random.uniform(0.5, 2) * velocidade
        self.vy = math.sin(angle) * random.uniform(0.5, 2) * velocidade
    
    def update(self):
        if self.trail and len(self.trail_points) < 5:
            self.trail_points.append((self.x, self.y))
        
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1
        
        # Reduzir tamanho ao longo da vida
        self.tamanho = max(0.5, self.tamanho * (self.vida / self.vida_max))
        return self.vida <= 0
    
    def draw(self, surface):
        alpha = 255 * (self.vida / self.vida_max)
        
        # Desenhar trilha se aplicável
        if self.trail and len(self.trail_points) > 1:
            for i in range(1, len(self.trail_points)):
                pos_prev = self.trail_points[i-1]
                pos = self.trail_points[i]
                trail_alpha = alpha * (i / len(self.trail_points))
                pygame.draw.line(surface, (*self.cor, trail_alpha), 
                                pos_prev, pos, max(1, int(self.tamanho/2)))
        
        # Desenhar partícula principal
        s = pygame.Surface((self.tamanho*2, self.tamanho*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.cor, alpha), (self.tamanho, self.tamanho), self.tamanho)
        
        # Efeito de brilho LED
        if self.tamanho > 1.5:
            pygame.draw.circle(s, (255, 255, 255, alpha/2), 
                              (self.tamanho, self.tamanho), self.tamanho/2)
        
        surface.blit(s, (int(self.x - self.tamanho), int(self.y - self.tamanho)))

class SistemaParticulasLED:
    def __init__(self):
        self.particulas = []
    
    def add_particulas(self, x, y, cor, count=10, velocidade=1, tamanho=2, vida=30, trail=False):
        for _ in range(count):
            self.particulas.append(ParticulaLED(x, y, cor, velocidade, tamanho, vida, trail))
    
    def update(self):
        for particula in self.particulas[:]:
            if particula.update():
                self.particulas.remove(particula)
    
    def draw(self, surface):
        for particula in self.particulas:
            particula.draw(surface)

# Configurações de dificuldade por fase (VERSÃO MAIS FÁCIL)
CONFIG_FASES = [
    # Fase 1: Muito fácil - apenas inimigos básicos lentos
    {"inimigos_por_nivel": 4, "velocidade_inimigos": 0.8, "inimigo_tipo": 0, "powerup_chance": 0.7},
    
    # Fase 2: Fácil - alguns inimigos básicos
    {"inimigos_por_nivel": 5, "velocidade_inimigos": 0.9, "inimigo_tipo": 0.1, "powerup_chance": 0.6},
    
    # Fase 3: Moderadamente fácil - mistura de básicos e alguns intermediários
    {"inimigos_por_nivel": 6, "velocidade_inimigos": 1.0, "inimigo_tipo": 0.2, "powerup_chance": 0.5},
    
    # Fase 4: Moderada - mais inimigos intermediários
    {"inimigos_por_nivel": 7, "velocidade_inimigos": 1.1, "inimigo_tipo": 0.3, "powerup_chance": 0.5},
    
    # Fase 5: Moderada - mistura equilibrada
    {"inimigos_por_nivel": 8, "velocidade_inimigos": 1.2, "inimigo_tipo": 0.4, "powerup_chance": 0.4},
    
    # Fase 6: Moderadamente difícil - mais inimigos intermediários
    {"inimigos_por_nivel": 9, "velocidade_inimigos": 1.3, "inimigo_tipo": 0.5, "powerup_chance": 0.4},
    
    # Fase 7: Difícil - aparecem inimigos avançados
    {"inimigos_por_nivel": 10, "velocidade_inimigos": 1.4, "inimigo_tipo": 0.6, "powerup_chance": 0.3},
    
    # Fase 8: Muito difícil - muitos inimigos avançados
    {"inimigos_por_nivel": 12, "velocidade_inimigos": 1.5, "inimigo_tipo": 0.7, "powerup_chance": 0.3},
    
    # Fase 9: Extremamente difícil - desafio máximo
    {"inimigos_por_nivel": 14, "velocidade_inimigos": 1.6, "inimigo_tipo": 0.8, "powerup_chance": 0.2},
    
    # Fase 10: Boss final - fase especial
    {"inimigos_por_nivel": 20, "velocidade_inimigos": 1.7, "inimigo_tipo": 0.9, "powerup_chance": 0.7, "boss": True}
]

# Classes do jogo com tema LED
class JogadorLED:
    def __init__(self, todos_sprites, sistemas_particulas):
        self.image = nave_img
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA // 2
        self.rect.bottom = ALTURA - 50
        self.velocidade = 8
        self.vidas = 5  # Mais vidas para facilitar
        self.pontuacao = 0
        self.powerup_tempo = 0
        self.powerup_ativo = False
        self.ultimo_tiro = pygame.time.get_ticks()
        self.tempo_recarga = 250
        self.todos_sprites = todos_sprites
        self.sistemas_particulas = sistemas_particulas
        self.invulneravel = False
        self.invulneravel_tempo = 0
        self.efeito_led_timer = 0
    
    def update(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
            # Partículas do propulsor esquerdo
            self.sistemas_particulas.add_particulas(
                self.rect.centerx + 15, self.rect.bottom, 
                (255, 100, 0), 2, 2, 3, 15, True
            )
        if teclas[pygame.K_RIGHT] and self.rect.right < LARGURA:
            self.rect.x += self.velocidade
            # Partículas do propulsor direito
            self.sistemas_particulas.add_particulas(
                self.rect.centerx - 15, self.rect.bottom, 
                (255, 100, 0), 2, 2, 3, 15, True
            )
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidade
            # Partículas do propulsor principal
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.bottom, 
                (255, 150, 0), 3, 3, 4, 20, True
            )
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTURA:
            self.rect.y += self.velocidade
            # Partículas do propulsor traseiro
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.top, 
                (200, 200, 200), 2, 1, 2, 10, True
            )
            
        # Partículas contínuas dos propulsores
        self.sistemas_particulas.add_particulas(
            self.rect.centerx + 15, self.rect.bottom, 
            (255, 100, 0), 1, 2, 2, 10, True
        )
        self.sistemas_particulas.add_particulas(
            self.rect.centerx - 15, self.rect.bottom, 
            (255, 100, 0), 1, 2, 2, 10, True
        )
            
        if self.powerup_ativo and pygame.time.get_ticks() > self.powerup_tempo:
            self.powerup_ativo = False
            self.tempo_recarga = 250
            
        # Gerenciar invulnerabilidade
        if self.invulneravel:
            if pygame.time.get_ticks() > self.invulneravel_tempo:
                self.invulneravel = False
            # Efeito LED piscante quando invulnerável
            self.efeito_led_timer += 1
            if self.efeito_led_timer % 10 < 5:
                # Adicionar partículas de efeito LED
                self.sistemas_particulas.add_particulas(
                    self.rect.centerx, self.rect.centery,
                    CIANO_LED, 3, 1, 2, 15
                )
        else:
            self.efeito_led_timer = 0

    def atirar(self, tiros):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.tempo_recarga:
            self.ultimo_tiro = agora
            tiros.append(TiroLED(self.rect.centerx, self.rect.top, 0, self.todos_sprites, self.sistemas_particulas))
            
            # Efeito de partículas LED ao atirar
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.top, 
                CIANO_LED, 5, 3, 2, 15, True
            )
            
            if self.powerup_ativo:
                tiros.append(TiroLED(self.rect.centerx, self.rect.top, -1, self.todos_sprites, self.sistemas_particulas))
                tiros.append(TiroLED(self.rect.centerx, self.rect.top, 1, self.todos_sprites, self.sistemas_particulas))

    def powerup(self):
        self.powerup_ativo = True
        self.powerup_tempo = pygame.time.get_ticks() + 5000
        self.tempo_recarga = 100
        
        # Efeito visual LED de power-up
        for _ in range(20):
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.centery,
                VERDE_LED, 1, 2, 4, 30, True
            )

    def tomar_dano(self):
        if not self.invulneravel:
            self.vidas -= 1
            self.invulneravel = True
            self.invulneravel_tempo = pygame.time.get_ticks() + 2000
            
            # Efeito de partículas LED ao tomar dano
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.centery,
                VERMELHO_LED, 20, 3, 4, 40, True
            )
            
            return self.vidas <= 0
        return False

class InimigoLED:
    def __init__(self, nivel, config_fase, todos_sprites, sistemas_particulas):
        # Escolher tipo de inimigo baseado na configuração da fase
        tipo_aleatorio = random.random()
        
        if tipo_aleatorio < 0.33:  # Inimigo tipo 1 (básico)
            self.image = inimigo1_img
            self.tipo = 1
            self.vida = 1
            self.pontos = 100
            self.cor_led = VERMELHO_LED
            self.raio_visao = 200
            self.velocidade_base = 1.0
        elif tipo_aleatorio < 0.66:  # Inimigo tipo 2 (intermediário)
            self.image = inimigo2_img
            self.tipo = 2
            self.vida = 2
            self.pontos = 200
            self.cor_led = AZUL_LED
            self.raio_visao = 250
            self.velocidade_base = 1.2
        else:  # Inimigo tipo 3 (avançado)
            self.image = inimigo3_img
            self.tipo = 3
            self.vida = 3
            self.pontos = 300
            self.cor_led = ROXO_LED
            self.raio_visao = 300
            self.velocidade_base = 1.5
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(LARGURA - self.rect.width)
        self.rect.y = random.randrange(-150, -50)
        self.speedy = random.randrange(1, 3) * config_fase["velocidade_inimigos"] * self.velocidade_base
        self.speedx = random.randrange(-2, 2) * config_fase["velocidade_inimigos"] * self.velocidade_base
        self.nivel = nivel
        self.todos_sprites = todos_sprites
        self.sistemas_particulas = sistemas_particulas
        self.particula_timer = 0
        self.tiro_timer = 0
        self.tempo_recarga_tiro = 60  # Frames entre tiros

    def update(self, jogador_x, jogador_y):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        # Partículas de propulsão LED
        self.particula_timer += 1
        if self.particula_timer >= 5:
            self.particula_timer = 0
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.bottom,
                self.cor_led, 1, 1, 2, 20, True
            )
        
        # IA diferente para cada tipo de inimigo
        dx = jogador_x - self.rect.centerx
        dy = jogador_y - self.rect.centery
        distancia = math.sqrt(dx*dx + dy*dy)
        
        # Comportamento baseado no tipo de inimigo
        if self.tipo == 1:  # Inimigo básico - movimento simples
            if distancia < self.raio_visao:
                fator = 0.03
                self.rect.x += dx * fator
                self.rect.y += dy * fator
                
        elif self.tipo == 2:  # Inimigo intermediário - movimento em zigue-zague
            if distancia < self.raio_visao:
                fator = 0.04
                self.rect.x += dx * fator + math.sin(pygame.time.get_ticks() * 0.001) * 2
                self.rect.y += dy * fator
                
        elif self.tipo == 3:  # Inimigo avançado - movimento circular e atira
            if distancia < self.raio_visao:
                fator = 0.05
                angulo = math.atan2(dy, dx)
                # Movimento circular ao redor do jogador
                self.rect.x += math.cos(angulo + math.pi/2) * 3 + dx * fator * 0.5
                self.rect.y += math.sin(angulo + math.pi/2) * 3 + dy * fator * 0.5
                
                # Tenta atirar no jogador
                self.tiro_timer += 1
                if self.tiro_timer >= self.tempo_recarga_tiro and distancia < 300:
                    self.tiro_timer = 0
                    # Criar um tiro inimigo
                    return True, (self.rect.centerx, self.rect.centery, angulo)
        
        # Se sair da tela, reaparece em cima
        if self.rect.top > ALTURA + 10 or self.rect.left < -50 or self.rect.right > LARGURA + 50:
            self.rect.x = random.randrange(LARGURA - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3) * self.velocidade_base
        
        return False, None

    def tomar_dano(self, dano=1):
        self.vida -= dano
        
        # Efeito de partículas LED ao tomar dano
        self.sistemas_particulas.add_particulas(
            self.rect.centerx, self.rect.centery,
            self.cor_led, 10, 2, 3, 25, True
        )
        
        return self.vida <= 0

class TiroLED:
    def __init__(self, x, y, direcao, todos_sprites, sistemas_particulas, inimigo=False, angulo=None):
        self.image = tiro_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        self.direcao = direcao
        self.todos_sprites = todos_sprites
        self.sistemas_particulas = sistemas_particulas
        self.particula_timer = 0
        self.inimigo = inimigo
        
        # Para tiros de inimigos com direção específica
        if inimigo and angulo is not None:
            self.vx = math.cos(angulo) * 5
            self.vy = math.sin(angulo) * 5
            self.speedy = 0  # Anula a velocidade padrão
            self.cor_led = ROXO_LED
        else:
            self.vx = direcao * 5
            self.vy = -10
            self.cor_led = CIANO_LED if not inimigo else ROXO_LED

    def update(self):
        if self.inimigo:
            self.rect.x += self.vx
            self.rect.y += self.vy
        else:
            self.rect.y += self.speedy
            self.rect.x += self.direcao * 5
        
        # Partículas de rastro LED
        self.particula_timer += 1
        if self.particula_timer >= 2:
            self.particula_timer = 0
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.bottom,
                self.cor_led, 1, 1, 2, 15, True
            )
        
        # Se sair da tela, marca para remoção
        return self.rect.bottom < 0 or self.rect.top > ALTURA or self.rect.right < 0 or self.rect.left > LARGURA

class PowerUpLED:
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
        self.cor_led = AZUL_LED if tipo == 'arma' else VERMELHO_LED

    def update(self):
        self.rect.y += self.speedy
        
        # Oscilação para efeito visual LED
        self.oscillate += 0.1
        self.rect.x += math.sin(self.oscillate) * 0.5
        
        # Partículas de brilho LED
        if random.random() < 0.1:
            self.sistemas_particulas.add_particulas(
                self.rect.centerx, self.rect.centery,
                self.cor_led, 3, 1, 2, 30, True
            )
        
        return self.rect.top > ALTURA

# Função para mostrar texto com estilo LED
def mostrar_texto_led(surface, texto, tamanho, x, y, cor=AZUL_LED, sombra=True):
    fonte = pygame.font.SysFont("Consolas", tamanho)
    
    if sombra:
        texto_sombra = fonte.render(texto, True, (0, 0, 0))
        sombra_rect = texto_sombra.get_rect()
        sombra_rect.midtop = (x + 2, y + 2)
        surface.blit(texto_sombra, sombra_rect)
    
    texto_surface = fonte.render(texto, True, cor)
    texto_rect = texto_surface.get_rect()
    texto_rect.midtop = (x, y)
    surface.blit(texto_surface, texto_rect)

# Função para desenhar barra de vida com estilo LED
def desenhar_barra_vida_led(surface, x, y, porcentagem, largura=100, altura=12):
    # Fundo escuro
    pygame.draw.rect(surface, (30, 30, 40), (x, y, largura, altura))
    
    # Vida (gradiente LED)
    fill = max(0, (porcentagem / 100) * largura)
    if fill > 0:
        for i in range(int(fill)):
            cor_progresso = i / fill
            r = int(255 * (1 - cor_progresso))
            g = int(255 * cor_progresso)
            b = int(150 * cor_progresso)
            pygame.draw.rect(surface, (r, g, b), (x + i, y, 1, altura))
    
    # Contorno LED
    pygame.draw.rect(surface, AZUL_LED, (x, y, largura, altura), 2)
    
    # Marcadores LED
    for i in range(0, largura, 20):
        pygame.draw.line(surface, (80, 80, 100), (x + i, y), (x + i, y + altura), 1)

# Função para mostrar tela de início com tema LED
def mostrar_tela_inicio_led(sistemas_particulas):
    tela.fill(CINZA_ESCURO)
    tela.blit(fundo_estrelas, (0, 0))
    
    # Adicionar partículas LED para efeito
    for _ in range(5):
        x = random.randint(0, LARGURA)
        y = random.randint(0, ALTURA)
        cor = random.choice([AZUL_LED, ROXO_LED, CIANO_LED])
        sistemas_particulas.add_particulas(x, y, cor, 10, 2, 3, 50, True)
    
    sistemas_particulas.update()
    sistemas_particulas.draw(tela)
    
    # Título com efeito LED
    mostrar_texto_led(tela, "SPACE DARK LED", 72, LARGURA // 2, ALTURA // 4, AZUL_LED)
    mostrar_texto_led(tela, "REALISTIC EDITION", 36, LARGURA // 2, ALTURA // 4 + 70, ROXO_LED)
    
    # Instruções
    mostrar_texto_led(tela, "Setas para mover, Espaço para atirar", 28, LARGURA // 2, ALTURA // 2, CIANO_LED)
    mostrar_texto_led(tela, "Colete power-ups para melhorar sua nave", 24, LARGURA // 2, ALTURA // 2 + 40, VERDE_LED)
    mostrar_texto_led(tela, "Pressione qualquer tecla para começar", 22, LARGURA // 2, ALTURA * 3/4, AMARELO_LED)
    
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

# Função para mostrar tela de game over com estilo LED
def mostrar_game_over_led(pontuacao, nivel, sistemas_particulas):
    tela.fill(CINZA_ESCURO)
    tela.blit(fundo_estrelas, (0, 0))
    
    # Adicionar partículas LED para efeito
    for _ in range(10):
        x = random.randint(0, LARGURA)
        y = random.randint(0, ALTURA)
        sistemas_particulas.add_particulas(x, y, VERMELHO_LED, 15, 2, 4, 60, True)
    
    sistemas_particulas.update()
    sistemas_particulas.draw(tela)
    
    mostrar_texto_led(tela, "GAME OVER", 80, LARGURA // 2, ALTURA // 4, VERMELHO_LED)
    mostrar_texto_led(tela, f"Pontuação: {pontuacao}", 40, LARGURA // 2, ALTURA // 2 - 30, CIANO_LED)
    mostrar_texto_led(tela, f"Nível alcançado: {nivel}", 40, LARGURA // 2, ALTURA // 2 + 20, AZUL_LED)
    mostrar_texto_led(tela, "Pressione qualquer tecla para jogar novamente", 24, LARGURA // 2, ALTURA * 3/4, AMARELO_LED)
    
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

# Função para mostrar tela de nível completo com LED
def mostrar_nivel_completo_led(nivel, sistemas_particulas):
    tela.fill(CINZA_ESCURO)
    tela.blit(fundo_estrelas, (0, 0))
    
    # Adicionar partículas LED para efeito
    for _ in range(15):
        x = random.randint(0, LARGURA)
        y = random.randint(0, ALTURA)
        cor = random.choice([VERDE_LED, AZUL_LED, CIANO_LED])
        sistemas_particulas.add_particulas(x, y, cor, 20, 2, 4, 70, True)
    
    sistemas_particulas.update()
    sistemas_particulas.draw(tela)
    
    mostrar_texto_led(tela, "NÍVEL COMPLETO!", 64, LARGURA // 2, ALTURA // 3, VERDE_LED)
    mostrar_texto_led(tela, f"Fase {nivel + 1} concluída!", 48, LARGURA // 2, ALTURA // 2, AZUL_LED)
    
    if nivel < len(CONFIG_FASES) - 1:
        mostrar_texto_led(tela, f"Próxima fase: {nivel + 2}", 36, LARGURA // 2, ALTURA // 2 + 50, CIANO_LED)
    else:
        mostrar_texto_led(tela, "Parabéns! Você completou todas as fases!", 36, LARGURA // 2, ALTURA // 2 + 50, AMARELO_LED)
    
    pygame.display.flip()
    pygame.time.delay(2500)

# Inicialização do jogo
print("🚀 Iniciando Space Dark LED...")
sistemas_particulas = SistemaParticulasLED()

# Mostrar tela de início
mostrar_tela_inicio_led(sistemas_particulas)

# Loop principal do jogo
game_over = False
executando = True
nivel = 0  # Começa na fase 1 (índice 0)
total_fases = len(CONFIG_FASES)

while executando:
    if game_over:
        mostrar_game_over_led(jogador.pontuacao, nivel, sistemas_particulas)
        game_over = False
        nivel = 0  # Reinicia na fase 1
    
    # Obter configuração da fase atual
    config_fase = CONFIG_FASES[min(nivel, len(CONFIG_FASES) - 1)]
    
    # Inicializar listas de objetos
    todos_sprites = []
    inimigos = []
    tiros = []
    tiros_inimigos = []
    powerups = []
    
    # Criar jogador
    jogador = JogadorLED(todos_sprites, sistemas_particulas)
    todos_sprites.append(jogador)
    
    # Criar inimigos baseado na configuração da fase
    for i in range(config_fase["inimigos_por_nivel"]):
        inimigo = InimigoLED(nivel, config_fase, todos_sprites, sistemas_particulas)
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
            atirou, tiro_info = inimigo.update(jogador.rect.centerx, jogador.rect.centery)
            
            # Se o inimigo atirou, criar um tiro
            if atirou and tiro_info:
                x, y, angulo = tiro_info
                tiro = TiroLED(x, y, 0, todos_sprites, sistemas_particulas, inimigo=True, angulo=angulo)
                tiros_inimigos.append(tiro)
                todos_sprites.append(tiro)
            
            # Verificar colisão com jogador
            if jogador.rect.colliderect(inimigo.rect):
                if jogador.tomar_dano():
                    game_over = True
                    rodando = False
        
        # Atualizar tiros do jogador
        for tiro in tiros[:]:
            if tiro.update():  # Se retornar True, saiu da tela
                tiros.remove(tiro)
                if tiro in todos_sprites:
                    todos_sprites.remove(tiro)
                continue
                
            # Verificar colisão com inimigos
            for inimigo in inimigos[:]:
                if tiro.rect.colliderect(inimigo.rect):
                    if inimigo.tomar_dano():  # Se retornar True, inimigo morreu
                        jogador.pontuacao += inimigo.pontos
                        inimigos.remove(inimigo)
                        if inimigo in todos_sprites:
                            todos_sprites.remove(inimigo)
                        
                        # Efeito de explosão LED
                        sistemas_particulas.add_particulas(
                            inimigo.rect.centerx, inimigo.rect.centery,
                            inimigo.cor_led, 30, 3, 5, 50, True
                        )
                        
                        # Chance de dropar power-up baseada na configuração da fase
                        if random.random() > config_fase["powerup_chance"]:
                            tipo = random.choice(['vida', 'arma'])
                            powerup = PowerUpLED(inimigo.rect.centerx, inimigo.rect.centery, 
                                            tipo, todos_sprites, sistemas_particulas)
                            powerups.append(powerup)
                            todos_sprites.append(powerup)
                    
                    if tiro in tiros:
                        tiros.remove(tiro)
                        if tiro in todos_sprites:
                            todos_sprites.remove(tiro)
                    break
        
        # Atualizar tiros dos inimigos
        for tiro in tiros_inimigos[:]:
            if tiro.update():  # Se retornar True, saiu da tela
                tiros_inimigos.remove(tiro)
                if tiro in todos_sprites:
                    todos_sprites.remove(tiro)
                continue
                
            # Verificar colisão com jogador
            if tiro.rect.colliderect(jogador.rect):
                if jogador.tomar_dano():
                    game_over = True
                    rodando = False
                
                tiros_inimigos.remove(tiro)
                if tiro in todos_sprites:
                    todos_sprites.remove(tiro)
                
                # Efeito de colisão LED
                sistemas_particulas.add_particulas(
                    tiro.rect.centerx, tiro.rect.centery,
                    ROXO_LED, 15, 2, 3, 30, True
                )
        
        # Atualizar power-ups
        poder_spawn_timer += 1
        if poder_spawn_timer >= 900:  # 15 segundos em 60 FPS
            poder_spawn_timer = 0
            tipo = random.choice(['vida', 'arma'])
            powerup = PowerUpLED(random.randint(50, LARGURA-50), -30, 
                            tipo, todos_sprites, sistemas_particulas)
            powerups.append(powerup)
            todos_sprites.append(powerup)
            
        for powerup in powerups[:]:
            if powerup.update():  # Se saiu da tela
                powerups.remove(powerup)
                if powerup in todos_sprites:
                    todos_sprites.remove(powerup)
                continue
                
            # Verificar colisão com jogador
            if jogador.rect.colliderect(powerup.rect):
                if powerup.type == 'vida':
                    jogador.vidas += 1
                elif powerup.type == 'arma':
                    jogador.powerup()
                
                # Efeito de coleta LED
                sistemas_particulas.add_particulas(
                    powerup.rect.centerx, powerup.rect.centery,
                    powerup.cor_led, 20, 2, 4, 40, True
                )
                
                powerups.remove(powerup)
                if powerup in todos_sprites:
                    todos_sprites.remove(powerup)
        
        # Verificar se nível completo
        if len(inimigos) == 0:
            mostrar_nivel_completo_led(nivel, sistemas_particulas)
            rodando = False
        
        # Desenhar / renderizar
        tela.blit(fundo_estrelas, (0, 0))
        
        # Desenhar todos os objetos
        for sprite in todos_sprites:
            tela.blit(sprite.image, sprite.rect)
        
        # Desenhar partículas
        sistemas_particulas.draw(tela)
        
        # Desenhar HUD com tema LED
        desenhar_barra_vida_led(tela, 20, 20, jogador.vidas * 20)  # 5 vidas = 100%
        mostrar_texto_led(tela, f"Vidas: {jogador.vidas}", 24, 70, 40, CIANO_LED)
        
        mostrar_texto_led(tela, f"Pontuação: {jogador.pontuacao}", 24, LARGURA // 2, 20, AZUL_LED)
        mostrar_texto_led(tela, f"Fase: {nivel + 1}/{total_fases}", 24, LARGURA - 70, 20, ROXO_LED)
        
        # Mostrar power-up ativo
        if jogador.powerup_ativo:
            tempo_restante = max(0, (jogador.powerup_tempo - pygame.time.get_ticks()) // 1000)
            mostrar_texto_led(tela, f"Power-up: {tempo_restante}s", 20, LARGURA - 70, 50, VERDE_LED)
        
        # Atualizar tela
        pygame.display.flip()
    
    # Avançar para a próxima fase se não foi game over
    if not game_over:
        nivel += 1
        # Se completou todas as fases, volta para a primeira mas mais difícil
        if nivel >= total_fases:
            nivel = total_fases - 1  # Permanece na última fase

pygame.quit()
sys.exit()