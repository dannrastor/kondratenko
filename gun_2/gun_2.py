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

def rand_color():
    return (randint(20, 200), randint(20, 200), randint(20, 200))



class Bullet:

    def __init__(self, coord, velocity, angle, R = 20, g=-1, color=RED):
        self.coord = coord
        color = RED
        self.color = color
        self.V = [velocity * numpy.cos(angle),
                  velocity * numpy.sin(angle)]
        self.g = g
        self.R = R
        self.life = True

    def reflection(self, refl_k=0.8):
        for i in range(2):
            if self.coord[i] >= screen_size[i] - self.R:
                self.coord[i] = screen_size[i] - self.R
                self.V[i] *= -refl_k
                self.V[1-i] *= refl_k ** 0.1
            elif self.coord[i] <= self.R:
                self.coord[i] = self.R
                self.V[i] *= -refl_k
                self.V[1-i] *= refl_k ** 0.1
            self.V[i] = int(self.V[i])

    def move(self):
        self.V[1] -= self.g
        for i in range(2):
            self.coord[i] += self.V[i]
            self.coord[i] = int(self.coord[i])
        self.reflection()
        if self.V[0] ** 2 + self.V[1] ** 2 <= 1 ** 2:
            self.life = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.coord, self.R)


class Gun:

    def __init__(self, coord=[screen_size[0] // 2, screen_size[1] - 20],
                 charge=5, step=2, angle=0, max_power=50, min_power=10,
                 color=RED, velocity=10, size=15):
        self.coord = coord
        self.angle = angle
        self.max_power = max_power
        self.min_power = min_power
        self.color = color
        self.active = False
        self.power = min_power
        self.charge = charge
        self.step = velocity
        self.step = step
        self.min_size = size
        self.size = size

    def activate(self):
        self.active = True

    def set_angle(self, target_pos):
        self.angle = numpy.arctan2(target_pos[1] - self.coord[1],
                                target_pos[0] - self.coord[0])

    def charging(self):
        if self.active and self.power < self.max_power:
            self.power += self.charge
            self.coord[0] += self.step
            self.size += self.step

    def fire(self):
        bullet = Bullet(self.coord, self.power, self.angle)
        self.power = self.min_power
        self.active = False
        self.size = self.min_size
        return bullet

    def draw(self, screen):
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



class Target_1:
    def __init__(self, coord=None, color=None, R=30):
        if coord == None:
            coord = [randint(R, screen_size[0] - R),
                     randint(R, screen_size[1] - R)]
        self.coord = coord
        self.R = R
        self.v = [randint(-7, +7), randint(-7, +7)]
        self.counter = 0

        if color == None:
            color = rand_color()
        self.color = color

    def check(self, ball):
        dist = 0
        for i in range(2):
            dist += (self.coord[i] - ball.coord[i]) ** 2
        dist **= 0.5
        min_dist = self.R + ball.R
        return dist <= min_dist

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.coord, self.R)

    def reflection(self):
        for i in range(2):
            if self.coord[i] > screen_size[i] - self.R or self.coord[i] < self.R:
                self.v[i] = -self.v[i]

    def move(self):
        self.reflection()
        self.coord[1] += self.v[1]
        self.coord[0] += self.v[0]



class Target_2:
    def __init__(self, coord=None, color=None, R=100):
        if coord == None:
            coord = [randint(R, screen_size[0] - R),
                     randint(R, screen_size[1] - R)]
        self.coord = coord
        self.R = R
        self.v = [randint(-7, +7), randint(-7, +7)]
        self.counter = 0

        if color == None:
            color = rand_color()
        self.color = color

    def check(self, ball):
        dist = 0
        for i in range(2):
            dist += (self.coord[i] - ball.coord[i]) ** 2
        dist **= 0.5
        min_dist = self.R + ball.R
        return dist <= min_dist

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.coord[0], self.coord[1],
                                              self.R, self.R])

    def reflection(self):
        for i in range(2):
            if self.coord[i] > screen_size[i] - self.R:
                self.coord[i] = self.R
            elif self.coord[i] < self.R:
                self.coord[i] = screen_size[i] - self.R

    def move(self):
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
    '''
    Score table class.
    '''

    def __init__(self, t_destr=0, b_used=0):
        self.t_destr = t_destr
        self.b_used = b_used
        self.font = pygame.font.SysFont("arial", 30)

    def score(self):
        '''
        Score calculation method.
        '''
        return self.t_destr - self.b_used

    def draw(self, screen):
        score_surf = []
        score_surf.append(self.font.render("Balls used: {}".format(self.b_used),
                                           True, WHITE))
        score_surf.append(self.font.render("Total: {}".format(self.score()),
                                           True, WHITE))
        for i in range(2):
            screen.blit(score_surf[i], [10, 10 + 30 * i])



class GameManager:
    def __init__(self, n_targets=1):
        self.balls = []
        self.gun = Gun()
        self.targets = []
        self.targets_2 = []
        self.score_t = ScoreTable()
        self.n_targets = n_targets
        self.new_mission()

    def new_mission(self):
        for i in range(self.n_targets):
            self.targets.append(Target_1(
                R=randint(max(1, 30 - 2 * max(0, self.score_t.score())),
                            30 - max(0, self.score_t.score()))))
        for i in range(self.n_targets):
            self.targets.append(Target_2(
                R=randint(max(1, 50 - 2 * max(0, self.score_t.score())),
                            50 - max(0, self.score_t.score()))))

    def process(self, events, screen):

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
        done = False
        for event in events:
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.gun.move(-5)
                elif event.key == pygame.K_DOWN:
                    self.gun.move(5)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == 1 and len(self.balls) == 0):
                    self.gun.activate()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.balls.append(self.gun.fire())
                    self.score_t.b_used += 1
        return done

    def draw(self, screen):
        for ball in self.balls:
            ball.draw(screen)
        for target in self.targets:
            target.draw(screen)
        self.gun.draw(screen)
        self.score_t.draw(screen)

    def move(self):
        dead_balls = []
        for i, ball in enumerate(self.balls):
            ball.move()
            if not ball.life:
                dead_balls.append(i)
        for i in reversed(dead_balls):
            self.balls.pop(i)
        for i, target in enumerate(self.targets):
            target.move()
        self.gun.charging()

    def check(self):
        collisions = []
        targets = []
        for i, ball in enumerate(self.balls):
            for j, target in enumerate(self.targets):
                if target.check(ball):
                    collisions.append([i, j])
                    targets.append(j)
        targets.sort()
        for j in reversed(targets):
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
