import pygame as pg
import random

pg.init()

WIDTH = 500
HEIGHT = 700

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Jumper')

# game fps
clock = pg.time.Clock()
fps = 60

# scroll
scroll_thresh = 200

# gravitation
gravity = 1

max_platforms = 10

# scroll line
scroll = 0

bg_scroll = 0

white_color = (255, 255, 255)


player_image = pg.image.load('images/playerb5.png').convert_alpha()
bg_image = pg.image.load('images/bgvektor.jpg').convert_alpha()
platform_image = pg.image.load('images/wood111z.png').convert_alpha()


# drawing background
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -300 + bg_scroll))


class Player:
    def __init__(self, x, y):
        # shape, size player
        self.image = pg.transform.scale(player_image, (45, 60))
        self.width = 45
        self.height = 60
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        # change of coordinates
        scroll = 0
        dx = 0
        dy = 0
        # buttons
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            dx = -10
            self.flip = True
        if key[pg.K_d]:
            dx += 10
            self.flip = False

        # gravity vel
        self.vel_y += gravity
        dy += self.vel_y

        # screen window
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > WIDTH:
            dx = WIDTH - self.rect.right

        # collision platform
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        dy = 0
                        self.rect.bottom = platform.rect.top
                        self.vel_y = -20

        # collision floor
        if self.rect.bottom + dy > HEIGHT:
            dy = 0
            self.vel_y = -20

        # if coll plyaer to floor
        if self.rect.top <= scroll_thresh:
            # if jump
            if self.vel_y < 0:
                scroll = -dy

        # new pos
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll


    def draw(self):
        # проверить
        screen.blit(pg.transform.flip(self.image, self.flip, False), (self.rect.x -3, self.rect.y - 1))
        pg.draw.rect(screen, white_color, self.rect, 2)


class Platform(pg.sprite.Sprite):

    def __init__(self, x, y, width):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # update platform pos
    def update(self, scroll):

        self.rect.y += scroll
        # if platform gone to screen
        if self.rect.top > HEIGHT:
            self.kill()



jumper = Player(WIDTH // 2, HEIGHT - 150)

# platform sprite
platform_group = pg.sprite.Group()

# going platform
# for pl in range(max_platforms):
#     p_w = random.randint(40, 60)
#     p_x = random.randint(0, WIDTH - p_w)
#     p_y = pl * random.randint(80, 120)
#     platform = Platform(p_x, p_y, p_w)
#     platform_group.add(platform)

platform = Platform(WIDTH // 2, HEIGHT - 50, 80)
platform_group.add(platform)


run = True
while run:

    clock.tick(fps)

    scroll = jumper.move()


    # draw background
    bg_scroll += scroll
    if bg_scroll >= 600:
        bg_scroll = 0
    draw_bg(bg_scroll)

    # add platforms, size, location
    if len(platform_group) < max_platforms:
        p_w = random.randint(40, 60)
        p_x = random.randint(0, WIDTH - p_w)
        p_y = platform.rect.y - random.randint(80, 120)
        platform = Platform(p_x, p_y, p_w)
        platform_group.add(platform)

    # print(len(platform_group))

    # print(bg_scroll)



    # scroll white line
    pg.draw.line(screen, white_color, (0, scroll_thresh), (WIDTH, scroll_thresh))

    # update platform
    platform_group.update(scroll)

    # draw sprites
    platform_group.draw(screen)
    jumper.draw()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.update()

pg.quit()
