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
user = Wizard()

# Iteration for spawning spiders
spawning = 500
iterator = 0

# Hearts
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

ticks = clock.tick(144)

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
    if Wizard.lives != 0:
        
        # Sets a timer for spiders spawning
        if iterator >= spawning:
            spiders = Spider((0, randint(100,HEIGHT-300)))
            enemies.add(spiders)
            iterator = 0
        iterator += 1
            
        # Gets presed keys
        pressedKeys = pygame.key.get_pressed()
        
        # Updates positions of users, enemies, and bullets
        user.update(pressedKeys)
        enemies.update()
        user.bullets.update()
        
        # Draws sprites on screen
        screen.blit(user.image, user.getPosition())
        enemies.draw(screen)
        user.bullets.draw(screen)
        
        # Checks for collision
        # Adds score if a bullet hits a spider
        if pygame.sprite.groupcollide(user.bullets, enemies, True, True):
            score += 1
            scoreText = setScore(score)
        
        # Changes text when user loses a life
        if prevLives != Wizard.lives:
            hearts.loseHeart()
            hearts.update()
            prevLives = Wizard.lives
    
    else:
        gameOver()
        
    # updates score and lives        
    screen.blit(scoreText, scoreRect)
    screen.blit(scoreBorder, (WIDTH-275,15))
    
    screen.blit(hearts.image, (25,15))

        
    pygame.display.flip()