import pygame
pygame.init()

#set up window 
WIDTH, HEIGHT = 700, 500
Window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")
FPS = 60# 60 frames/ second. 
#colors: this will be a black and white game.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Objects
P_Width, P_Hight = 20, 100
B_BAll = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
#play to
WINNING_SCORE = 3

#maine function 
def main():
    run = True
    clock = pygame.time.Clock()
    #set up the paddles, make sure the starting possitino is at the center
    Words_player = Paddle(10, HEIGHT//2 - P_Hight // 2, P_Width, P_Hight)
    Arrows_player = Paddle(WIDTH - 10 - P_Width, HEIGHT // 2 - P_Hight//2, P_Width, P_Hight)
    ball = Ball(WIDTH // 2, HEIGHT // 2, B_BAll)
    #scores
    words_score = 0
    arrows_score = 0
    #do while the game is runnign
    while run:
        clock.tick(FPS)
        draw(Window, [Words_player, Arrows_player], ball, words_score, arrows_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        #input
        keys = pygame.key.get_pressed()
        handle_movement(keys, Words_player, Arrows_player)
        #ball
        ball.move()
        handle_collision(ball, Words_player, Arrows_player)
        if ball.x < 0:
            arrows_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            words_score += 1
            ball.reset()
        won = False
        if words_score >= WINNING_SCORE:
            won = True
            win_text = "Letters won!"
        elif arrows_score >= WINNING_SCORE:
            won = True
            win_text = "Arrows won!"

        #if a player reaches the winning score
        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            Window.blit(text, (WIDTH//2 - text.get_width() // 2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            Words_player.reset()
            Arrows_player.reset()
            words_score = 0
            arrows_score = 0
    pygame.quit()

#the paddle class, this class will be used to handle the paddle functions
#draw it, move it(up and down)
class Paddle:
    COLOR = WHITE
    Paddle_velocity = 4
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.original_x = x
        self.x = self.original_x
        self.original_y = y
        self.y = self.original_y

    def draw(self, win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height))
    def move(self, up=True):
        if up:
            self.y -= self.Paddle_velocity
        else:
            self.y += self.Paddle_velocity
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

#the Ball class, this class will be used to handle the ball functions
#bounce
class Ball:
    Ball_Velocity = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.original_x = x
        self.x = self.original_x
        self.original_y = y
        self.y = self.original_y
        self.radius = radius
        self.horizontal_velocity = self.Ball_Velocity
        self.vertical_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.horizontal_velocity
        self.y += self.vertical_vel
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.vertical_vel = 0
        self.horizontal_velocity *= -1

#Draw on the window
def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)


    ball.draw(win)
    pygame.display.update()

#move the paddles
def handle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.Paddle_velocity >= 0:# press w, to move up
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.Paddle_velocity + left_paddle.height <= HEIGHT:# press s, to move down....
        left_paddle.move(up=False)

    #Same as above, but this is for the player using arrow keys
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.Paddle_velocity >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.Paddle_velocity + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.vertical_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.vertical_vel *= -1

    if ball.horizontal_velocity < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                #The bounce mechanics are based on simply reversing the velocity.
                #we do this by multiplying it by -1. 
                ball.horizontal_velocity *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                Vertical_change = middle_y - ball.y
                reduce = (left_paddle.height / 2) / ball.Ball_Velocity
                vertical_vel = Vertical_change / reduce
                ball.vertical_vel = -1 * vertical_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                #same as above, for the vertical colisions
                ball.horizontal_velocity *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                Vertical_change = middle_y - ball.y
                reduce = (right_paddle.height / 2) / ball.Ball_Velocity
                vertical_vel = Vertical_change / reduce
                ball.vertical_vel = -1 * vertical_vel
main()