# Py-Pong
from pygame import *
from pygame.locals import *
import random
import webbrowser as web

init()
mixer.init()
font.init()

# Constant Variables
LENGTH = 858
HEIGHT = 525
WINDOW = display.set_mode((LENGTH, HEIGHT))
CLOCK = time.Clock()
ICON = image.load("icon.png").convert()

display.set_caption("Py-Pong!")
display.set_icon(ICON)

# Non-Constant Variables
player1_score = 0
player2_score = 0

# Fonts
dev_font = font.Font('8bit.ttf', 20)
font_28 = font.Font('8bit.ttf', 28)
ai_font = font.Font('8bit.ttf', 30)
winner_font = font.Font('8bit.ttf', 40)
serve_font = font.Font('8bit.ttf', 45)
score_font = font.Font('8bit.ttf', 80)
font_72 = font.Font('8bit.ttf', 72)
title_font = font.Font('8bit.ttf', 115)

# Game Controlling Bools
timeout = True
gameEnd = False
onHome = True
aiPlayer = False
paused = False
start = True

r=random.randint(100,255)
g=random.randint(100,255)
b=random.randint(100,255)

# Player Class
class Player(sprite.Sprite):
    # Initialize Player
    def __init__(self, playernum, x):
        super(Player, self).__init__()
        self.image = Surface((6, 45))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midleft=(x, HEIGHT/2))
        self.playernum = playernum

    def update(self):
        keys = key.get_pressed()

        if not timeout and self.playernum==0:
            if keys[K_w]:
                self.rect.y -= 8
            if keys[K_s]:
                self.rect.y += 8
        elif not timeout and self.playernum==1:
            if keys[K_UP]:
                self.rect.y -= 8
            if keys[K_DOWN]:
                self.rect.y += 8

        if self.rect.y < 0:
            self.rect.y = 2
        elif self.rect.y > HEIGHT-47:
            self.rect.y = HEIGHT-47

        WINDOW.blit(self.image, self.rect)

