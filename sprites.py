from Constants import *
from movement import *

class Hearts(pygame.sprite.Sprite):
    def __init__(self) -> None:
        self.img = "3hearts.png"
        self.setHeartSprite()
        
    def loseHeart(self):
        imageList = list(self.img)
        number = int(self.img[0])
        imageList[0] = str(number-1)
        self.img = ''.join(imageList)
        self.setHeartSprite()
        
    def gainHeart(self):
        imageList = list(self.img)
        number = int(self.image[0])
        imageList[0] = str(number+1)
        self.img = ''.join(imageList)
        self.setHeartSprite()
        
    def setHeartSprite(self):
        self.image = pygame.image.load(f"sprites/{self.img}").convert_alpha()
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 5,self.image.get_size()[1] * 5))

class Wizard(Movement):
    lives = 3
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
        self.bullets = pygame.sprite.Group()
        
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
                    self.bullets.add(bullet)
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
            Wizard.lives -= 1
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