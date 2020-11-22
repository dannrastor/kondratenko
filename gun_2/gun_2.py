import pygame
import numpy
from random import randint

pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 204, 204)
screen_size = (800, 800)
"""
Цвета используемые в программе, и размер игрового экрана
"""



def rand_color():
    """
    Функция возвращает случайный цвет
    """
    color = (randint(20, 180), randint(20, 180), randint(20, 180))
    return color


class Bullet:
    """
    Класс пуль - отвечает за объекты для стрельбы из пушки
    """
    def __init__(self, coord, velocity, angle, color, r=20, g=-1):
        """
        Создание объекта класса Bullet
        :param coord: list; список x, y: int;
        отвечает за положение пули на экране
        :param velocity: int; отвечает за модуль вектора скорости пули
        :param angle: int; значение угла между осью икс и вектором скорости
        в градусах
        :param color: список из r, g, b: int; отвечает за цвет пули в RGB
        :param r: int; радиус круга пули
        :param g: int; значение ускорения свободного падения
        """
        self.coord = coord
        color = color
        self.color = color
        self.V = [velocity * numpy.cos(angle),
                  velocity * numpy.sin(angle)]
        self.g = g
        self.r = r
        self.life = True

    def reflection(self, refl_k=0.8):
        """
        Проверка на столкновение со стеной
        :param refl_k: float; отвечает за потерю энергии при столкновении
        """
        for i in range(2):
            if self.coord[i] >= screen_size[i] - self.r:
                self.coord[i] = screen_size[i] - self.r
                self.V[i] *= -refl_k
                self.V[1 - i] *= refl_k ** 0.1
            elif self.coord[i] <= self.r:
                self.coord[i] = self.r
                self.V[i] *= -refl_k
                self.V[1 - i] *= refl_k ** 0.1
            self.V[i] = int(self.V[i])

    def move(self):
        """
        Перемещает пулю в зависимости от скорости
        """
        self.V[1] -= self.g
        for i in range(2):
            self.coord[i] += self.V[i]
            self.coord[i] = int(self.coord[i])
        self.reflection()
        if self.V[0] ** 2 + self.V[1] ** 2 <= 1 ** 2:
            self.life = False

    def draw(self, screen):
        """
        Рисует пулю на заданном экране
        :param screen: pygame.Surface; игровой экран
        """
        pygame.draw.circle(screen, self.color, self.coord, self.r)


