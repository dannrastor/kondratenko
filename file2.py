import pygame
from PIL import Image, ImageDraw, ImageFilter

def myellipse(center: list, color: list, a: int, b: int):
    pygame.draw.ellipse(screen, color, (center[0] - a, center[1] - b, 2 * a, 2 * b))

def UFO(size: float, center: list):
    a1 = int(175 * size)
    b1 = int(60 * size)
    a2 = int(125 * size)
    b2 = int(45 * size)
    light = [[100, 0], [190, 0], [320, 250], [0, 250]]
    for x, y in light:
        x, y = int(x * size), int(y * size)
    for element in light:
        element[0] = int(element[0] * size)
        element[1] = int(element[1] * size)
    illuminaters = [(center[0] - int(146 * size), center[0] + int(146 * size), center[1] + int(4 * size)),
                    (center[0] - int(95 * size), center[0] + int(95 * size), center[1] + int(28 * size)),
                    (center[0] - int(33 * size), center[0] + int(33 * size), center[1] + int(40 * size))]
    surface_light = pygame.Surface((int(320 * size), int(250 * size)), pygame.SRCALPHA)
    pygame.draw.polygon(surface_light, (255, 255, 255, 40), light)
    screen.blit(surface_light, (center[0] - int(160 * size), center[1] + int(50 * size)))
    myellipse(center, (153, 153, 153), a1, b1)
    myellipse([center[0], center[1] - int(25 * size)], (204, 204, 204), a2, b2)
    for x1, x2, y in illuminaters:
        myellipse([x1, y], (255, 255, 255), int(22 * size), int(8 * size))
        myellipse([x2, y], (255, 255, 255), int(22 * size), int(8 * size))

def Alien(size: float, center: list, direct: int):
    basehead = [(center[0] + int(5 * size) * direct, center[1] - int(60 * size)),
                (center[0] - int(20 * size) * direct, center[1] - int(103 * size)),
                (center[0] + int(30 * size) * direct, center[1] - int(103 * size))]

    rightline = [(center[0] + int(5 * size) * direct, center[1] - int(85 * size)),
                 (center[0] + int(41 * size) * direct, center[1] - int(96 * size)),
                 (center[0] + int(16 * size) * direct, center[1] - int(53 * size))]

    leftline = [(center[0] + int(5 * size) * direct, center[1] - int(85 * size)),
                (center[0] - int(31 * size) * direct, center[1] - int(96 * size)),
                (center[0] - int(6 * size) * direct, center[1] - int(53 * size))]

    upperline = [(center[0], center[1] - int(85 * size)), (center[0] - int(25 * size), center[1] - int(117 * size)),
                 (center[0] + int(25 * size), center[1] - int(117 * size))]

    rightleg = [((center[0] + int(18 * size) * direct, center[1] + int(55 * size)), int(12 * size), int(20 * size)),
                ((center[0] + int(28 * size) * direct, center[1] + int(90 * size)), int(10 * size), int(25 * size)),
                ((center[0] + int(40 * size) * direct, center[1] + int(115 * size)), int(12 * size), int(12 * size))]

    rightarm = [((center[0] + int(32 * size) * direct, center[1] - int(30 * size)), int(14 * size), int(14 * size)),
                ((center[0] + int(48 * size) * direct, center[1] - int(22 * size)), int(12 * size), int(8 * size)),
                ((center[0] + int(70 * size) * direct, center[1] - int(15 * size)), int(14 * size), int(7 * size))]

    leftleg = [((center[0] - int(22 * size) * direct, center[1] + int(40 * size)), int(12 * size), int(20 * size)),
               ((center[0] - int(30 * size) * direct, center[1] + int(75 * size)), int(10 * size), int(22 * size)),
               ((center[0] - int(40 * size) * direct, center[1] + int(100 * size)), int(12 * size), int(12 * size))]

    leftarm = [((center[0] - int(24 * size) * direct, center[1] - int(36 * size)), int(14 * size), int(14 * size)),
               ((center[0] - int(38 * size) * direct, center[1] - int(20 * size)), int(10 * size), int(7 * size)),
               ((center[0] - int(49 * size) * direct, center[1] - int(5 * size)), int(5 * size), int(7 * size))]

    leftear = [((center[0] - int(28 * size) * direct, center[1] - int(125 * size)), int(7 * size), int(10 * size)),
               ((center[0] - int(40 * size) * direct, center[1] - int(140 * size)), int(10 * size), int(10 * size)),
               ((center[0] - int(45 * size) * direct, center[1] - int(160 * size)), int(11 * size), int(6 * size)),
               ((center[0] - int(49 * size) * direct, center[1] - int(175 * size)), int(12 * size), int(10 * size))]

    rightear = [((center[0] + int(42 * size) * direct, center[1] - int(117 * size)), int(10 * size), int(10 * size)),
                ((center[0] + int(47 * size) * direct, center[1] - int(127 * size)), int(6 * size), int(11 * size)),
                ((center[0] + int(60 * size) * direct, center[1] - int(145 * size)), int(8 * size), int(8 * size)),
                ((center[0] + int(78 * size) * direct, center[1] - int(155 * size)), int(7 * size), int(5 * size)),
                ((center[0] + int(92 * size) * direct, center[1] - int(152 * size)), int(10 * size), int(15 * size))]

    myellipse(center, (221, 233, 175), int(25 * size), int(60 * size))
    pygame.draw.polygon(screen, (221, 233, 175), basehead)
    pygame.draw.circle(screen, (221, 233, 175),
                       (center[0] + int(5 * size) * direct, center[1] - int(60 * size)), int(14 * size))
    pygame.draw.circle(screen, (221, 233, 175),
                       (center[0] + int(30 * size) * direct, center[1] - int(103 * size)), int(14 * size))
    pygame.draw.circle(screen, (221, 233, 175),
                       (center[0] - int(20 * size) * direct, center[1] - int(103 * size)), int(14 * size))
    pygame.draw.polygon(screen, (221, 233, 175), rightline)
    pygame.draw.polygon(screen, (221, 233, 175), leftline)
    pygame.draw.polygon(screen, (221, 233, 175), upperline)
    pygame.draw.circle(screen, (255, 0, 0), (center[0] + int(80 * size) * direct, center[1] - int(40 * size)),
                       int(25 * size))
    pygame.draw.line(screen, (0, 0, 0), (center[0] + int(80 * size) * direct, center[1] - int(60 * size)),
                     (center[0] + int(100 * size) * direct, center[1] - int(75 * size)), 4)
    pygame.draw.circle(screen, (0, 0, 0),
                       (center[0] + int(25 * size) * direct, center[1] - int(93 * size)), int(9 * size))
    pygame.draw.circle(screen, (0, 0, 0),
                       (center[0] - int(13 * size) * direct, center[1] - int(95 * size)), int(12 * size))
    pygame.draw.circle(screen, (255, 255, 255),
                       (center[0] + int(26 * size) * direct, center[1] - int(92 * size)), int(3 * size))
    pygame.draw.circle(screen, (255, 255, 255),
                       (center[0] - int(11 * size) * direct, center[1] - int(93 * size)), int(4 * size))
    myellipse((center[0] + int(7 * size) * direct, center[1] - int(80 * size)), (0, 0, 0), int(2 * size), int(4 * size))
    myellipse((center[0] + int(8 * size) * direct, center[1] - int(62 * size)), (0, 0, 0), int(5 * size), int(3 * size))
    leaf = pygame.Surface((40 * size, 40 * size), pygame.SRCALPHA)
    pygame.draw.ellipse(leaf, (130, 160, 0), (0, 0, int(20 * size), (10 * size)))
    leaf = pygame.transform.rotate(leaf, -30 * direct)
    screen.blit(leaf, (center[0] + int((80 - 5 * direct) * size) * direct, center[1] - int((77 - 7 * direct) * size)))
    for center, a, b in leftleg:
        myellipse(center, (221, 233, 175), a, b)
    for center, a, b in rightleg:
        myellipse(center, (221, 233, 175), a, b)
    for center, a, b in leftarm:
        myellipse(center, (221, 233, 175), a, b)
    for center, a, b in rightarm:
        myellipse(center, (221, 233, 175), a, b)
    for center, a, b in rightear:
        myellipse(center, (221, 233, 175), a, b)
    for center, a, b in leftear:
        myellipse(center, (221, 233, 175), a, b)


