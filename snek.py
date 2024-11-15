import random
import sys

import pygame

SCREEN_WIDTH = 768
SCREEN_HEIGHT = 768

GRIDSIZE = 32
GRID_WIDTH = int(SCREEN_HEIGHT / GRIDSIZE)
GRID_HEIGHT = int(SCREEN_WIDTH / GRIDSIZE)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snek:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.bodyColor = (50, 243, 250)
        self.borderColor = (55, 247, 255)
        self.score = 0
        self.highScore = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (
            ((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH),
            (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT,
        )
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):  # snek die
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        if self.score > self.highScore:
            self.highScore = self.score
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.bodyColor, r)
            pygame.draw.rect(surface, self.borderColor, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_UP
                    or event.key == pygame.K_w
                    or event.key == pygame.K_k
                ):
                    self.turn(UP)  # all da way
                elif (
                    event.key == pygame.K_DOWN
                    or event.key == pygame.K_s
                    or event.key == pygame.K_j
                ):
                    self.turn(DOWN)  # for what?
                elif (
                    event.key == pygame.K_LEFT
                    or event.key == pygame.K_a
                    or event.key == pygame.K_h
                ):
                    self.turn(LEFT)
                elif (
                    event.key == pygame.K_RIGHT
                    or event.key == pygame.K_d
                    or event.key == pygame.K_l
                ):
                    self.turn(RIGHT)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.bodyColor = (230, 38, 250)
        self.borderColor = (235, 43, 255)
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRIDSIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
        )

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.bodyColor, r)
        pygame.draw.rect(surface, self.borderColor, r, 1)


def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (10, 10, 10), r)
                pygame.draw.rect(surface, (15, 15, 15), r, 1)
            else:
                rr = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (10, 10, 10), rr)
                pygame.draw.rect(surface, (15, 15, 15), rr, 1)


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("snek")

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snek = Snek()
    food = Food()

    fontSize = 18
    scoreFont = pygame.font.SysFont("monospace", fontSize)
    scoreColor = (255, 255, 255)
    scoreMarginLeft = 5
    highScoreMarginTop = 10
    scoreMarginTop = fontSize + (highScoreMarginTop * 2)

    while True:
        clock.tick(10)
        snek.handle_keys()
        drawGrid(surface)
        snek.move()
        if snek.get_head_position() == food.position:
            snek.length += 1
            snek.score += 1
            food.randomize_position()
        snek.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))

        # scoreboard
        score = scoreFont.render("Score {0}".format(snek.score), 1, scoreColor)
        highScore = scoreFont.render(
            "High Score {0}".format(snek.highScore), 1, scoreColor
        )
        screen.blit(highScore, (scoreMarginLeft, highScoreMarginTop))
        screen.blit(score, (scoreMarginLeft, scoreMarginTop))

        pygame.display.update()


main()
