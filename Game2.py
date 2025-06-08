import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (80, 175, 90)
BLUE = (60, 160, 200)

WIDTH = 700
HEIGHT = 700
FPS = 60

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")
clock = pygame.time.Clock()


class Paddle:
    def __init__(self):
        self.width = int(WIDTH / 10)
        self.height = 20
        self.x = int(WIDTH / 2) - int(self.width / 2)
        self.y = HEIGHT - 40
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_paddle(self):
        pygame.draw.rect(win, WHITE, self.rect)

    def move_paddle(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if key[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed


class Ball:
    def __init__(self, x, y, speed=3):
        self.radius = 10
        self.x = x - self.radius
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.dx = speed
        self.dy = -speed
        self.game_status = 0

    def draw_ball(self):
        pygame.draw.circle(win, BLUE, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

    def move_ball(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.right > WIDTH or self.rect.left < 0:
            self.dx *= -1
        if self.rect.top < 0:
            self.dy *= -1
        if self.rect.bottom > HEIGHT:
            self.game_status = -1

        if self.rect.colliderect(paddle.rect) and self.dy > 0:
            self.dy *= -1

        all_done = True
        row_num = 0
        for row in brick_wall.bricks:
            col_num = 0
            for br in row:
                if br != (0, 0, 0, 0) and self.rect.colliderect(br):
                    if abs(self.rect.bottom - br.top) < abs(self.dy) and self.dy > 0:
                        self.dy *= -1
                    elif abs(self.rect.top - br.bottom) < abs(self.dy) and self.dy < 0:
                        self.dy *= -1
                    elif abs(self.rect.right - br.left) < abs(self.dx) and self.dx > 0:
                        self.dx *= -1
                    elif abs(self.rect.left - br.right) < abs(self.dx) and self.dx < 0:
                        self.dx *= -1
                    brick_wall.bricks[row_num][col_num] = (0, 0, 0, 0)
                if brick_wall.bricks[row_num][col_num] != (0, 0, 0, 0):
                    all_done = False
                col_num += 1
            row_num += 1
        if all_done:
            self.game_status = 1

        return self.game_status


class Brick:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.width = int(WIDTH / self.cols)
        self.height = 50

    def create_bricks(self):
        self.bricks = []
        for row in range(self.rows):
            bricks_row = []
            for col in range(self.cols):
                brick_x = col * self.width
                brick_y = row * self.height
                br = pygame.Rect(brick_x, brick_y, self.width, self.height)
                bricks_row.append(br)
            self.bricks.append(bricks_row)

    def draw_bricks(self):
        for row in self.bricks:
            for br in row:
                pygame.draw.rect(win, GREEN, br)
                pygame.draw.rect(win, BLACK, br, 2)


def reset_game(level):
    global paddle, ball, brick_wall
    paddle = Paddle()
    ball = Ball(paddle.x + int(paddle.width / 2), paddle.y - 10, speed=3 + level)
    brick_wall = Brick(cols=10 + level, rows=6 + level)
    brick_wall.create_bricks()


level = 0
reset_game(level)

run = True
game_over = False

while run:
    clock.tick(FPS)
    win.fill(BLACK)

    if not game_over:
        paddle.draw_paddle()
        paddle.move_paddle()
        ball.draw_ball()
        brick_wall.draw_bricks()
        game_status = ball.move_ball()

        if game_status == -1:
            game_over = True
        elif game_status == 1:
            level += 1
            reset_game(level)

    if game_over:
        font = pygame.font.SysFont(None, 50)
        text = font.render("GAME OVER. Press R to Restart", True, BLUE)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        win.blit(text, text_rect)

    if game_status == 1 and not game_over:
        font = pygame.font.SysFont(None, 50)
        text = font.render(f"Level {level + 1}", True, BLUE)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        win.blit(text, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                level = 0
                reset_game(level)
                game_over = False

    pygame.display.update()

pygame.quit()
