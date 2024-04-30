from Constants import *


# Class for basic wizard hearts
class Hearts(pygame.sprite.Sprite):
    def __init__(self) -> None:
        self.sprites = [pygame.image.load("sprites/Wizard/0hearts.png").convert_alpha()]
        self.sprites.append(pygame.image.load("sprites/Wizard/1hearts.png").convert_alpha())
        self.sprites.append(pygame.image.load("sprites/Wizard/2hearts.png").convert_alpha())
        self.sprites.append(pygame.image.load("sprites/Wizard/3hearts.png").convert_alpha())
        self.currentSprite = 3
        self.setHeartSprite()
        
    def loseHeart(self):
        self.currentSprite -= 1
        self.setHeartSprite()
        
    def gainHeart(self):
        self.currentSprite += 1
        self.setHeartSprite()
        
    def resetHearts(self):
        self.currentSprite = 3
        self.setHeartSprite()
        
    def setHeartSprite(self):
        self.image = self.sprites[self.currentSprite]
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 5,self.image.get_size()[1] * 5))

# Main user
class Wizard(pygame.sprite.Sprite):
    lives = 3
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.sprites = [pygame.image.load("sprites/Wizard/wiz0.png").convert_alpha()]
        self.sprites.append(pygame.image.load("sprites/Wizard/wiz1.png").convert_alpha())
        self.sprites.append(pygame.image.load("sprites/Wizard/wiz2.png").convert_alpha())
        self.sprites.append(pygame.image.load("sprites/Wizard/wiz3.png").convert_alpha())
        self.currentSprite = 0
        self.spriteBuffer = 0
        
        self.laser = pygame.mixer.Sound('sound/laser.mp3')
        
        self.image = self.sprites[self.currentSprite]
        self.image = pygame.transform.scale(self.image, (200,200))
            
        x = WIDTH // 2
        y = HEIGHT - self.image.get_size()[1] // 2
        self.rect = self.image.get_rect(center = (x, y))
        self.movingRight = False
        self.buffer = 0
        self.speed = 2
        self.bullets = pygame.sprite.Group()
        
    def update(self, keyspressed: dict):
        
        # basic movement Right and left
        if keyspressed[K_RIGHT]:
            if self.rect.center[0] <= WIDTH - self.image.get_size()[0] // 2:
                self.rect.move_ip(self.speed,0)
            self.movingRight = True
    
        if keyspressed[K_LEFT]:
            if self.rect.center[0] >= 0+self.image.get_size()[0] // 2:
                self.rect.move_ip(-self.speed,0)
            self.movingRight = False
              
        # Summons bullet when press space with a buffer limit  
        if keyspressed[K_SPACE]:
            if self.buffer == 0:
                x,y = self.rect.center
                pygame.mixer.Sound.play(self.laser)
                if self.movingRight:
                    x += self.image.get_size()[0] // 2
                else:
                    x -= self.image.get_size()[1] // 2
                
                bullet = BulletWizard((x,y))
                self.bullets.add(bullet)
                self.buffer = 150
                
        # Cycles animation every 30 iterations of buffer
        if self.spriteBuffer >= 30:
            self.cycleSprite()
        else:
            self.spriteBuffer += 1
        
        self.buffer = self.buffer - 1 if self.buffer != 0 else self.buffer

    # Animation for wizard
    def cycleSprite(self):
        if self.currentSprite >= 4: self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]
        self.image = pygame.transform.scale(self.image, (200,200))
        self.currentSprite += 1
        self.spriteBuffer = 0
        if self.movingRight:
            self.image = pygame.transform.flip(self.image, True, False)
            
    def getPosition(self):
        return self.rect.center
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self,position):
        self._x = position if position > 0 and position < WIDTH - self.image.get_size()[0] else self._x

# Bullest for the wizard
class BulletWizard(pygame.sprite.Sprite):
    lives = 3
    def __init__(self,otherSurf) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.sprites = [pygame.image.load("sprites/Bullet0.png").convert(), pygame.image.load("sprites/Bullet1.png").convert()]
        self.sprites[0].set_colorkey(BLACK, RLEACCEL)
        self.sprites[1].set_colorkey(BLACK, RLEACCEL)
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = (otherSurf)
        
        self.currentSprite = 0
        self.spriteBuffer = 0
        
    # Moves down to up based on wizard position
    def update(self):
        if self.rect.center[1] >= 0:
            self.rect.move_ip(0, -5)
            
            if self.spriteBuffer >= 15:
                self.cycleSprite()
            else:
                self.spriteBuffer += 1
                
        else:
            self.kill()           
            
    def cycleSprite(self):
        # Sets current sprite back to 0 if its past 1
        if self.currentSprite > 1: self.currentSprite = 0
        # sets image
        self.image = self.sprites[self.currentSprite]
        self.currentSprite += 1
        self.spriteBuffer = 0
  
