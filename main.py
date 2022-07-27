# Importing libraries
import pygame
import os

# Adding fonts and sound effects
pygame.font.init()
pygame.mixer.init()

# Width and Height of the window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Setting Captions
pygame.display.set_caption("Spaceship War")

# Colors in RGB (red green blue)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Setting the border
BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

# Sound effects
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Settings
FPS = 60 # Frames per second
BLACK_VEL = 5 # Black spaceship speed
BLUE_VEL = 5 # Blue spaceship speed
BULLET_VEL = 7 # Bullet speed
MAX_BULLETS = 3 # Max bullets in a row
SPACESHIP_W, SPACESHIP_H = 55, 55 # Spaceship width and height

# Hit Events
BLUE_HIT = pygame.USEREVENT + 1
BLACK_HIT = pygame.USEREVENT + 2

# Setting up the spaceship images
BLUE_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'bluess.png'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (SPACESHIP_W, SPACESHIP_H)), 270)
BLACK_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'blackss.png'))
BLACK_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLACK_SPACESHIP_IMAGE, (SPACESHIP_W, SPACESHIP_H)), 90)
# Space background
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# Fuction for drawing the first things we see
def draw_window(black, blue, blackBullets, blueBullets, blackHealth, blueHealth):
    
    # Space background and border
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)

    # Health bars
    blackHealthText = HEALTH_FONT.render("Health: " + str(blackHealth), 1, WHITE)
    blueHealthText = HEALTH_FONT.render("Health: " + str(blueHealth), 1, WHITE)
    WIN.blit(blackHealthText, (WIDTH - blackHealthText.get_width() - 10, 10))
    WIN.blit(blueHealthText, (10, 10))

    # Setting up the spaceships
    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y))
    WIN.blit(BLACK_SPACESHIP, (black.x, black.y))

    # Setting up the bullets
    for bullet in blackBullets:
        pygame.draw.rect(WIN, WHITE, bullet)

    for bullet in blueBullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    # Updating the screen
    pygame.display.update()

# Function for handling blue spaceship's movements (WASD)
def blueHandleMovement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - BLUE_VEL > 0: # LEFT
        blue.x -= BLUE_VEL
    if keys_pressed[pygame.K_d] and blue.x + BLUE_VEL + blue.width < BORDER.x: # RIGHT
        blue.x += BLUE_VEL
    if keys_pressed[pygame.K_w] and blue.y - BLUE_VEL > 0: # UP
        blue.y -= BLUE_VEL
    if keys_pressed[pygame.K_s] and blue.y + BLUE_VEL + blue.width < HEIGHT - 15: # DOWN
        blue.y += BLUE_VEL

# Function for handling black spaceship's movements (Arrows)
def blackHandleMovement(keys_pressed, black):
    if keys_pressed[pygame.K_LEFT] and black.x - BLACK_VEL > BORDER.x + BORDER.width: # LEFT
        black.x -= BLACK_VEL
    if keys_pressed[pygame.K_RIGHT] and black.x + BLACK_VEL + black.width < WIDTH: # RIGHT
        black.x += BLACK_VEL
    if keys_pressed[pygame.K_UP] and black.y - BLACK_VEL > 0: # UP
        black.y -= BLACK_VEL
    if keys_pressed[pygame.K_DOWN] and black.y + BLACK_VEL + black.width < HEIGHT: # DOWN
        black.y += BLACK_VEL

# Function for handling bullets
def handleBullets(blueBullets, blackBullets, blue, black):
    for bullet in blueBullets:
        # Bullet movement
        bullet.x += BULLET_VEL

        if black.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLACK_HIT)) # If blue spaceship's bullets hit black spaceship, it runs the BLACK_HIT event
            blueBullets.remove(bullet)
        elif bullet.x > WIDTH:
            blueBullets.remove(bullet) # If it doesn't hit the black spaceship, it disappears

    # Same as above, but with black spaceship's bullets
    for bullet in blackBullets:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            blackBullets.remove(bullet)
        elif bullet.x < 0:
            blackBullets.remove(bullet)

# Function for showing the text after a spaceship wins
def drawWinner(text):
    if text == "Blue Won!": 
        drawText = WINNER_FONT.render(text, 1, BLUE) # If blue won, the text will be blue
    elif text == "Black Won!":
        drawText = WINNER_FONT.render(text, 1, WHITE) # If black won, the text will be black

    # Shows that up
    WIN.blit(drawText, (WIDTH/2 - drawText.get_width()/2, HEIGHT/2 - drawText.get_height()/2))

    # Updates the screen and after 5 seconds (5000 milliseconds), it runs the game again
    pygame.display.update()
    pygame.time.delay(5000)


# Main function of the game
def main():
    # Spaceships
    black = pygame.Rect(700, 300, SPACESHIP_W, SPACESHIP_H)
    blue = pygame.Rect(100, 300, SPACESHIP_W, SPACESHIP_H)

    # Bullets
    blackBullets = []
    blueBullets = []

    # Health
    blackHealth = 10
    blueHealth = 10


    clock = pygame.time.Clock()
    run = True
    while run:
        # Runs at a certain FPS (60 in this case)
        clock.tick(FPS)
        for event in pygame.event.get():

            # If we click X on the window, it will quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


            if event.type == pygame.KEYDOWN:
                # Press Left CTRL to shoot from the blue spaceship
                if event.key == pygame.K_LCTRL and len(blueBullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5)
                    blueBullets.append(bullet) # Adds the bullet to a list
                    BULLET_FIRE.play() # Sound Effect

                # Press Right CTRL to shoot from the black spaceship
                if event.key == pygame.K_RCTRL and len(blackBullets) < MAX_BULLETS:
                    bullet = pygame.Rect(black.x, black.y + black.height//2 - 2, 10, 5)
                    blackBullets.append(bullet) # Adds the bullet to a list
                    BULLET_FIRE.play() # Sound Effect

            # BLACK_HIT event
            if event.type == BLACK_HIT:
                blackHealth -= 1 # Removes one from the health
                BULLET_HIT_SOUND.play() # Sound Effects

            # BLUE_HIT event
            if event.type == BLUE_HIT:
                blueHealth -= 1 # Removes one from the health
                BULLET_HIT_SOUND.play() # Sound Effects


        # Text for showing who wins
        winnerText = ""

        if blackHealth <= 0:
            winnerText = "Blue Won!"

        if blueHealth <= 0:
            winnerText = "Black Won!"

        if winnerText != "":
            drawWinner(winnerText)
            break

        # Gets the pressed keys for movement and shooting
        keys_pressed = pygame.key.get_pressed()

        # Calling the functions
        blueHandleMovement(keys_pressed, blue)
        blackHandleMovement(keys_pressed, black)
        handleBullets(blueBullets, blackBullets, blue, black)
        draw_window(black, blue, blackBullets, blueBullets, blackHealth, blueHealth)

        
        

    main()


if __name__ == "__main__":
    main()
