import pygame
import sys

# ---------------- INIT ----------------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mini Mario")

clock = pygame.time.Clock()
FPS = 60

# ---------------- COLORS ----------------
SKY = (100, 180, 255)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)

# ---------------- LOAD ASSETS ----------------
mario_img = pygame.transform.scale(
    pygame.image.load("assets/mario.png"), (40, 50)
)
goomba_img = pygame.transform.scale(
    pygame.image.load("assets/goomba.png"), (40, 40)
)
coin_img = pygame.transform.scale(
    pygame.image.load("assets/coin.png"), (25, 25)
)

jump_sound = pygame.mixer.Sound("assets/jump.wav")
coin_sound = pygame.mixer.Sound("assets/coin.wav")
stomp_sound = pygame.mixer.Sound("assets/stomp.wav")

font = pygame.font.SysFont("Arial", 22)

# ---------------- CLASSES ----------------
class Player:
    def __init__(self):
        self.rect = pygame.Rect(50, 300, 40, 50)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -14
        self.gravity = 0.8
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            jump_sound.play()
            self.on_ground = False

        self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p) and self.vel_y > 0:
                self.rect.bottom = p.top
                self.vel_y = 0
                self.on_ground = True

    def draw(self):
        screen.blit(mario_img, self.rect)


class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.direction = 1
        self.speed = 2

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1

    def draw(self):
        screen.blit(goomba_img, self.rect)


# ---------------- LEVELS ----------------
levels = [
    {
        "platforms": [
            pygame.Rect(0, 400, WIDTH, 50),
            pygame.Rect(300, 300, 120, 20),
            pygame.Rect(520, 240, 120, 20),
        ],
        "coins": [
            pygame.Rect(330, 260, 25, 25),
            pygame.Rect(560, 200, 25, 25),
        ],
        "enemies": [
            Enemy(450, 360),
        ],
    },
    {
        "platforms": [
            pygame.Rect(0, 400, WIDTH, 50),
            pygame.Rect(200, 320, 120, 20),
            pygame.Rect(420, 260, 120, 20),
            pygame.Rect(650, 200, 120, 20),
        ],
        "coins": [
            pygame.Rect(230, 280, 25, 25),
            pygame.Rect(450, 220, 25, 25),
            pygame.Rect(680, 160, 25, 25),
        ],
        "enemies": [
            Enemy(350, 360),
            Enemy(600, 360),
        ],
    },
]

# ---------------- GAME STATE ----------------
player = Player()
level_index = 0
score = 0
lives = 3

# ---------------- GAME LOOP ----------------
while True:
    clock.tick(FPS)
    screen.fill(SKY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    level = levels[level_index]

    # UPDATE
    player.update(level["platforms"])

    for enemy in level["enemies"][:]:
        enemy.update()

        if player.rect.colliderect(enemy.rect):
            if player.vel_y > 0:
                level["enemies"].remove(enemy)
                stomp_sound.play()
                player.vel_y = -7
                score += 20
            else:
                lives -= 1
                player.rect.x, player.rect.y = 50, 300
                player.vel_y = 0

    for coin in level["coins"][:]:
        if player.rect.colliderect(coin):
            level["coins"].remove(coin)
            coin_sound.play()
            score += 10

    # LEVEL COMPLETE
    if len(level["coins"]) == 0:
        level_index += 1
        if level_index >= len(levels):
            print("YOU WIN!")
            pygame.quit()
            sys.exit()
        player.rect.x, player.rect.y = 50, 300

    if lives <= 0:
        print("GAME OVER")
        pygame.quit()
        sys.exit()

    # DRAW
    for p in level["platforms"]:
        pygame.draw.rect(screen, GREEN, p)

    for coin in level["coins"]:
        screen.blit(coin_img, coin)

    for enemy in level["enemies"]:
        enemy.draw()

    player.draw()

    hud = font.render(
        f"Score: {score}   Lives: {lives}   Level: {level_index + 1}",
        True,
        WHITE,
    )
    screen.blit(hud, (20, 10))

    pygame.display.update()
