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
    
<<<<<<< Updated upstream
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,coord):
        self._x = coord if coord > 0 and coord < WIDTH  else self._x
        
    @property
    def y(self):
        return self._y
=======
# Part one of the game ( basic wiz, bullets and spider movement )
def partOne():
    global iterator, prevLives, score
    # Sets a timer for spiders spawning
    if iterator >= spawning:
        spiders = Spider((0, randint(100,HEIGHT-300)))
        enemies.add(spiders)
        iterator = 0
    iterator += 1
    
    # Updates positions of users, enemies, and bullets
    user.update(pressedKeys)
    enemies.update()
    user.bullets.update()
    
    # Draws sprites on screen
    player.draw(screen)
    enemies.draw(screen)
    user.bullets.draw(screen)
    
    # Changes text when user loses a life
    if prevLives != Wizard.lives:
        hearts.loseHeart()
        hearts.update()
        prevLives = Wizard.lives

def partTwo():
    global lastSpiderBullet, spiderBulletAngle, spiderBulletHell

    currentSpiderBullet = pygame.time.get_ticks()
    
    # adds a bullet every .01 seconds
    if currentSpiderBullet - lastSpiderBullet >= 10:
        for spider in enemies:
            spider.update()
        lastSpiderBullet = pygame.time.get_ticks()
                
    # Updates player pos
    player.update(pressedKeys)
    
    # Updates bullets and draws to screen
    for spider in enemies:
        spider.bullets.update()
        spider.bullets.draw(screen)
    
    
    # Draws player and enemies to screen
    player.draw(screen)
    enemies.draw(screen)
        
def partThree():
    pass
    
>>>>>>> Stashed changes
    
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
player = pygame.sprite.Group()
user = Wizard()
player.add(user)

spawning = 500
iterator = 0

<<<<<<< Updated upstream
score = 0
lives = 3
prevLives = lives
=======
part2 = False
spiderBullets = pygame.sprite.Group()
spiderBulletAngle = 0
lastSpiderBullet = pygame.time.get_ticks()

part3 = False

# Hearts
score = 5
prevLives = Wizard.lives
>>>>>>> Stashed changes
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

running = True
while running:
    clock.tick(144)
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            sys.exit()
<<<<<<< Updated upstream
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
=======
            
    if Wizard.lives > 0 and BulletHellPlayer.lives > 0:

        # Gets presed keys
        pressedKeys = pygame.key.get_pressed()
        
        if score < 5:
            
            partOne()
            
            # Collision Detection
            if pygame.sprite.groupcollide(user.bullets, enemies, True, True):
                score += 1
                scoreText = setScore(score)
        
        else:
            # Part 2 of game
            
            # Initialized part 2 of the game
            if not part2:
                part2 = True
                
                wizard_X, wizard_Y = user.getPosition()
                userPart2 = BulletHellPlayer(wizard_X, wizard_Y)
                
                hearts.resetHearts()
                
                enemies.empty()
                user.bullets.empty()
                player.empty()
                
                spiderBulletHell = SpiderHell((100, 100))
                enemies.add(spiderBulletHell)
                spiderBulletHell2 = SpiderHell((WIDTH-100, 100))
                enemies.add(spiderBulletHell2)
                
                player.add(userPart2)
                
                invisibility_Frame = 150
                invisibility_iteration = 150
                
                # Gets ticks of the beginning frame
                startOfPart2 = pygame.time.get_ticks()
                oneFrameOfPart2 = pygame.time.get_ticks()
                
            # Part 2 ends after 15 seconds
            if oneFrameOfPart2 - startOfPart2 <= 15000:
                   
                partTwo()
                
                # Collision Detection
                if invisibility_iteration == invisibility_Frame:
                    if pygame.sprite.groupcollide(player, spiderBulletHell.bullets, False, False):
                        BulletHellPlayer.lives -= 1
                        hearts.loseHeart()
                        hearts.update()
                        invisibility_iteration = 0
                else:
                    invisibility_iteration += 1 if invisibility_iteration != invisibility_Frame else 0
                oneFrameOfPart2 = pygame.time.get_ticks()

            
            else:
                # initializes part 3 of the game
                if not part3:
                    part3 = True
                    
                    hearts.resetHearts()
                    
                    enemies.empty()
                    player.empty()
                    spiderBullets.empty()
                    
                    player.add(user)
                
                player.update(pressedKeys)
                
                player.draw(screen)
                
    else:
        gameOver()
            
    # updates score and lives        
    screen.blit(scoreText, scoreRect)
    screen.blit(scoreBorder, (WIDTH-275,15))
    
    screen.blit(hearts.image, (25,15))

>>>>>>> Stashed changes
    pygame.display.flip()