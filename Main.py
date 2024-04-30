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
    
def wingame():
    winGameFont = pygame.font.SysFont("Comis Sans MS", 100)
    winGameText = winGameFont.render("YOU WIN!!!", True, WHITE)
    winGameRect = winGameText.get_rect()
    winGameRect.center = (WIDTH//2, HEIGHT//2)
    screen.blit(winGameText, winGameRect)
    
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
    if currentSpiderBullet - lastSpiderBullet >= 20:
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

# Iteration for spawning spiders
spawning = 500
iterator = 0

# Set up part 2
part2 = False
spiderBullets = pygame.sprite.Group()
spiderBulletAngle = 0
lastSpiderBullet = pygame.time.get_ticks()

# Setup part 3
part3 = False

# Win condition
win = False

# Hearts and score
score = 0
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
            
    # Runs main loop if user has lives left
    if (Wizard.lives > 0 and BulletHellPlayer.lives > 0):

        # Gets presed keys
        pressedKeys = pygame.key.get_pressed()
        
        # part 1 is ran if the score is below 5
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
                
                # Resets hearts
                hearts.resetHearts()
                Wizard.lives = 3
                
                # Gets rid of all other sprites loaded
                enemies.empty()
                user.bullets.empty()
                player.empty()
                
                # Sets position of new character in position of the wizard
                wizard_X, wizard_Y = user.getPosition()
                userPart2 = BulletHellPlayer(wizard_X, wizard_Y)
                player.add(userPart2)
                
                # Adds the topleft and topright spider
                spiderBulletHell = SpiderHell((100, 100))
                enemies.add(spiderBulletHell)
                spiderBulletHell2 = SpiderHell((WIDTH-100, 100))
                enemies.add(spiderBulletHell2)
                
                invisibility_Frame = 150
                invisibility_iteration = 150
                
                # Gets ticks of the beginning frame
                startOfPart2 = pygame.time.get_ticks()
                oneFrameOfPart2 = pygame.time.get_ticks()
                
                # Adds score every 100 iterations
                scoreIterator = 0
                scoreBuffer = 100
                
            # Part 2 ends after 15 seconds
            if oneFrameOfPart2 - startOfPart2 <= 15000:
                   
                partTwo()
                
                # Collision Detection with invisibility frames
                if invisibility_iteration == invisibility_Frame:
                    if pygame.sprite.groupcollide(player, spiderBulletHell.bullets, False, False):
                        BulletHellPlayer.lives -= 1
                        hearts.loseHeart()
                        hearts.update()
                        invisibility_iteration = 0
                else:
                    invisibility_iteration += 1 if invisibility_iteration != invisibility_Frame else 0
                oneFrameOfPart2 = pygame.time.get_ticks()
                
                # Adds score every 100 iterations 
                if scoreIterator == scoreBuffer:
                    score += 1
                    scoreIterator = 0
                    scoreText = setScore(score)
                else: scoreIterator += 1

            
            else:
                # initializes part 3 of the game
                if not part3:
                    part3 = True
                    miniphase = True
                    startOfMiniphase = True
                    
                    # Resets hearts
                    hearts.resetHearts()
                    
                    # Removes all other sprites
                    enemies.empty()
                    player.empty()
                    spiderBullets.empty()
                    
                    # Sets up boss
                    boss = Boss()
                    enemies.add(boss)
                    
                    # Add wizard back to player group
                    player.add(user)
                    
                    invisibility_Frame = 150
                    invisibility_iteration = 150
                    
                # If the boss dies, you win
                if boss.hp == 0:
                    wingame()
                
                # Starts phase 2 when boss has 4 hp
                if boss.hp == 4 and miniphase:
                    boss.phase2 = True
                    
                    # Initilized at start of phase 2
                    if startOfMiniphase:
                        startOfMiniphase = False
                        # changes wizard back to bullet hell player
                        player.empty()
                        userPart2 = BulletHellPlayer(wizard_X, wizard_Y)
                        player.add(userPart2)
                        
                        # sets up ticks to keep track of how long phase 2 has been
                        startOfPhase2 = pygame.time.get_ticks()
                        oneFrameOfPhase2 = pygame.time.get_ticks()
                    
                    # Phase 2 lasts 8 seconds
                    if not(oneFrameOfPhase2 - startOfPhase2 <= 8000):
                        miniphase = False
                    oneFrameOfPhase2 = pygame.time.get_ticks()
                        
                # Ran once phase 2 ends
                elif boss.hp == 4 and not miniphase:
                    boss.phase2 = False
                    
                    # removes all bullets on screen
                    boss.bullets.empty()
                    
                    # Resets player back to wizard
                    player.empty()
                    player.add(user)
                    boss.updateHealth(-1)
                    
                                        
                user.bullets.update()
                player.update(pressedKeys)
                enemies.update()
                boss.bullets.update()
                
                
                # Adds to score if user hits boss
                if pygame.sprite.groupcollide(enemies, user.bullets, False, True):
                    boss.updateHealth(-1)
                    score += 1
                    scoreText = setScore(score)
                    if boss.hp == 0:
                        boss.kill()
                        boss.bullets.empty()
                        score += 100
                        scoreText = setScore(score)
                        win = True
                
                # Collision detection with invisibility frames     
                if invisibility_iteration == invisibility_Frame:
                    if pygame.sprite.groupcollide(boss.bullets, player, True, False):
                        hearts.loseHeart()
                        Wizard.lives -= 1
                else:
                    invisibility_iteration += 1 if invisibility_iteration != invisibility_Frame else 0
                
                user.bullets.draw(screen)
                player.draw(screen)
                enemies.draw(screen)
                boss.bullets.draw(screen)
                boss.health.draw(screen)  
                
    else:
        gameOver()
            
    # updates score and lives        
    screen.blit(scoreText, scoreRect)
    screen.blit(scoreBorder, (WIDTH-275,15))
    
    screen.blit(hearts.image, (25,15))

    pygame.display.flip()