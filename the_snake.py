"""
The Snake Game
==============
Implemented with pg.

Goal:
    Collect as many apples as you can and stay alive. Also have fun with it! :)

This version of a game contains:
- Apple: Collectable, that increases your snake`s length.
         Disappears if not collected in time (random lifetime).
- Rock: Beware! That one kills. Maybe it is radioactive or something like that.
        Amount of rocks is set by default to 3 and may be changed.
        Also disappears over time and appear in new location.
- Snake: Player-controlled, growing from apples (though it may seem unusual).
         Increasing its speed over every eaten apple.
         Dies on hitting a rock.

Controls:
    Use your keyboard arrows to set direction of a snake.


Created by Yandex.Practicum student:
    Dmitry Isarenko
    isarenko.dmitry.it@gmail.com
"""


from random import randint, randrange
import pygame as pg

# Параметры яблок(а)
APPLE_LIFE_IN_TICKS = [25, 70]
APPLE_BLINK_SPEED_IN_TICKS = 3

# Параметры камня(ей)
ROCKS_GENERATED = 3
ROCK_LIFE_IN_TICKS = [40, 150]
ROCK_BLINK_SPEED_IN_TICKS = 3

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет мигания при исчезании - белый:
BLINK_COLOR = (255, 255, 255)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет камня
ROCK_COLOR = (100, 100, 100)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
START_SPEED = 5
SPEED_STEP = 5
game_speed = START_SPEED

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """
    Base game class. Used to define fundamental attributes to all
    inheritant classes.

    Superclass:
        object (built-in)
    Subclasses:
        Apple, Rock, Snake
    """

    def __init__(self):
        self.body_color = BOARD_BACKGROUND_COLOR
        self.default_body_color = BOARD_BACKGROUND_COLOR
        self.low_life_blink_speed = 3
        self.blink_tick_count = 0
        self.position = SCREEN_CENTER_POS

    def draw(self):
        """Method is not available in superclass.
        Has to be overridden in every subclass.
        """
        raise NotImplementedError('This method should be called only in'
                                  'child classes.')

    def draw_single_dot(self, *, color, border_color, position):
        """
        Method is used for drawing an apple object on a grid.
        Color is predefined.

        args:
            None
        returns:
            None
        """
        if position and color and border_color:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, color, rect)
            pg.draw.rect(screen, border_color, rect, 1)


class LifeUpdatableMixin:
    """
    Mixin that adds lifespan to a class.
    Built-in check for having attr 'life'
    """

    def update_life(self):
        """
        Method is used to decrease 'life' counter of an object.
        - Triggers method 'blink_on_low_life' when reaching certain amount.
        - Triggers method 'reset' on reaching zero.

        args:
            None
        returns:
            None
        """
        if hasattr(self, 'life'):
            self.life -= 1
            if self.life <= 0:
                self.reset()
            elif self.life <= 20:
                self.blink_on_low_life()


class ResetableMixin:
    """
    Mixin that adds reset behaviour for a class.
    1. Fills with background color last position.
    2. Triggers reinitialization
    """

    def reset(self):
        """
        Fills last recorded position of an object with a background color
        (i.e. erases) and triggers reinitialization.

        args:
            None
        returns:
            None
        """
        # self.randomize_position()

        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        self.__init__()


class RandomizibleCoordsMixin:
    """
    Mixin that forces initialized object to appear at random location.
    Used for Apple and Rock classes.
    """

    def randomize_position(self):
        """
        Assigns a random position for an object.
        Coords stays withing the game field.

        args:
            None
        returns:
            None
        """
        rand_x = randrange(0, SCREEN_WIDTH, GRID_SIZE)
        rand_y = randrange(0, SCREEN_HEIGHT, GRID_SIZE)

        self.position = (rand_x, rand_y)


class BlinkableMixin:
    """
    Mixin that allows blinking behaviour.
    Applies to Apple and Rock classes.
    """

    def blink_on_low_life(self):
        """
        Adds blinks for a rock object on trigger. Each iteration switches
        color from default rock color to predefined blinking color.

        args:
            None
        returns:
            None
        """
        if self.blink_tick_count == self.low_life_blink_speed:
            self.body_color = self.default_body_color
            self.draw()
            self.blink_tick_count = 0
        elif self.blink_tick_count % 2 == 0:
            self.blink_tick_count += 1
            self.body_color = self.default_body_color
        else:
            self.blink_tick_count += 1
            self.body_color = BLINK_COLOR


# class DrawableMixin:
#     """
#     Mixin that defines common to Rock and Apple drawing behaviour.
#     Mixin created to follow DRY convention.
#     """

#     def draw_single_dot(self, screen):
#         """
#         Method is used for drawing an apple object on a grid.
#         Color is predefined.

#         args:
#             None
#         returns:
#             None
#         """
#         rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#         pg.draw.rect(screen, self.body_color, rect)
#         pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(
    GameObject,
    LifeUpdatableMixin,
    ResetableMixin,
    RandomizibleCoordsMixin,
    BlinkableMixin,
    # DrawableMixin
):
    """
    Class that describes an apple in game.
    - Apple has a random lifetime and disappears if hasn`t been picked up.
    - Blinks on final lifespan phase.

    Picking up:
    - increases the snake`s length by 1 segment.
    - increases the snake`s speed by fixed amount.
    - generates a new apple at a random location.

    Superclass:
        GameObject
    Subclasses:
        Rock
    """

    def __init__(self):
        super().__init__()
        self.randomize_position()
        self.life = randint(APPLE_LIFE_IN_TICKS[0], APPLE_LIFE_IN_TICKS[1])
        self.body_color = APPLE_COLOR
        self.default_body_color = APPLE_COLOR
        self.border_color = BORDER_COLOR
        self.low_life_blink_speed = APPLE_BLINK_SPEED_IN_TICKS

    def draw(self):
        self.draw_single_dot(
            position=self.position,
            color=self.body_color,
            border_color=self.border_color
        )


