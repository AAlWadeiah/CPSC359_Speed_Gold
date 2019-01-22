import pygame, os, random, sys
import explorerhat as hat
from pygame.locals import *

allSprites = pygame.sprite.Group()
coins = pygame.sprite.Group()
bombs = pygame.sprite.Group()

WIDTH = 400
HEIGHT = 700
BLACK = (0,0,0)
WHITE = (255,255,255)

leftLimit = 63
rightLimit = 277

def load_image(filename):
    image = pygame.image.load(os.path.join("data", filename))
    return image.convert_alpha()


class Coin(pygame.sprite.Sprite):
    """Class to represent and control gold coins"""
    def __init__(self, offset):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = load_image('gold_coin.png')
        self.image = self.base_image
        self.area = pygame.display.get_surface().get_rect()
        start_x = self.area.width-offset
        start_y = self.area.height-750
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.yspeed = random.randrange(1, 6)

    def update(self):
        self.rect.move_ip(0, self.yspeed)
        if self.rect.bottom >= 750:
            pygame.sprite.Sprite.kill(self)


class Bomb(pygame.sprite.Sprite):

    def __init__(self, offset):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = load_image('bomb.png')
        self.image = self.base_image
        self.area = pygame.display.get_surface().get_rect()
        start_x = self.area.width-offset
        start_y = self.area.height-750
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.yspeed = random.randrange(1, 6)

    def update(self):
        self.rect.move_ip(0, self.yspeed)
        if self.rect.bottom >= 750:
            pygame.sprite.Sprite.kill(self)


class Car(pygame.sprite.Sprite):
    """Class to represent and control player car"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = load_image('car.png')
        self.image = self.base_image
        self.area = pygame.display.get_surface().get_rect()
        start_x = self.area.width/2
        start_y = self.area.height-20
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.velocity = pygame.math.Vector2()
        self.heading = pygame.math.Vector2(0, -1)

    def update(self):
        key = pygame.key.get_pressed()

        #read keyboard input
        if key[K_LEFT] or hat.analog.one.read() < 2:
            self.rect.move_ip(-5, 0)
        if key[K_RIGHT] or hat.analog.one.read() > 3:
            self.rect.move_ip(5, 0)

        if key[K_UP] or hat.input.one.is_on():
            if self.rect.y >= 330:
                self.velocity = pygame.math.Vector2(0, -25)

        #move car
        if self.rect.y <= 650:
            self.velocity = self.velocity - (self.heading/4)

        self.rect.move_ip(self.velocity.x, self.velocity.y)
        self.rect.clamp_ip(Rect(leftLimit, 350, rightLimit, 350))


def spawn():
    '''Spawns one gold coin and one bomb.'''
    offset = random.randrange(leftLimit+20, rightLimit+20)

    coin = Coin(offset)
    coin.add(allSprites)
    coin.add(coins)

    bomb = Bomb(offset)
    bomb.add(allSprites)
    bomb.add(bombs)

def drawText(surface, text, fontName, size, color, x, y):
    font = pygame.font.SysFont(fontName, size)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.midtop = (x, y)
    surface.blit(textSurface, textRect)

def main():
    """run the game"""
    # initialization and setup
    pygame.init()
    random.seed()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Speed Gold')
    background = load_image('dirt_road.png')
    screen.blit(background, (0, 0))
    score = 0
    gameOver = False

    car = Car()
    car.add(allSprites)

    #game loop
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                return

        # 1% chance to spawn coins and bombs
        if random.randrange(0, 100) < 1:
            spawn()

        allSprites.update()
        if pygame.sprite.spritecollideany(car, bombs):
            car.kill()
            gameOver = True

        if pygame.sprite.spritecollide(car, coins, True):
            score += 1

        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        allSprites.clear(screen, background)
        allSprites.draw(screen)
        drawText(screen, str(score), "monospace", 16, WHITE, WIDTH/2, 10)
        if gameOver:
            drawText(screen, "GAME OVER", "monospace", 30, WHITE, WIDTH/2, HEIGHT/2)
        pygame.display.flip()
        pygame.time.wait(16)


if __name__ == '__main__': main()
pygame.quit()
exit()
