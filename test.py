<<<<<<< Updated upstream
img = "3hearts.png"
number = int(img[0])
imgList = list(img)
imgList[0] = str(number-1)
img = ''.join(imgList)
print(img)
=======
from Constants import *
import sys
from sprites import *

def setScore(score,firstRun = False):
    text = font.render(f"Score: {score}", True, WHITE)
    if firstRun:
        rect = text.get_rect()
        rect.center = (WIDTH-150,73)
        return text, rect
    return text

def gameOver():
    gameoverFont = pygame.font.SysFont("Comis Sans MS", 100)
    gameoverText = gameoverFont.render("GAME OVER!!!", True, WHITE)
    gameoverRect = gameoverText.get_rect()
    gameoverRect.center = (WIDTH//2, HEIGHT//2)
    screen.blit(gameoverText, gameoverRect)
    
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
    global lastSpiderBullet, spiderBulletAngle    

    currentSpiderBullet = pygame.time.get_ticks()
    
    if currentSpiderBullet - lastSpiderBullet >= 10:
        sBullet = BulletSpider((WIDTH//2, HEIGHT//2),spiderBulletAngle)
        spiderBullets.add(sBullet)
        spiderBulletAngle = (spiderBulletAngle + randint(20,40)) % 360
        lastSpiderBullet = pygame.time.get_ticks()
                
    player.update(pressedKeys)
    enemies.update()
    spiderBullets.update()
    
    
    player.draw(screen)
    enemies.draw(screen)
    spiderBullets.draw(screen)
        
def partThree():
    pass
    
    
#-------------Main--------------#

# Initilizing Pygame
pygame.init()
pygame.mixer.init()

# Setting up screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Wizard Game")
clock = pygame.time.Clock()

# Sets up the enemies and wizard
enemies = pygame.sprite.Group()
player = pygame.sprite.Group()
user = Wizard()
player.add(user)
userPart2 = BulletHellPlayer()

# Iteration for spawning spiders
spawning = 500
iterator = 0

part2 = False
spiderBullets = pygame.sprite.Group()
spiderBulletAngle = 0
lastSpiderBullet = pygame.time.get_ticks()

part3 = False

# Hearts
score = 9
prevLives = Wizard.lives
hearts = Hearts()

# Sets Font
font = pygame.font.SysFont("ebrima", 32,bold=True)

# Sets up the scoring and the border image
scoreText,scoreRect = setScore(score,True)
scoreBorder = pygame.image.load("sprites/Border.png").convert_alpha()
scoreBorder.set_colorkey((0,0,0), RLEACCEL)
scoreBorder = pygame.transform.scale(scoreBorder, (scoreBorder.get_size()[0] * 5,scoreBorder.get_size()[1] * 5))

# Loads the background
bg = pygame.image.load("sprites/bg.png")
bg = pygame.transform.smoothscale(bg, (WIDTH,HEIGHT))

running = True
while running:
    clock.tick(144)
    screen.fill(WHITE)
    screen.blit(bg,(0,0))
    
    # Lets you press x to exit game
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            sys.exit()
            
    if Wizard.lives > 0 and BulletHellPlayer.lives > 0:

        # Gets presed keys
        pressedKeys = pygame.key.get_pressed()
        
        if score <= 9:
            
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
                
                hearts.resetHearts()
                
                enemies.empty()
                user.bullets.empty()
                player.empty()
                
                spiderPart2 = Spider2((WIDTH//2, HEIGHT//2))
                enemies.add(spiderPart2)
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
                    if pygame.sprite.groupcollide(player, spiderBullets, False, False):
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

    pygame.display.flip()
>>>>>>> Stashed changes
