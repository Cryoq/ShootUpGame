from Constants import *
import sys
from abc import ABC, abstractmethod

class Hearts:
    def __init__(self) -> None:
        self.img = "3hearts.png"
        self.setHeartSprite()
        
    def deleteHeart(self):
        imageList = list(self.img)
        number = self.img[0]
        imageList[0] = str(number-1)
        self.image = ''.join(imageList)
        
    def addHeart(self):
        imageList = list(self.img)
        number = self.image[0]
        imageList[0] = str(number+1)
        self.image = ''.join(imageList)
        
    def setHeartSprite(self):
        self.image = pygame.image.load(f"sprites/{self.img}")
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.image = pygame.transform.smoothscale(self.image, (150,150))

# Basic movement for sprites
class Movement(pygame.sprite.Sprite, ABC):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = WIDTH/2
        self.y = HEIGHT/2
    
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,coord):
        self._x = coord if coord > 0 and coord < WIDTH  else self._x
        
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, coord):
        self._y = coord if coord > 0 and coord < HEIGHT else self._y

    def moveLeft(self,dec):
        self.x -= dec
        
    def moveRight(self, inc):
        self.x += inc
    
    def moveUp(self,dec):
        self.y -= dec
        
    def moveDown(self, inc):
        self.y += inc
        
    def getPosition(self):
        return self.x, self.y
    
    @abstractmethod
    def update(self):
        raise NotImplementedError("You need an update function")

class Wizard(Movement):
    def __init__(self) -> None:
        self.image = pygame.image.load("sprites/wiz.png").convert()
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.image = pygame.transform.scale(self.image, (200,200))
        Movement.__init__(self)
        self.y = HEIGHT - self.image.get_size()[1]
        self.movingLeft = True
        self.movingRight = False
        self.buffer = 0
        self.speed = 2   
        
    def update(self, keyspressed: dict):
        if keyspressed[K_RIGHT]:
            self.moveRight(self.speed)
            if self.movingLeft == True:
                self.image = pygame.transform.flip(self.image, True, False)
                self.movingLeft, self.movingRight = False, True
    
        if keyspressed[K_LEFT]:
            self.moveLeft(self.speed)
            if self.movingRight == True:
                self.image = pygame.transform.flip(self.image, True, False)
                self.movingRight, self.movingLeft = False, True
        
        if keyspressed[K_SPACE]:
            if self.buffer == 0:
                x,y = self.getPosition()
                if self.movingRight:
                    x += self.image.get_size()[0]
                for i in range(50):
                    bullet = Bullet((x,y-i))
                    bullets.add(bullet)
                self.buffer = 150
            
        
        self.buffer = self.buffer - 1 if self.buffer != 0 else self.buffer
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self,coord):
        self._x = coord if coord > 0 and coord < WIDTH - self.image.get_size()[0] else self._x

class Spider(Movement):
    def __init__(self,coord) -> None:
        Movement.__init__(self)
        self.y = randint(0,HEIGHT/2)
        self.image = pygame.image.load("sprites/spider1.png")
        self.image.set_colorkey((0,0,0),RLEACCEL)
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = ((coord))
        self.buffer = 10
        self.iterator = 0
        
    def update(self):
        if self.rect.center[0] <= WIDTH:
            self.rect.move_ip(1,0)
        else:
            global lives
            lives -= 1
            self.kill()
    
    def getSize(self):
        return self.image.get_size()

class Bullet(Movement):
    def __init__(self,otherSurf) -> None:
        Movement.__init__(self)
        self.image = pygame.image.load("sprites/Bullet.png").convert()
        self.image = pygame.transform.scale(self.image, (25,25))
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (otherSurf)
        
    def update(self):
        if self.rect.center[1] >= 0:
            self.rect.move_ip(0, -5)
        else:
            self.kill()

#-------------Main--------------#

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
user = Wizard()

spawning = 500
iterator = 0

score = 0
lives = 3
prevLives = lives
hearts = Hearts()

font = pygame.font.SysFont("Comic Sans MS", 32)

scoreText = font.render(f"Score: {score}", True, BLACK, WHITE)
scoreRect = scoreText.get_rect()
scoreRect.center = (75,25)

livesText = font.render(f"Lives: {lives}", True, BLACK, WHITE)
livesRect = livesText.get_rect()
livesRect.center = (WIDTH-75, 25)

gameoverFont = pygame.font.SysFont("Comis Sans MS", 100)
gameoverText = gameoverFont.render("GAME OVER!!!", True, BLACK, WHITE)
gameoverRect = gameoverText.get_rect()
gameoverRect.center = (WIDTH//2, HEIGHT//2)

ticks = clock.tick(144)

running = True
while running:
    clock.tick(144)
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            sys.exit()
    if lives != 0:
        if iterator >= spawning:
            spiders = Spider((0, randint(50,HEIGHT-300)))
            enemies.add(spiders)
            iterator = 0
        iterator += 1
                
        pressedKeys = pygame.key.get_pressed()
        user.update(pressedKeys)
        screen.fill(WHITE)
        screen.blit(user.image, user.getPosition())
        bullets.draw(screen)
        bullets.update()
        enemies.draw(screen)
        enemies.update()
        screen.blit(scoreText, scoreRect)
        screen.blit(livesText, livesRect)
        if pygame.sprite.groupcollide(bullets, enemies, True, True):
            score += 1
            scoreText = font.render(f"Score: {score}", True, BLACK, WHITE)
        if prevLives != lives:
            livesText = font.render(f"Lives: {lives}", True, BLACK, WHITE)
            prevLives = lives
    else:
        screen.blit(scoreText, scoreRect)
        screen.blit(livesText, livesRect)
        screen.blit(gameoverText, gameoverRect)
    pygame.display.flip()