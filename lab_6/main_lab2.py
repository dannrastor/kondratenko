import pygame
import ModuleGameBalls as mgb

GH = mgb.GameHandler()

GH.screen.blit(GH.surface_end,
               ((GH.screen_width - GH.end_width) // 2,
                (GH.screen_height - GH.end_height) // 2))
GH.screen.blit(GH.start_text, GH.start_textRect)
pygame.display.update()

pygame.mixer.init()
pygame.mixer.music.load("Lygushka_sound.mp3")
pygame.mixer.music.set_volume(1.0)
# игровой цикл
while not GH.finished:
    GH.clock.tick(GH.FPS)
    time = pygame.time.get_ticks()
    if GH.end == False and GH.pause == False and GH.start == False:
        pygame.draw.rect(GH.screen, GH.WHITE,
                         ((GH.screen_width * 0.08,
                           GH.screen_height * 0.08),
                          (GH.screen_width * 0.82,
                           GH.screen_height * 0.82)),
                         1)
        text = GH.font.render(str(GH.score), True,
                              GH.WHITE, GH.BLACK)
        textRect = text.get_rect()
        textRect.center = (GH.screen_width // 2, GH.screen_height // 2)
        GH.screen.blit(text, textRect)
        pygame.display.update()
        if not GH.frog:
            Frog = mgb.FakeTarget()
            GH.frog = True
        if GH.frog:
            Frog.move()
        pygame.display.update()
        for ball in GH.pool:
            ball.move()
            pygame.display.update()
        if time - GH.time_of_prev_spawn >= GH.spawn_time:
            unit = mgb.Ball()
            GH.pool.append(unit)
            GH.time_of_prev_spawn = time
            pygame.display.update()
    if GH.frog_killed:
        del GH.pool[:]
        GH.screen.fill(GH.BLACK)
        pygame.mixer.music.play()
        GH.screen.blit(GH.Lygushka, GH.LygushkaRect)
        GH.pause = True
        pygame.display.update()
        GH.time_pause = time
        GH.score -= 3
        if GH.score < 0:
            GH.score = 0
        GH.frog_killed = False
    if GH.cheackscore() and GH.end == False:
        GH.screen.fill(GH.BLACK)
        GH.screen.blit(GH.surface_end, GH.endRect)
        GH.pause = True
        GH.screen.blit(GH.faster_text, GH.faster_textRect)
        pygame.display.update()
        GH.time_pause = time
        GH.score = 0
        GH.level += 1
        GH.max_quantity -= 3
        GH.spawn_time -= 250
    if time - GH.time_pause >= 2 * GH.spawn_time \
            and GH.pause == True:
        GH.screen.fill(GH.BLACK)
        pygame.draw.rect(GH.screen, GH.WHITE,
                         ((GH.screen_width * 0.08,
                           GH.screen_height * 0.08),
                          (GH.screen_width * 0.82,
                           GH.screen_height * 0.82)),
                         1)
        GH.pause = False
    if len(GH.pool) >= GH.max_quantity:
        del GH.pool[:]
        GH.screen.fill(GH.BLACK)
        GH.screen.blit(GH.surface_end,
                       ((GH.screen_width - GH.end_width) // 2,
                        (GH.screen_height - GH.end_height) // 2))
        GH.end = True
        GH.screen.blit(GH.end_text, GH.end_textRect)
        pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GH.finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if GH.start:
                GH.screen.fill(GH.BLACK)
                GH.start = False
            if GH.frog:
                if Frog.check(x, y) == True and GH.start == False:
                    GH.frog_killed = True
                    Frog.kill()
                    GH.frog = False
                    del Frog
            for i, ball in enumerate(GH.pool):
                if ball.check(x, y):
                    ball.kill()
                    GH.pool.pop(i)
                    GH.score += 1
                    text = GH.font.render(str(GH.score), True,
                                          GH.WHITE, GH.BLACK)
                    textRect = text.get_rect()
                    textRect.center = (GH.screen_width // 2,
                                       GH.screen_height // 2)
                    GH.screen.blit(text, textRect)

pygame.font.quit
pygame.mixer.quit()
pygame.quit()


pygame.font.quit
pygame.quit()
