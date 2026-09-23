from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс для всех объектов игры.

    Хранит общие характеристики игровых объектов: их текущую
    позицию на игровом поле и цвет. Используется как родительский
    класс для яблока и змейки.
    """

    def __init__(self, position=SCREEN_CENTER,
                 body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Это Абстрактный метод.
        Для переопределения в дочерних классах
        """


class Apple(GameObject):
    """
    Хранит позицию яблока.

    Отвечает за случайное размещение яблока
    в пределах игрового поля и исключает появление на змейке.
    """

    def __init__(self, positions=None, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position(positions)

    def randomize_position(self, positions=None):
        """
        Случайное размещение яблока на игровом поле.

        Генерирует случайные координаты с учётом размеров игрового
        поля, и размера одной клетки сетки и исключает появление на змейке.
        """
        if positions is None:
            positions = []

        while True:
            position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (position_x, position_y)
            if new_position not in positions:
                self.position = new_position
                break

    def draw(self):
        """
        Отрисовка яблока.

        Создаёт квадрат размером с одну клетку в текущей
        позиции яблока и отрисовывает его вместе с границей.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Хранит координаты сегментов змейки.

    Хранит информацию о длине, текущем и следующем
    направлениях движения, а также координатах последнего удалённого
    сегмента.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        """
        Инициализирует змейку.

        Создаёт змейку длиной в один сегмент и устанавливает
        начальное направление движения вправо
        """
        super().__init__(body_color=body_color)
        self.reset()
        self.direction = RIGHT

    def update_direction(self):
        """
        Обновление направления после нажатия на кнопку.

        Применяет следующее выбранное направление и сбрасывает
        сохранённое значение после его использования.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Движение змейки.

        Перемещает змейку в текущем направлении, обновляет позиции
        сегментов и сохраняет координаты последнего удалённого
        сегмента.
        """
        head_position = self.get_head_position()
        x, y = head_position
        dx, dy = self.direction

        new_x = (x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_x, new_y)

        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """
        Отрисовка змейки.

        Рисует сегменты змейки и очищает клетку последнего
        удалённого сегмента.
        """
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.

        Головой считается первый сегмент в списке позиций змейки.
        """
        return self.positions[0]

    def reset(self):
        """
        Cброс змейки.

        Возвращает змейку в начальное состояние: длина в один сегмент,
        позиция в центре игрового поля.
        """
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш.

    Изменение направления движения змейки (было в прекоде)
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Основной игровой цикл.

    Создаёт объекты змейки и яблока, обрабатывает
    нажатия клавиш, обновляет состояние игры и отрисовывает
    объекты на экране.
    """
    pygame.init()
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        head_position = snake.get_head_position()
        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        if head_position in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
