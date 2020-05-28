import pygame
import random
import math

from pygame import mixer

#INITIALISE PYGAME
pygame.init()
font=pygame.font.Font('Img/REGELLOS.ttf',32)

#PYGAME DISPLAY
screen = pygame.display.set_mode((800,600))
bg_color= (19,46,50)

#BACKGROUND CONFIGURATION
background=pygame.image.load("Img/space1.jpg")
background=pygame.transform.scale(background, (800, 600))

#MUSIC
mixer.music.load('Music/EZ4ENCE.mp3')
mixer.music.play(-1)

#TITLE AND ICON
pygame.display.set_caption("Galactic Wars")
icon= pygame.image.load("Img/meteor.png")
pygame.display.set_icon(icon)

#PLAYER ICON
playerimg=pygame.image.load('Img/spaceship.png')
playerX=370
playerY=480
playerX_change=0

#DRAWING THE PLAYER ICON ON SCREEN
def player(x,y):
    screen.blit(playerimg,(x,y))


#ENEMY ICON
alienimg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_enemies=6

ali=pygame.image.load('Img/alien.png')
ali=pygame.transform.scale(ali, (32, 32))
ali1=pygame.image.load('Img/alien1.png')
ali2=pygame.image.load('Img/alien (1).png')
img=[ali,ali1,ali2]

for i in range(num_enemies):
    alienimg.append(random.choice(img))  #size scaling
    alienX.append(random.randint(0,735))
    alienY.append(random.randint(50, 200))
    alienX_change.append(2.2)
    alienY_change.append(50)

#DRAWING THE ALIEN ICON ON SCREEN
def alien(x,y,i):
    screen.blit(alienimg[i],(x,y))

#BULLETS
bulletimg=pygame.image.load('Img/bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state = "READY"          #READY=BULLET CAN'T BE SEEN / #FIRE= THE BULLET IS CURRENTLY MOVING 

#DRAWING BULLETS ON SCREEN
def bullet(x,y):
    global bullet_state
    bullet_state="FIRE"
    screen.blit(bulletimg,(x+16,y+10))

def isCollision(alienX,alienY,bulletX,bulletY):
    distance=math.sqrt(math.pow((alienX-bulletX),2)+math.pow((alienY-bulletY),2))
    if distance < 27:
        return True
    else:
        return False


#MAINTAIN SCORE
points=0
font=pygame.font.Font('Img/REGELLOS.ttf',32)

textX=10
textY=10

def show_score(x,y):
    score = font.render("Score :" + str(points),True,(252, 163, 17))
    screen.blit(score,(x,y))

#GAME OVER
over_font=pygame.font.Font('Img/REGELLOS.ttf',50)

def game_over():
    over_text = over_font.render("YOU SERIOUSLY LOST TO THESE CHUMPS?",True,(252,163,17))
    screen.blit(over_text,(20,250))

#VICTORY
win_font=pygame.font.Font('Img/REGELLOS.ttf',40)
win_font2=pygame.font.Font('Img/REGELLOS.ttf',35)
def victory():
    win_text1 = win_font.render("YOUR SCORE IS 100!!! VICTORY IS YOURS",True,(252,163,17))
    screen.blit(win_text1,(110,250))
    win_text2 = win_font2.render("These villains stand no chance, you are a HERO!!!",True,(252,163,17))
    screen.blit(win_text2,(115,300))

running = True
#GAME LOOP
while running:
    
    screen.fill(bg_color)
    screen.blit(background,(0,0))
    #CONFIGURE EXIT BUTTON
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #CHECKING KEYSTROKE
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change=-5
            if event.key == pygame.K_RIGHT:
                playerX_change=5
            if event.key == pygame.K_SPACE:
                if bullet_state is "READY":
                    bulletX=playerX
                    bullet_sound=mixer.Sound('Music/laser.wav')
                    bullet_sound.play()
                    bullet(bulletX,bulletY)
                    
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_LEFT):
                playerX_change=0

    #SPACESHIP CONTROL
    playerX += playerX_change
    if playerX <0:
        playerX=0
    elif playerX>736:
        playerX=736

    #ALIEN CONTROL
    for i in range(num_enemies):

        #GAME OVER
        if alienY[i]>440:
            for j in range(num_enemies):
                alienY[j]=2000
            game_over()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <=0:
            alienX_change[i]=2.5
            alienY[i]+=30
        elif alienX[i]>736:
            alienX_change[i]=-2.5
            alienY[i]+=alienY_change[i]
        
        alien(alienX[i],alienY[i],i)
        
        collision=isCollision(alienX[i],alienY[i],bulletX,bulletY)
        if collision:
            bulletY=480
            bullet_state="READY"
            points+=1
            collision_sound=mixer.Sound('Music/Explosion.wav')
            collision_sound.play()
            alienX[i]=random.randint(0,735)
            alienY[i]=random.randint(50, 200)
        if points == 100:
            for j in range(num_enemies):
                alienY[j]=-2000
            victory()
            break
            
    #BULLET MOVEMENT
    if bullet_state is "FIRE":
        bullet(bulletX,bulletY)
        bulletY-=bulletY_change

    if bulletY<=0:
        bulletY=480
        bullet_state="READY"

    #FINAL DISPLAY
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()

    