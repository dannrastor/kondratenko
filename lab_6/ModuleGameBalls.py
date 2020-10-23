import random
import pygame
import math


class GameHandler:
    def __init__(self):
        """
        Создание констант игры, заготовок изображений и объектов игры.
        """
        self.FPS = 30
        self.screen_height = 1000
        self.screen_width = 1000
        self.level = 1
        self.max_quantity = 10
        self.spawn_time = 1000
        self.time_of_prev_spawn = 0
        self.direction = 360
        self.speed_max = 10
        self.speed_min = 2
        self.radius_min = 20
        self.radius_max = 40
        self.rotationalspeed = 15
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)
        self.MAGENTA = (255, 0, 255)
        self.CYAN = (0, 255, 255)
        self.BLACK = (0, 0, 1)
        self.WHITE = (255, 255, 255)
        self.score = 0
        self.COLORS = [self.RED, self.BLUE, self.YELLOW, self.GREEN,
                       self.MAGENTA, self.CYAN, self.WHITE]
        self.start = True
        self.end = False
        self.pause = False
        self.frog = False
        self.frog_killed = False
        self.finished = False
        self.time_pause = 0
        self.pool = []
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.screen_height,
                                               self.screen_width))
        self.faketarget_origin = pygame.image.load("FakeTarget.png", "RGBA")
        self.faketarget_origin = pygame.transform.scale(self.faketarget_origin,
                                                        (2 * self.radius_max,
                                                         2 * self.radius_max))
        self.deadfaketarget_origin = pygame.image.load("DeadFakeTarget.png",
                                                       "RGBA")
        self.deadfaketarget_origin \
            = pygame.transform.scale(self.deadfaketarget_origin,
                                     (2 * self.radius_max,
                                      2 * self.radius_max))
        self.Lygushka = pygame.image.load('Lygushka.jpg', "RGB")
        self.LygushkaRect = self.Lygushka.get_rect()
        self.LygushkaRect.center = (self.screen_width // 2,
                                    self.screen_height // 2)
        self.surface_end = pygame.image.load('ENDGAME.png')
        self.endRect = self.surface_end.get_rect()
        self.endRect.center = (self.screen_width // 2,
                               self.screen_height // 2)
        self.end_width, self.end_height = self.surface_end.get_size()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.start_text = self.font.render("Вы готовы? Показывайте,"
                                           " что у вас там",
                                           True, self.WHITE, self.BLACK)
        self.start_textRect = self.start_text.get_rect()
        self.start_textRect.center = (self.screen_width // 2,
                                      self.screen_height // 10 * 9)
        self.end_text = self.font.render("Ну вам уд 4, идите", True,
                                         self.WHITE, self.BLACK)
        self.end_textRect = self.end_text.get_rect()
        self.end_textRect.center = (self.screen_width // 2,
                                    self.screen_height // 10 * 9)
        self.faster_text = self.font.render("А можно побыстрее?", True,
                                            self.WHITE, self.BLACK)
        self.faster_textRect = self.end_text.get_rect()
        self.faster_textRect.center = (self.screen_width // 2,
                                       self.screen_height // 10 * 9)
        self.clock = pygame.time.Clock()

    def cheackscore(self):
        if self.score >= 2:
            self.score = 0
            self.pool.clear
            return True
        else:
            return False

class BaseTarget(GameHandler):
    """
    Класс - содержащий общие методы для всех "игровых целей на экране"
    """
    def __init__(self):
        """
        Основные параметры: x, y - координаты, velocity - список содержащий
        скорость и направление скорости (ввиде угла в градусах отсчитанного
        против часовой от горизонтали). Color - цвет объекта.
        """
        super().__init__()
        self.x = random.randint(self.screen_width * 0.15 + self.radius_max,
                                self.screen_width * 0.85 - self.radius_max)
        self.y = random.randint(self.screen_height * 0.15 + self.radius_max,
                                self.screen_height * 0.85 - self.radius_max)
        self.velocity = [random.randint(self.speed_min, self.level * self.speed_max),
                         random.randint(0, self.direction)]
        self.color = self.COLORS[random.randint(0, 6)]

    def move_xy(self):
        """
        Отвечает за измененине координат.
        """
        if self.x >= self.screen_width * 0.85 or self.x <= self.screen_width * 0.15:
            self.velocity[1] = 180 - self.velocity[1]
        elif self.y >= self.screen_height * 0.85 or self.y <= self.screen_height * 0.15:
            self.velocity[1] *= -1
        self.x = self.x + int(self.velocity[0]
                              * math.cos(math.pi * self.velocity[1] / 180))
        self.y = self.y - int(self.velocity[0]
                              * math.sin(math.pi * self.velocity[1] / 180))


class Ball(BaseTarget):
    """
    Первый тип игровой цели - шарик, за попадание в него получаешь 1 очко.
    """
    def __init__(self):
        """
        Параметры наследумеые из класса BaseTarget и инициализация параметра
        радиус отвечаещего за радиус круга, символизирующего шарик.
        """
        super().__init__()
        self.radius = random.randint(self.radius_min, self.radius_max)

    def draw(self):
        """
        Функция рисует на игровом экране объект.
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def kill(self):
        """
        Закрашивает объект черным цветом.
        """
        pygame.draw.circle(self.screen, self.BLACK, (self.x, self.y), self.radius)

    def move(self):
        """
        Отвечает за передвижение объекта.
        """
        self.kill()
        self.move_xy()
        self.draw()

    def check(self, x, y):
        """
        Проверка попадания. x, y - координаты точки проверки.
        """
        if (self.x - x) ** 2 + (self.y - y) ** 2 <= self.radius ** 2:
            return True
        else:
            return False


class FakeTarget(BaseTarget):
    """
    Второй тип игровой цели. Лягушка, за нажатие на неё теряешь 3 очка
    (меньше 0 нельзя). Так же при попадание в лягушку на экран ненадолго
    выводится картинка лягушки.
    """
    def __init__(self):
        """
        Параметры наследумеые из класса BaseTarget и инициализация параметров:
        rotationalspeed - скорость поворота, две поверхности
        (лягушка и черный квадрат для закрашивания лягушки), а так же параметры
        этих двух поверхностей, rotaterecord = счетчик для регулировки поворота
        """
        super().__init__()
        self.surface_FakeTarget = self.faketarget_origin.copy()
        self.surface_DeadFakeTarget = self.deadfaketarget_origin.copy()
        self.FakeTargetRect = self.surface_FakeTarget.get_rect()
        self.DeadFakeTargetRect = self.surface_DeadFakeTarget.get_rect()
        self.FakeTargetRect.center = (self.x, self.y)
        self.DeadFakeTargetRect.center = (self.x, self.y)
        self.rotaterecord = 0

    def draw(self):
        """
        Функция рисует на игровом экране объект.
        """
        self.screen.blit(self.surface_FakeTarget, self.FakeTargetRect)

    def kill(self):
        """
        Закрашивает объект черным цветом.
        """
        self.screen.blit(self.surface_DeadFakeTarget, self.DeadFakeTargetRect)

    def move(self):
        """
        Отвечает за передвижение объекта.
        """
        self.kill()
        self.move_xy()
        self.FakeTargetRect.center = (self.x, self.y)
        self.DeadFakeTargetRect.center = (self.x, self.y)
        if self.rotaterecord == 3:
            self.surface_FakeTarget = \
                pygame.transform.rotate(self.surface_FakeTarget,
                                        90)
            self.surface_DeadFakeTarget = \
                pygame.transform.rotate(self.surface_DeadFakeTarget,
                                        90)
            self.rotaterecord = 0
        else:
            self.rotaterecord += 1
        self.draw()

    def check(self, x: int, y: int):
        """
        Проверка попадания. x, y - координаты точки проверки.
        """
        if (self.x - x) ** 2 + (self.y - y) ** 2 <= (self.radius_max ** 2) * 2:
            if self.screen.get_at((x, y)) == ((0, 0, 0) or (244, 67, 54)
                                         or (139, 195, 74) or (205, 220, 57)
                                         or (255, 224, 189) or (0, 188, 212)):
                return True
            else:
                return False
        else:
            return False