class Gun:
    """
    Класс пушки - отвечает за работу пушки
    """
    def __init__(self, coord=[screen_size[0] // 2, screen_size[1] - 20],
                 charge=5, angle=0, max_power=50, min_power=0,
                 color=RED, back_color=WHITE, velocity=10, r=20):
        """
        Создание объекта класса Gun
        :param coord: list; список x, y: int; отвечает за положение пушки
        :param charge: int; шаг увеличения силы выстрела
        :param angle: int; угол между направлением пушки и осью икс в градусах
        :param max_power: int; максимальное значение силы выстрела
        :param min_power: int; минамальное (начальное) значение силы выстрела
        :param color: list; список из r, g, b: int; цвет ствола пушки в RGB
        :param back_color: list; список из r, g, b: int;
        цвет ствола пушки в RGB
        :param velocity: int; модуль скорости пушки
        :param r: int; радиус корпуса пушки
        """
        self.coord = coord
        self.angle = angle
        self.max_power = max_power
        self.min_power = min_power
        self.color = color
        self.back_color = back_color
        self.active = False
        self.power = min_power
        self.charge = charge
        self.r = r
        self.start_coord = coord
        self.velocity = velocity

    def activate(self):
        """
        Активирует пушку, дает возможность стрелять
        """
        self.active = True

    def set_angle(self, target_pos):
        """

        :param target_pos: list; список x, y : int; координаты курсора мышки
        """
        self.angle = numpy.arctan2(target_pos[1] - self.coord[1],
                                   target_pos[0] - self.coord[0])

    def charging(self):
        """
        Увеличивает силу выстрела
        """
        if self.active and self.power < self.max_power:
            self.power += self.charge

    def alt_fire(self):
        """
        Первый вариант выстрела - пушка остается на меесте, вылетает
        красная пуля
        """
        coord, power, angle = self.coord.copy(), self.power, self.angle
        bullet = Bullet(coord, power, angle, RED)
        self.power = self.min_power
        self.active = False
        return bullet

    def fire(self):
        """
        Второй вариант выстрела - пушка перемещается вместе, с пулей
        белого цвета
        """
        bullet = Bullet(self.coord, self.power, self.angle, WHITE)
        self.power = self.min_power
        self.active = False
        return bullet

    def move_x(self, direction):
        """
        Передвигает пушку вдоль оси x
        :param direction: int; направление передвижения пушкик: +1 - вдоль оси,
        -1 - против оси
        """

        if (self.coord[1] > 30 or inc > 0) \
                and (self.coord[0] < screen_size[0] - 30 or inc < 0):
            self.coord[0] += self.velocity

    def move_y(self, direction):
        """
        Передвигает пушку вдоль оси y
        :param direction: int; направление передвижения пушкик: +1 - вдоль оси,
        -1 - против оси
        """
        if (self.coord[1] > 30 or inc > 0) \
                and (self.coord[1] < screen_size[1] - 30 or inc < 0):
            self.coord[1] += self.velocity * direction

    def draw(self, screen):
        """
        Рисует пушку на щаданном экране
        :param screen: pygame.Surface; игровой экран
        """
        gun_shape = []
        vec_1 = numpy.array([int(5 * numpy.cos(self.angle - numpy.pi / 2)),
                            int(5 * numpy.sin(self.angle - numpy.pi / 2))])
        vec_2 = numpy.array([int(self.power * numpy.cos(self.angle)),
                            int(self.power * numpy.sin(self.angle))])
        gun_pos = numpy.array(self.coord)
        gun_shape.append((gun_pos + vec_1).tolist())
        gun_shape.append((gun_pos + vec_1 + vec_2).tolist())
        gun_shape.append((gun_pos + vec_2 - vec_1).tolist())
        gun_shape.append((gun_pos - vec_1).tolist())
        pygame.draw.polygon(screen, self.color, gun_shape)
        pygame.draw.circle(screen, self.back_color, self.coord, self.r)


class Target_1:
    """
    Класс, отвечающий за создание целей первого типа
    """
    def __init__(self, coord=None, color=None, r=30):
        """
        Создает объект класс Target_1
        :param coord: list; лист x, y: int; отвечает за координаты цели
        :param color: list; список r, g, b: int; цвет цели в RGB
        :param r: int; радиус цели
        """
        if coord == None:
            coord = [randint(r, screen_size[0] - r),
                     randint(r, screen_size[1] - r)]
        self.coord = coord
        self.r = r
        self.v = [randint(-7, +7), randint(-7, +7)]
        self.counter = 0

        if color == None:
            color = rand_color()
        self.color = color

    def check(self, ball):
        """
        Проверяет столкновение пули (ball) и цели
        :param ball: Bullet; пуля, столкновение с которой проверют
        """
        dist = 0
        for i in range(2):
            dist += (self.coord[i] - ball.coord[i]) ** 2
        dist **= 0.5
        min_dist = self.r + ball.r
        return dist <= min_dist

    def draw(self, screen):
        """
        Рисует на заданном экране цель
        :param screen: pygame.Surface; игровой экран
        """
        pygame.draw.circle(screen, self.color, self.coord, self.r)

    def reflection(self):
        """
        Проверяет столкновения со стенами и в случае столкновения отражает
        """
        for i in range(2):
            if self.coord[i] > screen_size[i] - self.r or \
                    self.coord[i] < self.r:
                self.v[i] = -self.v[i]

    def move(self):
        """
        Двигает цель, в соответствии со значениями скорости
        """
        self.reflection()
        self.coord[1] += self.v[1]
        self.coord[0] += self.v[0]


class Target_2:
    """
    Класс, отвечающий за создание целей второго типа
    """
    def __init__(self, coord=None, color=None, r=100):
        """
        Создает объект класс Target_1
        :param coord: list; лист x, y: int; отвечает за координаты цели
        :param color: list; список r, g, b: int; цвет цели в RGB
        :param r: int; сторона квадрата цели
        """
        if coord == None:
            coord = [randint(r, screen_size[0] - r),
                     randint(r, screen_size[1] - r)]
        self.coord = coord
        self.r = r
        self.v = [randint(-7, +7), randint(-7, +7)]
        self.counter = 0

        if color == None:
            color = rand_color()
        self.color = color

    def check(self, ball):
        """
        Проверяет столкновение пули (ball) и цели
        :param ball: Bullet; пуля, столкновение с которой проверют
        """
        dist = 0
        for i in range(2):
            dist += (self.coord[i] - ball.coord[i]) ** 2
        dist **= 0.5
        min_dist = self.r + ball.r
        return dist <= min_dist

    def draw(self, screen):
        """
        Рисует на заданном экране цель
        :param screen: pygame.Surface; игровой экран
        """
        pygame.draw.rect(screen, self.color, [self.coord[0], self.coord[1],
                                              self.r, self.r])

    def reflection(self):
        """
        Проверяет столкновения со стенами и в случае столкновения отражает
        """
        for i in range(2):
            if self.coord[i] > screen_size[i] - self.r:
                self.coord[i] = self.r
            elif self.coord[i] < self.r:
                self.coord[i] = screen_size[i] - self.r

    def move(self):
        """
        Двигает цель, в соответствии со значениями скорости; раз в 40 отсчетов
        скорость сслучайно меняет направление не меняя модуля.
        """
        self.reflection()
        if self.counter >= 40:
            self.counter = 0
            angel = randint(0, 360)
            vel = (self.v[0] ** 2 + self.v[1] ** 2) ** 0.5
            self.v[0] = vel * numpy.cos(numpy.pi * angel / 360)
            self.v[1] = vel * numpy.sin(numpy.pi * angel / 360)
        self.coord[1] += self.v[0]
        self.coord[0] += self.v[1]
        self.counter += 1


class ScoreTable:
    """
    Класс, отвечающий за табличку счета
    """
    def __init__(self, t_destr=0, b_used=0):
        """
        Создает объект класса ScoreTable
        :param t_destr: int; колчиество уничтоженных целей
        :param b_used: int; количество выстрелов
        """
        self.t_destr = t_destr
        self.b_used = b_used
        self.font = pygame.font.SysFont("arial", 30)

    def score(self):
        """
        Подсчитывает значение очков, набранных в игре
        """
        return self.t_destr * 2 - self.b_used

    def draw(self, screen):
        """
        Рисует табличку с счетом на заданном экране
        :param screen: pygame.Surface; игровой экран
        """
        score_surf = []
        score_surf.append(
            self.font.render("Balls used: {}".format(self.b_used),
                             True, WHITE))
        score_surf.append(self.font.render("Total: {}".format(self.score()),
                                           True, WHITE))
        for i in range(2):
            screen.blit(score_surf[i], [10, 10 + 30 * i])


class GameManager:
    """
    Класс, отвечающий за управеление игровыми процессами
    """
    def __init__(self, n_targets):
        """
        Создает обеъект класса GameManager
        :param n_targets: количество целей каждого вида
        """
        self.balls = []
        self.gun = Gun()
        self.targets = []
        self.score_t = ScoreTable()
        self.n_targets = n_targets
        self.new_mission()

    def new_mission(self):
        """
        Функцияс, отвечающия за начало каждой игры
        """
        for i in range(self.n_targets):
            self.targets.append(Target_1(
                r=randint(max(1, 30 - 2 * max(0, self.score_t.score())),
                          30 - max(0, self.score_t.score()))))
        for i in range(self.n_targets):
            self.targets.append(Target_2(
                r=randint(max(1, 50 - 2 * max(0, self.score_t.score())),
                          50 - max(0, self.score_t.score()))))

    def process(self, events, screen):
        """
        Направляет пушку, двигает все объекты, проверяет столкновения, рисует
        все объекты; если все цели уничтожены запускаетновую игру
        :param events: pygame.event; событие игры для обработки
        :param screen: pygame.Surface; игровой экран
        """

        done = self.handle_events(events)

        if pygame.mouse.get_focused():
            mouse_pos = pygame.mouse.get_pos()
            self.gun.set_angle(mouse_pos)

        self.move()
        self.check()
        self.draw(screen)

        if len(self.targets) == 0 and len(self.balls) == 0:
            self.new_mission()

        return done

    def handle_events(self,
                      events):
        """
        Обработка всех игровых событий
        :param events: список игровых событий pygame.event
        """
        done = False
        for event in events:
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.gun.move_y(-1)
                elif event.key == pygame.K_DOWN:
                    self.gun.move_y(1)
                elif event.key == pygame.K_LEFT:
                    self.gun.move_x(-1)
                elif event.key == pygame.K_rIGHT:
                    self.gun.move_x(1)
                elif event.key == pygame.K_SPACE:
                    self.balls.append(self.gun.alt_fire())
                    self.score_t.b_used += 1
                    self.gun.activate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == 1 and len(self.balls) == 0):
                    activator = True
                    for ball in self.balls:
                        if ball.life:
                            activator = False
                    if activator:
                        self.gun.activate()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.gun.active:
                    self.balls.append(self.gun.fire())
                    self.score_t.b_used += 1
        return done

    def draw(self, screen):
        """
        Отрисовывает все объекты в игре
        :param screen: pygame.Surface; игровой экран
        """
        for ball in self.balls:
            ball.draw(screen)
        for target in self.targets:
            target.draw(screen)
        self.gun.draw(screen)
        self.score_t.draw(screen)

    def move(self):
        """
        Двигает все объекты в игре
        """
        for i, ball in enumerate(self.balls):
            ball.move()
            if not ball.life:
                self.balls.pop(i)
        for i, target in enumerate(self.targets):
            target.move()
        self.gun.charging()

    def check(self):
        """
        Проверяет столкнование пуль с объектами
        """
        for i, ball in enumerate(self.balls):
            for j, target in enumerate(self.targets):
                if target.check(ball):
                    self.score_t.t_destr += 1
                    self.targets.pop(j)


screen = pygame.display.set_mode(screen_size)

done = False
clock = pygame.time.Clock()

gm = GameManager(n_targets=3)
FPS = 30

while not done:
    clock.tick(FPS)
    screen.fill(BLUE)

    done = gm.process(pygame.event.get(), screen)

    pygame.display.update()

pygame.quit()