# Ball Class
class Ball(sprite.Sprite):
    # Initialize Ball
    def __init__(self, player1, player2):
        super(Ball, self).__init__()
        self.image = Surface((10, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(LENGTH/2, HEIGHT/2))
        self.rect.y = random.randint(20, HEIGHT-20)

        self.player1 = player1
        self.player2 = player2      
        self.vel_y = random.choice([-3, 3])
        self.vel_x = random.choice([-3, 3])

    def update(self):
        global player1_score, player2_score
        mixer.music.set_volume(1.0)

        if player1.rect.colliderect(self.rect):
            mixer.music.load("ballHit.wav")
            mixer.music.play()
            self.vel_x = -self.vel_x
        elif player2.rect.colliderect(self.rect):
            mixer.music.load("ballHit.wav")
            mixer.music.play()
            self.vel_x = -self.vel_x
        elif self.rect.y <= 0:
            mixer.music.load("ballHit.wav")
            mixer.music.play()
            self.vel_y = -self.vel_y
        elif self.rect.y >= 515:
            mixer.music.load("ballHit.wav")
            mixer.music.play()
            self.vel_y = -self.vel_y

        # Checks if ball is out of bounds on Player 1's side, if so give 1 point to Player 2
        if self.rect.x <= -11:
            mixer.music.load("scoreUp.wav")
            mixer.music.play()
            player2_score += 1
            GameEnd()
            Reset()

        # Checks if ball is out of bounds on Player 2's side, if so give 1 point to Player 1
        if self.rect.x >= 869:
            mixer.music.load("scoreUp.wav")
            mixer.music.play()
            player1_score += 1
            GameEnd()
            Reset()

        # Sets the ball's velocity to (0,0) to keep it in place during serving mode, else it += self.vel_[x or y] to self.rect.[x or y]
        if timeout:
            self.rect.x += 0
            self.rect.y += 0
        else:
            self.rect.x += self.vel_x
            self.rect.y += self.vel_y

        WINDOW.blit(self.image, self.rect)

# Creates the "net" that is in the middle of the screen
def MiddleSplit():
    width = 2
    height = 10
    y = 0
    for i in range(int(HEIGHT/3)):
        draw.rect(WINDOW, (255, 255, 255), (LENGTH/2-width/2,0+(height*i)+y,width,height))
        y += 10

# Resets player 1 and player 2 pos when ball goes out of bounds
def Reset():
    global timeout
    player1.rect.center = (10, HEIGHT/2)
    player2.rect.center = (LENGTH-10, HEIGHT/2)
    ball.rect.center = (LENGTH/2, random.randint(20, HEIGHT-20))
    timeout = True

# Ends game when score cap is met by either player
def GameEnd():
    global gameEnd
    if player1_score == 3:
        gameEnd = True
    elif player2_score == 3:
        gameEnd = True

# Class Variables
player1 = Player(0, 10)
player2 = Player(1, LENGTH-10)
ball = Ball(player1_score, player2_score)
#MAIN TITLE#
title = title_font.render("Py-Pong", False, (255,255,255))
title_rect = title.get_rect(center=(LENGTH/2,HEIGHT/2-185))
#DEVELOPER CREDITS#
dev = dev_font.render('Developed By The-BigMan', False, (255, 255, 255))
dev_rect = dev.get_rect(center=(LENGTH/2, HEIGHT/2-85))
#COMING SOON#
ai = ai_font.render('(Coming Soon)', False, (255, 255, 255))
ai_rect = ai.get_rect(center=(LENGTH/2, HEIGHT/2))
#2 PLAYERS#
multi = ai_font.render('2 Players', False, (255, 255, 255))
multi_rect = multi.get_rect(center=(LENGTH/2, HEIGHT/2+40))
#GITHUB URL#
url = dev_font.render("The-BigMan's Github", False, (255, 255, 255))
url_rect = url.get_rect(midleft=(20, 500))
#GAMEOVER HEADER#
gameover = font_72.render('Game Over!', False, (255, 255, 255))
gameover_rect = gameover.get_rect(center=(LENGTH/2, HEIGHT/2-50))
#RESTART GAME#
restart = font_28.render('Press SPACE to Replay or Press ESC to Quit', False, (255, 255, 255))
restart_rect = restart.get_rect(center=(LENGTH/2, HEIGHT/2+100))

homeElements = [title_rect, dev_rect, ai_rect, multi_rect, url_rect]

# Main game loop
while start:
    mouse_pos = mouse.get_pos()
    WINDOW.fill((0, 0, 0))
    for EVENT in event.get():
        if EVENT.type == QUIT:
            start = False
        if EVENT.type == KEYDOWN:
            if EVENT.key == K_SPACE and timeout:
                timeout = False
            elif EVENT.key == K_TAB:
                if onHome == False:
                    if gameEnd == False:
                        if paused == False:
                            paused = True
                        else:
                            paused = False
                                
        if url_rect.collidepoint(mouse_pos):
            mouse.set_cursor(11)
            url = dev_font.render("The-BigMan's Github", False, (r,g,b))
            if mouse.get_pressed()[0]:
                web.open(r"https://github.com/The-BigMan")
        else:
            mouse.set_cursor(0)
            url = dev_font.render("The-BigMan's Github", False, (255,255,255))

        if dev_rect.collidepoint(mouse_pos):
            dev = dev_font.render("Developed By The-BigMan", False, (r,g,b))
        else:
            dev = dev_font.render("Developed By The-BigMan", False, (255,255,255))

        if multi_rect.collidepoint(mouse_pos):
            mouse.set_cursor(11)
            multi = ai_font.render("2 Players", False, (r,g,b))
            if mouse.get_pressed()[0]:
                for i in homeElements:
                    i.center=(10000,10000)
                onHome=False
        else:
            multi = ai_font.render("2 Players", False, (255,255,255))

        if ai_rect.collidepoint(mouse_pos):
            mouse.set_cursor(11)
            ai = ai_font.render("(Coming Soon)", False, (r,g,b))
        else:
            ai = ai_font.render("(Coming Soon)", False, (255,255,255))

        if title_rect.collidepoint(mouse_pos):
            title = title_font.render("Py-Pong", False, (r,g,b))
        else:
            title = title_font.render("Py-Pong", False, (255,255,255))


    if timeout:
        serve = serve_font.render('Press Space to Serve Ball', False, (60, 60, 60))
        serve_rect = serve.get_rect(center=(LENGTH/2+10, HEIGHT/2))
    else:
        serve_rect.center = (10000, 10000)

    # Shows game over screen when gameEnd bool is ==true
    if gameEnd:

        keys = key.get_pressed()

        if player1_score > player2_score:
            winner = winner_font.render('Player 1 Won the Game', False, (255, 255, 255))
        elif player2_score > player1_score:
            winner = winner_font.render('Player 2 Won the Game', False, (255, 255, 255))

        winner_rect = winner.get_rect(center=(LENGTH/2, HEIGHT/2+5))

        WINDOW.blit(gameover, gameover_rect)
        WINDOW.blit(winner, winner_rect)
        WINDOW.blit(restart, restart_rect)

        if keys[K_SPACE]:
            gameEnd = False
            player1_score = 0
            player2_score = 0
            Reset()
        elif keys[K_ESCAPE]:
            start = False
    else:
        # Shows main menu screen when onHome bool ==true
        if onHome:
            WINDOW.blit(title, title_rect)
            WINDOW.blit(dev, dev_rect)
            WINDOW.blit(ai, ai_rect)
            WINDOW.blit(multi, multi_rect)
            WINDOW.blit(url, url_rect)

        elif paused:
            keys = key.get_pressed()

            #PAUSED HEADER#
            paused = font_72.render("Paused", False, (255, 255, 255))
            paused_rect = paused.get_rect(center=(LENGTH/2, HEIGHT/2-50))

            #RESUME GAME#
            resume = font_28.render('Press TAB to Resume Game or Press ESC to Quit', False, (255, 255, 255))
            resume_rect = resume.get_rect(center=(LENGTH/2, HEIGHT/2+100))

            if keys[K_ESCAPE]:
                start = False

            WINDOW.blit(paused, paused_rect)
            WINDOW.blit(resume, resume_rect)
        else:
            WINDOW.blit(serve, serve_rect)

            player1.update()
            player2.update()
            ball.update()
            MiddleSplit()

            score1 = score_font.render(str(player1_score), False, (255, 255, 255))
            score2 = score_font.render(str(player2_score), False, (255, 255, 255))
            score1_rect = score1.get_rect(center=(LENGTH/4, 64))
            score2_rect = score2.get_rect(center=(LENGTH-(LENGTH/4), 64))

            WINDOW.blit(score1, score1_rect)
            WINDOW.blit(score2, score2_rect)

    display.update()
    display.flip()
    CLOCK.tick(60)

quit()