# Basic spider           
class Spider(pygame.sprite.Sprite):
    def __init__(self,position) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/spider1.png")
        self.image.set_colorkey((0,0,0),RLEACCEL)
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.buffer = 10
        self.iterator = 0
        
    # Moves from left to right
    def update(self):
        if self.rect.center[0] <= WIDTH:
            self.rect.move_ip(1,0)
        else:
            Wizard.lives -= 1
            self.kill()
    
    def getSize(self):
        return self.image.get_size()
  
# Player for part 2          
class BulletHellPlayer(pygame.sprite.Sprite):
    lives = 3
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/dotPlayer.png").convert_alpha()
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.image.get_rect(center = (x,y))
        self.speed = 2
        
    def update(self, keysPressed: dict) -> None:
        speed = self.speed
        
        # Basic player movement for up, down, left, right
        if keysPressed[K_UP]:
            if self.rect.center[1] > 0 + self.image.get_size()[1] // 2:
                self.rect.move_ip(0,-speed)
            
        if keysPressed[K_DOWN]:
            if self.rect.center[1] < HEIGHT - self.image.get_size()[1] // 2:
                self.rect.move_ip(0,speed)
    
        if keysPressed[K_LEFT]:
            if self.rect.center[0] > 0 + self.image.get_size()[0] // 2:
                self.rect.move_ip(-speed,0)
            
        if keysPressed[K_RIGHT]:
            if self.rect.center[0] < WIDTH - self.image.get_size()[1] // 2:
                self.rect.move_ip(speed,0)
 
# Bullet for spiders           
class BulletSpider(pygame.sprite.Sprite):
    def __init__(self, position, angle) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/BulletSpider.png").convert_alpha()
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.image.get_rect(center = position)
        
        # Uses vectors to change direction the bullet is traveling
        self.center = pygame.Vector2(self.rect.center)
        self.vector = pygame.Vector2()
        self.vector.from_polar((1,angle))
        self.speed = 2
          
    def update(self) -> None:
        prev_XY = self.rect.center
        if (prev_XY[0] > 0 and prev_XY[0] < WIDTH) and (prev_XY[1] > 0 and prev_XY[1] < HEIGHT):            
            self.center += self.vector * self.speed
            self.rect.center = self.center
        else:
            self.kill() 
  
# Phase 2 spiders ( that has bullets )          
class SpiderHell(Spider):
    def __init__(self, position) -> None:
        Spider.__init__(self, position)
        self.bullets = pygame.sprite.Group()
        self.spiderBulletAngle = 0
    
    def update(self):
        sBullet = BulletSpider(self.rect.center,self.spiderBulletAngle)
        self.bullets.add(sBullet)
        # Changes the direction of bullets every time update is ran 
        self.spiderBulletAngle = (self.spiderBulletAngle + randint(20,40)) % 360
        
# Final boss   
class Boss(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/spiderBoss.png").convert_alpha()
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2,(self.image.get_size()[1]//2)+HEIGHT//4)
        self.movingLeft = False
        self.phase2 = False
        
        self.spiderBulletAngle = 90
        self.bullets = pygame.sprite.Group()
        
        self.bulletIterator = 0
        self.bulletBuffer = 75
        
        self.hp = 20
        
        self.health = healthBar((WIDTH//2)-(500//2), 40, 500, 40, self.hp)
        
    def update(self):
        # Moves left and right
        if not self.phase2:
            self.spiderBulletAngle = 90
            if self.movingLeft:
                self.rect.move_ip(-1,0)
            else:
                self.rect.move_ip(1,0)
            
            if self.rect.center[0] < 0 + self.image.get_size()[0] and self.movingLeft:
                self.movingLeft = False
            elif self.rect.center[0] > WIDTH - self.image.get_size()[0] and not self.movingLeft:
                self.movingLeft = True
                
            # Adds a bullet every so often
            if self.bulletIterator == self.bulletBuffer:
                self.addBullet()
                self.bulletIterator = 0
            else: self.bulletIterator += 1
            
        # Phase 2 of boss fight
        else:
            self.rect.center = (WIDTH//2,(self.image.get_size()[1]//2)+HEIGHT//4)
            sBullet = BulletSpider(self.rect.center,self.spiderBulletAngle)
            self.bullets.add(sBullet)
            self.spiderBulletAngle = (self.spiderBulletAngle + randint(20,40)) % 360
            
        
    def addBullet(self):
        sBullet = BulletSpider(self.rect.center,self.spiderBulletAngle)
        self.bullets.add(sBullet)
            
    def updateHealth(self, value):
        self.hp += value
        self.health.updateHealth(value)
               
class healthBar:
    def __init__(self,x,y,w,h,hp) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = hp
        self.maxHp = hp
        
    def draw(self,surface):
        ratio = self.hp / self.maxHp
        
        pygame.draw.rect(surface, 'red', (self.x,self.y,self.w,self.h))
        pygame.draw.rect(surface, 'green', (self.x, self.y, self.w * ratio, self.h))
        
    def updateHealth(self,value):
        self.hp += value
        