pygame.init()

# constants
FPS = 30
screenwidth = 794
screenhight = 1123
lightclouds = [(-600, 20, 400, 220), (500, -25, 1100, 95), (350, 130, 1050, 270),
               (250, 300, 950, 450), (-150, 250, 530, 400)]
darkclouds = [(120, 80, 980, 200), (-333, 200, 333, 360), (169, 380, 835, 530)]
UFOs_coordinates = [(0.8, (180, 450)), (0.3, (370, 550)), (0.5, (600, 450))]
ALIENs_coordinates = [(0.9, (560, 750), 1), (0.5, (75, 720), -1), (0.3, (200, 650), -1),
                      (0.4, (300, 710), 1), (0.6, (230, 870), -1)]

# screens
screen = pygame.display.set_mode((screenwidth, screenhight))

# background

pygame.draw.rect(screen, (0, 34, 43), (0, 0, 794, 579))
pygame.draw.rect(screen, (34, 43, 0), (0, 579, 794, 1123))
pygame.draw.circle(screen, (242, 242, 242), (510, 265), 120)
pygame.draw.circle(screen, (255, 255, 210), (455, 240), 30)
pygame.draw.circle(screen, (255, 255, 210), (458, 255), 20)
pygame.draw.circle(screen, (255, 255, 210), (462, 270), 15)
# clouds

img = Image.new('RGBA', (screenwidth, screenhight), (0, 0, 0, 0))
idraw = ImageDraw.Draw(img)

for cloud in lightclouds:
    idraw.ellipse(cloud, (102, 102, 102, 150), None)
for cloud in darkclouds:
    idraw.ellipse(cloud, (51, 51, 51, 150), None)
img = img.filter(ImageFilter.BLUR)
raw_clouds = img.tobytes("raw", 'RGBA')
surf_clouds = pygame.image.fromstring(raw_clouds, (screenwidth, screenhight), 'RGBA')
screen.blit(surf_clouds, (0, 0))
# UFO
for size, center in UFOs_coordinates:
    UFO(size, center)

# Alien
for size, center, direction in ALIENs_coordinates:
    Alien(size, center, direction)

pygame.display.update()
pygame.image.save(screen, 'file2_result.png')
clock = pygame.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()