class Rock(
    GameObject,
    LifeUpdatableMixin,
    ResetableMixin,
    RandomizibleCoordsMixin,
    BlinkableMixin,
    # DrawableMixin
):
    """
    Class that describes a rock in game.
    - Rock has a random lifetime and disappears over time.
    - Blinks on final lifespan phase.

    Hitting rock:
    - kills your snake instantly.
    - decreases snake`s length to 1.
    - decreases snake`s speed to default speed.

    Superclass:
        Apple
    Subclasses:
        None
    """

    def __init__(self):
        super().__init__()
        self.body_color = ROCK_COLOR
        self.randomize_position()
        self.life = randint(ROCK_LIFE_IN_TICKS[0], ROCK_LIFE_IN_TICKS[1])
        self.body_color = ROCK_COLOR
        self.default_body_color = ROCK_COLOR
        self.border_color = BORDER_COLOR
        self.low_life_blink_speed = ROCK_BLINK_SPEED_IN_TICKS

    def draw(self):
        self.draw_single_dot(
            position=self.position,
            color=self.body_color,
            border_color=self.border_color
        )


class Snake(GameObject):
    """
    Class that describes a snake in game.
    -  Starting direction: right.
    -  Starting length: 1.
    -  Moves in discrete steps on grid. Controlled by keyboard arrows.
    -  Grows by consuming apples.
    -  Dies upon hitting itself or any rock.

    Superclass:
        GameObject
    Subclasses:
        None
    """

    def __init__(self):
        super().__init__()
        self.has_eaten = False
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.position = SCREEN_CENTER_POS
        self.positions = [self.position]
        self.last = None

    def get_head_position(self):
        """
        Returns position of the snake`s head.

        args:
            None
        returns:
            tuple: (x, y)
        """
        return self.positions[0]

    def reset(self):
        """
        Resets game.

        args:
            None
        returns:
            None
        """
        global game_speed
        game_speed = START_SPEED
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.position = SCREEN_CENTER_POS
        self.direction = RIGHT
        self.length = 1
        self.next_direction = None
        self.positions = [self.position]

    def draw(self):
        """
        Draws head and body of a snake. Clears tail trail on movement.

        args:
            None
        returns:
            None
        """
        # for position in self.positions[:-1]:
        #     rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        #     pg.draw.rect(screen, self.body_color, rect)
        #     pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """
        Implementation of 'movement' of a snake:
        1. add head to heading direction
        2. cut the tail segment if haven`t recently eaten an apple

        Warping over game field edges.

        args:
            None
        returns:
            None
        """
        current_x, current_y = self.get_head_position()
        direction_x, direction_y = self.direction
        next_x = current_x + GRID_SIZE * direction_x
        next_y = current_y + GRID_SIZE * direction_y

        if next_x > SCREEN_WIDTH - GRID_SIZE:
            next_x = 0
        elif next_x < 0:
            next_x = SCREEN_WIDTH - GRID_SIZE

        if next_y > SCREEN_HEIGHT - GRID_SIZE:
            next_y = 0
        elif next_y < 0:
            next_y = SCREEN_HEIGHT - GRID_SIZE

        self.positions.insert(0, ((next_x), (next_y)))

        if self.has_eaten:
            self.has_eaten = False
            self.length += 1
            self.update_speed()
        else:
            self.last = self.positions.pop(-1)

        self.position = self.positions[0]

        self.draw()

    def check_collision(self, game_object):
        """
        Check collisions with game objects:
        - Apple: triggers growth
        - Rock: triggers death
        - Snake: (hit yourself) triggers death

        args:
            game_object (GameObject): The object to check collision against.
        returns:
            None
        """
        if isinstance(game_object, Rock):
            if game_object.position == self.position:
                self.reset()

        if isinstance(game_object, Apple):
            if game_object.position == self.position:
                self.has_eaten = True
                game_object.reset()

        if isinstance(game_object, Snake):
            if any(self.position == pos for pos in self.positions[1::]):
                self.reset()

    def update_direction(self):
        """
        Rewrites movement direction if another one was set.

        args:
            None
        returns:
            None
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def update_speed(self):
        """
        Increases speed on call. Typically used in eating an apple condition.

        args:
            None
        returns:
            None
        """
        global game_speed
        game_speed += SPEED_STEP
        # self.speed += SPEED_STEP


def handle_keys(game_object: Snake):
    """
    Used to handle keyboard inputs (arrow keys) and 'close window' event.

    Allows to steer a snake over field and exit game by closing a window.

    args:
        object (Snake): The snake obj, that should be controlled.
    returns:
        None
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Initializes and runs the main game loop.

    Handles object rendering, movement, input processing,
    collision detection, and frame timing.

    args:
        None
    returns:
        None
    """
    pg.init()

    snake = Snake()
    apple = Apple()
    rocks = [Rock() for _ in range(ROCKS_GENERATED)]

    snake.draw()

    while True:
        apple.draw()
        for rock in rocks:
            rock.draw()

        apple.update_life()
        for rock in rocks:
            rock.update_life()

        snake.check_collision(apple)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        snake.check_collision(snake)
        for rock in rocks:
            snake.check_collision(rock)

        clock.tick(game_speed)
        pg.display.update()


if __name__ == '__main__':
    main()
