# Bibliotecas
import pgzrun
from random import randint

# Definição do projeto (constantes)
HEIGHT = 720
WIDTH = 1280
TITLE = "Egg Survival"

# Objetos/ Variáveis do menu
state = "menu"  # Estado atual do jogo: "menu" ou "game"
button_play = Rect(
    (WIDTH // 2 - 100, HEIGHT // 2 - 50), (200, 100)
)  # Botão "PLAY" no menu
button_exit = Rect(
    (WIDTH // 2 - 100, HEIGHT // 2 + 100), (200, 100)
)  # Botão "EXIT" no menu
button_sound = Rect((50, 70), (100, 100))  # Botão "SOUND" no menu

# Variável global para controlar o estado da música
musicPlay = True


# Desenha o menu principal
def draw_menu():
    global musicPlay
    screen.draw.text(
        "EGG SURVIVAL", center=(WIDTH // 2, 100), fontsize=60, color="black"
    )
    # Desenha o botão "PLAY"
    screen.draw.filled_rect(button_play, "green")
    screen.draw.text("PLAY", center=button_play.center, fontsize=40, color="black")
    # Desenha o botão "EXIT"
    screen.draw.filled_rect(button_exit, "green")
    screen.draw.text("EXIT", center=button_exit.center, fontsize=40, color="black")
    # Desenha o botão "SOUND" com base no estado da música
    if musicPlay:
        screen.draw.filled_rect(button_sound, "green")
        screen.draw.text(
            "SOUND", center=button_sound.center, fontsize=40, color="black"
        )
    else:
        screen.draw.filled_rect(button_sound, "red")
        screen.draw.text(
            "SOUND", center=button_sound.center, fontsize=40, color="black"
        )


# Função para animar sprites
def animate_frames(obj, sprite_frames, counter):
    if not hasattr(obj, "frame_counter"):
        obj.frame_counter = 0
        obj.current_frame = 0
    # Controla a velocidade da animação (delay entre frames)
    obj.frame_counter += 1
    if obj.frame_counter >= counter:  # Ajuste este valor para mudar a velocidade 8
        obj.frame_counter = 0
        obj.current_frame = (obj.current_frame + 1) % len(sprite_frames)
        obj.sprite.image = sprite_frames[obj.current_frame]


# Classe para o jogador principal
class Player:
    def __init__(self, image, x, y):
        self.sprite = Actor(image)
        self.sprite.x = x
        self.sprite.y = y
        self.vel = 3  # Velocidade de movimento do jogador
        # Variáveis para animação
        self.frame_counter = 0
        self.current_frame = 0
        self.can_shoot = True  # Controla se o jogador pode atirar
        self.facing_left = False  # Rastreia se o jogador está virado para a esquerda
        self.egg_idle = ["egg_idle1", "egg_idle2", "egg_idle3", "egg_idle4"]
        self.egg_run = ["egg_run_0", "egg_run_1"]
        self.egg_run_left = ["egg_run_left_0", "egg_run_left_1"]
        self.egg_idle_left = [
            "egg_idle_left0",
            "egg_idle_left1",
            "egg_idle_left2",
            "egg_idle_left3",
        ]

    def draw(self):
        self.sprite.draw()

    def move(self):
        movx = (keyboard.d - keyboard.a) * self.vel  # Movimento horizontal
        movy = (keyboard.s - keyboard.w) * self.vel  # Movimento vertical
        self.sprite.x += movx
        self.sprite.y += movy
        # Mantém o jogador dentro dos limites da tela (horizontalmente)
        self.sprite.x = max(
            self.sprite.width // 2, min(WIDTH - self.sprite.width // 2, self.sprite.x)
        )
        # Mantém o jogador dentro dos limites da tela (verticalmente)
        self.sprite.y = max(
            self.sprite.height // 2,
            min(HEIGHT - self.sprite.height // 2, self.sprite.y),
        )

        # Atualiza a direção do jogador
        if keyboard.a:
            self.facing_left = True
        elif keyboard.d:
            self.facing_left = False
        # Anima o sprite com base no movimento e direção
        if movx != 0 or movy != 0:
            if self.facing_left:
                animate_frames(self, self.egg_run_left, 8)
            else:
                animate_frames(self, self.egg_run, 8)
        else:
            if self.facing_left:
                animate_frames(self, self.egg_idle_left, 8)
            else:
                animate_frames(self, self.egg_idle, 8)

    def shoot(self):
        if self.can_shoot:
            shootx_dir = keyboard.right - keyboard.left  # Direção do tiro horizontal
            shooty_dir = keyboard.up - keyboard.down  # Direção do tiro vertical

            if shootx_dir > 0:
                bullets.append(
                    Gun(
                        "gema_01",
                        "right",
                        self.sprite.x + self.sprite.width // 2,
                        self.sprite.y,
                    )
                )
                self.can_shoot = False
            elif shootx_dir < 0:
                bullets.append(
                    Gun(
                        "gema_01",
                        "left",
                        self.sprite.x - self.sprite.width // 2,
                        self.sprite.y,
                    )
                )
                self.can_shoot = False
            elif shooty_dir > 0:
                bullets.append(
                    Gun(
                        "gema_01",
                        "up",
                        self.sprite.x,
                        self.sprite.y - self.sprite.height // 2,
                    )
                )
                self.can_shoot = False
            elif shooty_dir < 0:
                bullets.append(
                    Gun(
                        "gema_01",
                        "down",
                        self.sprite.x,
                        self.sprite.y + self.sprite.height // 2,
                    )
                )
                self.can_shoot = False


# Classe para o projétil (gema)
class Gun:
    def __init__(self, image, direction, x, y):
        self.sprite = Actor(image)
        self.sprite.pos = x, y
        self.vel = 5  # Velocidade do projétil
        self.direction = direction  # Direção do movimento do projétil
        play_sound(2)  # Toca o som de tiro

    def draw(self):
        self.sprite.draw()

    def update(self):
        # Atualiza a posição do projétil com base na direção
        if self.direction == "right":
            self.sprite.x += self.vel
        elif self.direction == "left":
            self.sprite.x -= self.vel
        elif self.direction == "up":
            self.sprite.y -= self.vel
        elif self.direction == "down":
            self.sprite.y += self.vel
        # Remove o projétil se sair da tela para otimizar a performance
        if not 0 < self.sprite.x < WIDTH or not 0 < self.sprite.y < HEIGHT:
            return True  # Sinaliza para remover
        return False  # Sinaliza para manter


# Classe para o inimigo
class Enemy:
    def __init__(self, image, x, y):
        self.sprite = Actor(image)
        self.sprite.pos = x, y
        self.vel = 1  # Velocidade de movimento do inimigo
        self.life = 2  # Pontos de vida do inimigo
        self.sprite_animation = ['garfin', 'garfin_1']


    def draw(self):
        self.sprite.draw()

    def move(self, player):
        animate_frames(self, self.sprite_animation, 20)

        # Movimento horizontal em direção ao jogador
        if self.sprite.x > player.sprite.x:
            self.sprite.x -= self.vel
        elif self.sprite.x < player.sprite.x:
            self.sprite.x += self.vel
        # Movimento vertical em direção ao jogador
        if self.sprite.y > player.sprite.y:
            self.sprite.y -= self.vel
        elif self.sprite.y < player.sprite.y:
            self.sprite.y += self.vel

    def take_damage(self):
        self.life -= 1
        if self.life <= 0:
            play_sound(1)  # Toca o som de explosão ao morrer
            return True  # Sinaliza que o inimigo deve ser removido
        return False


# Função para verificar e aplicar dano aos inimigos
def damage_enemy():
    global bullets
    global instancia_enemy
    global score
    bullets_to_remove = []  # Lista de balas que atingiram inimigos
    enemies_hit = []  # Lista de inimigos atingidos neste frame

    for bullet in bullets:
        for enemy in instancia_enemy:
            if bullet.sprite.colliderect(enemy.sprite):
                if (
                    enemy not in enemies_hit
                ):  # Evita múltiplos hits no mesmo inimigo por frame
                    enemy.take_damage()
                    enemies_hit.append(enemy)
                if bullet not in bullets_to_remove:
                    bullets_to_remove.append(bullet)
    # Remove os inimigos que morreram e atualiza a pontuação
    enemies_removed = [enemy for enemy in instancia_enemy if enemy.life <= 0]
    for enemy in enemies_removed:
        instancia_enemy.remove(enemy)
        score += 1  # Incrementa a pontuação ao derrotar um inimigo
    # Cria uma nova lista de balas sem as que colidiram
    new_bullets = [bullet for bullet in bullets if bullet not in bullets_to_remove]
    bullets = new_bullets


# Função para tocar sons de efeito
def play_sound(soundplay):
    global musicPlay
    if musicPlay:
        if soundplay == 1:
            sounds.explosion.play()
            sounds.explosion.set_volume(0.2)
        elif soundplay == 2:
            sounds.lasershoot.play()
            sounds.lasershoot.set_volume(0.2)


# Variáveis globais do jogo
enemy_spawned = False  # Flag para controlar se os inimigos foram gerados
player = None  # Instância da classe Player
bullets = []  # Lista de projéteis ativos
instancia_enemy = []  # Lista de inimigos ativos
enemy_scheduler = None  # Agendador para criar inimigos
score = 0  # Pontuação do jogo


# Função para criar novos inimigos
def create_enemy():
    global instancia_enemy
    en1 = Enemy("garfin", randint(0, 1280), 0)  # Cria um inimigo no topo da tela
    en2 = Enemy(
        "garfin", randint(0, 1280), 720
    )  # Cria um inimigo na parte inferior da tela
    instancia_enemy.append(en1)
    instancia_enemy.append(en2)


# Função para iniciar o jogo
def start_game():
    global state, player, bullets, instancia_enemy
    global enemy_spawned, score, enemy_scheduler
    if musicPlay:
        music.play("cas")
        music.set_volume(0.1)
    score = 0
    state = "game"
    player = Player("egg_front_idle", WIDTH / 2, HEIGHT / 2)  # Cria o jogador
    bullets = []
    instancia_enemy = [
        Enemy("garfin", randint(0, 1280), 0),
        Enemy("garfin", randint(0, 1280), 720),
    ]  # Cria os inimigos iniciais
    enemy_spawned = False
    if enemy_scheduler is not None:
        clock.unschedule(create_enemy)  # Cancela qualquer agendamento anterior
    enemy_scheduler = clock.schedule_interval(
        create_enemy, 2
    )  # Agenda a criação de inimigos


# Função de desenho principal
def draw():
    screen.clear()
    if state == "menu":
        screen.blit("menu_background", (0, 0))
        draw_menu()
    elif state == "game":
        screen.blit("background_01", (0, 0))
        player.draw()
        for enemy in instancia_enemy:
            enemy.draw()
        for bullet in bullets:
            bullet.draw()
        screen.draw.text(f"Score: {score}", (10, 10), color="white", fontsize=30)
    elif state == "game_over":
        screen.fill("red")
        screen.draw.text(
            "GAME OVER",
            center=(WIDTH // 2, HEIGHT // 2 - 50),
            fontsize=80,
            color="white",
        )
        screen.draw.text(
            "Clique para reiniciar",
            center=(WIDTH // 2, HEIGHT // 2 + 50),
            fontsize=40,
            color="white",
        )
        screen.draw.text(
            f"Score: {score}",
            center=(WIDTH // 2, HEIGHT // 2 + 150),
            fontsize=40,
            color="white",
        )


# Função de atualização principal (chamada a cada frame)
def update():
    global state, bullets, enemy_spawned, player, instancia_enemy, score
    if state == "game":
        player.move()
        for enemy in instancia_enemy:
            enemy.move(player)
            if player.sprite.colliderect(enemy.sprite):
                state = "game_over"  # Transiciona para o estado de "game over"
        # Atualiza e remove projéteis que saíram da tela
        new_bullets = []
        for bullet in bullets:
            if not bullet.update():
                new_bullets.append(bullet)
        bullets = new_bullets
        damage_enemy()  # Verifica se os projéteis atingiram os inimigos

        # Agenda a criação contínua de inimigos
        if not enemy_spawned:
            enemy_spawned = True
        # Permite que o jogador atire novamente após um certo tempo (ou quando nenhuma tecla de direção de tiro está pressionada)
        if not (keyboard.right or keyboard.left or keyboard.up or keyboard.down):
            player.can_shoot = True
    elif state == "game_over":
        if enemy_scheduler is not None:
            clock.unschedule(create_enemy)  # Cancela a criação de inimigos no game over


# Função chamada quando uma tecla é pressionada
def on_key_down(key):
    global state
    if state == "game":
        player.shoot()


# Função chamada quando um botão do mouse é pressionado
def on_mouse_down(pos):
    global state, musicPlay
    if state == "menu":
        if button_play.collidepoint(pos):
            start_game()
        if button_sound.collidepoint(pos):
            musicPlay = not musicPlay
            print(musicPlay)
        if button_exit.collidepoint(pos):
            exit()
    elif state == "game_over":
        start_game()  # Reinicia o jogo ao clicar na tela de game over


pgzrun.go()
