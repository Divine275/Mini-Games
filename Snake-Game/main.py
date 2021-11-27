import time
import random
import pygame
from pygame.locals import *

SIZE = 20
BACKGROUND_COLOR = (15, 133, 74)

class Food:
    def __init__(self, parent_screen):
        self.food = pygame.image.load("Util/bait.png").convert()
        self.parent_screen = parent_screen
        self.x = random.randint(8, 12)*SIZE
        self.y = random.randint(17, 23)*SIZE

    def draw(self):
        self.parent_screen.blit(self.food, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 13)*SIZE
        self.y = random.randint(0, 8)*SIZE


class Snake:
    def __init__(self, parent_screen, length = 1):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("Util/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'right'

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def crawl(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

class Game:
    def __init__(self):
        # initialising module
        pygame.init() 
        pygame.mixer.init()

        pygame.display.set_caption(f"Snake Game")
        self.play_bg_music()

        self.surface = pygame.display.set_mode((800, 500))
        self.surface.fill(BACKGROUND_COLOR)

        self.snake = Snake(self.surface)
        self.snake.draw()
        
        self.food = Food(self.surface)
        self.food.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x2 + SIZE > x1:
            if y1 >= y2 and y2 + SIZE > y1:
                return True

        return False

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"Util/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play_bg_music(self):
        pygame.mixer.music.load("Util/bg_music.mp3")
        pygame.mixer.music.play()

    def render_bg(self, img):
        bg = pygame.image.load(f"Util/{img}.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_bg("bg")
        self.snake.crawl()
        self.food.draw()
        self.display_score()
        pygame.display.flip()

        # collision of snake and apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.food.move()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over"
                
    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Food(self.surface)

    def display_score(self):
        font = pygame.font.SysFont('arial', 30, bold=True)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (650, 8))

    def show_game_over(self):
        self.render_bg("gameover")
        game_over_font = pygame.font.SysFont('arial', 35 , bold = True)
        normal_font = pygame.font.SysFont('arial', 20 , italic=True)

        line1 = game_over_font.render(f"Game over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 200))

        line2 = normal_font.render(f"To quit press Escape. To play again press Enter", True, (255, 255, 255))
        self.surface.blit(line2, (200, 250))

        pygame.display.flip()
        pygame.mixer.music.pause()

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pause = False
                        self.reset()
                        pygame.mixer.music.unpause()
                    
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False 

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
            time.sleep(0.3)


if __name__ == "__main__":
    game = Game()
    game.run()
    