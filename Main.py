from Constants import *
import sys
from sprites import *

def setScore(score,firstRun = False):
    text = font.render(f"Score: {score}", True, BLACK, WHITE)
    if firstRun:
        rect = text.get_rect()
        rect.center = (WIDTH-75,25)
        return text, rect
    return text

def setLives(lives, firstRun = False):
    text = font.render(f"Lives: {lives}", True, BLACK, WHITE)
    if firstRun:
        rect = text.get_rect()
        rect.center = (75,25)
        return text, rect
    return text

def gameOver():
    gameoverFont = pygame.font.SysFont("Comis Sans MS", 100)
    gameoverText = gameoverFont.render("GAME OVER!!!", True, BLACK, WHITE)
    gameoverRect = gameoverText.get_rect()
    gameoverRect.center = (WIDTH//2, HEIGHT//2)
    screen.blit(gameoverText, gameoverRect)
    
    
#-------------Main--------------#

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

enemies = pygame.sprite.Group()
user = Wizard()

spawning = 500
iterator = 0

score = 0
prevLives = Wizard.lives
hearts = Hearts()

font = pygame.font.SysFont("Comic Sans MS", 32)

scoreText,scoreRect = setScore(score,True)
livesText,livesRect = setLives(Wizard.lives,True)

ticks = clock.tick(144)

running = True
while running:
    
    clock.tick(144)
    screen.fill(WHITE)
    
    screen.blit(scoreText, scoreRect)
    screen.blit(hearts.image, (25,15))
    
    # Lets you press x to exit game
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            sys.exit()
    if Wizard.lives != 0:
        
        # Sets a timer for spiders spawning
        if iterator >= spawning:
            spiders = Spider((0, randint(50,HEIGHT-300)))
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
            livesText = setLives(Wizard.lives)
            prevLives = Wizard.lives
    
    else:
        gameOver()
        
    # updates score and lives
        
    pygame.display.flip()