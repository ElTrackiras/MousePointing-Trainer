import pygame
import random
pygame.init()
pygame.mixer.init()
ShipOne = pygame.image.load('Assets/Monster.png')
shot = pygame.mixer.Sound('Assets/gunshot.wav')


class iontro:
    font_blinker = 0

    @classmethod
    def home(cls, screen, font):
        Puppeteer.reset_variables()
        title_lbl = font.render('Mouse-Pointing Trainer', True, (0, 0, 0))
        start_lbl = font.render('Press "Space" to start', True, (cls.font_blinker, cls.font_blinker, cls.font_blinker))
        cls.font_blinker += 9
        if cls.font_blinker >= 255:
            cls.font_blinker = 0
        screen.blit(title_lbl, (200, 200))
        screen.blit(start_lbl, (200, 300))

    @classmethod
    def game_over(cls, screen, font, misses, kills, ran):
        game_over_lbl = font.render('GAME OVER', True, (0, 0, 0))
        misses_lbl = font.render('Misses: ' + str(misses), True, (0, 0, 0))
        kills_lbl = font.render('Kills: ' + str(kills), True, (0, 0, 0))
        ran_lbl = font.render('Got Away: ' + str(ran), True, (0, 0, 0))
        press_lbl = font.render('PRESS SPACE', True, (cls.font_blinker, cls.font_blinker, cls.font_blinker))
        if (kills + misses) > 0:
            accuracy = font.render('Accuracy: {}%'.format(round((kills/(kills + misses)) * 100)), True, (0, 0, 0))
        else:
            accuracy = font.render('Accuracy: No shots taken', True, (0, 0, 0))
        screen.blit(game_over_lbl, (0, 0))
        screen.blit(misses_lbl, (300, 0))
        screen.blit(kills_lbl, (300, 100))
        screen.blit(ran_lbl, (300, 200))
        screen.blit(accuracy, (300, 300))
        screen.blit(press_lbl, (300, 450))
        cls.font_blinker += 9
        if cls.font_blinker >= 255:
            cls.font_blinker = 0


class Targets:
    all_targets = list()

    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.image = ShipOne
        self.lifetime = 200
        Targets.all_targets.append(self)

    def summon(self, screen):
        self.image = pygame.transform.scale(self.image, (self.height, self.width))
        screen.blit(self.image, (self.x, self.y))
        self.lifetime -= 1
        if self.lifetime <= 0:
            Targets.all_targets.remove(self)
            Puppeteer.ran_away += 1


class Puppeteer:
    fps = pygame.time.Clock()
    screen_width = 1000
    screen_height = 700
    game_screen = pygame.display.set_mode((screen_width, screen_height))
    monster_spawn_time = 10
    missed_shots = 0
    kills = 0
    ran_away = 0
    myfont = pygame.font.SysFont("monospace", 30)
    page = 'Home'
    time = 0
    dt = 0

    @classmethod
    def ui_texts(cls):
        missed_lbl = cls.myfont.render('Missed Shots:' + str(cls.missed_shots), True, (0, 0, 0))
        killed_lbl = cls.myfont.render('Kills:' + str(cls.kills), True, (0, 0, 0))
        ran_away_lbl = cls.myfont.render('Got Away:' + str(cls.ran_away), True, (0, 0, 0))
        cls.game_screen.blit(missed_lbl, (200, 0))
        cls.game_screen.blit(killed_lbl, (500, 0))
        cls.game_screen.blit(ran_away_lbl, (690, 0))

    @classmethod
    def monster_spawner(cls):
        cls.monster_spawn_time -= 1
        if cls.monster_spawn_time <= 0:
            x = Targets(random.randrange(0, cls.screen_width - 50), random.randrange(0, cls.screen_height - 50), 50, 50)
            for i in Targets.all_targets:
                if x.x > i.x and x.x < i.x + i.width or x.x + x.width > i.x and x.x + x.width < i.x + i.width:
                    if x.y > i.y and x.y < i.y + i.height or x.y + x.height > i.y and x.y + x.height < i.y + i.height:
                        Targets.all_targets.remove(i)
                        print('Collision')
            cls.monster_spawn_time = 15

    @classmethod
    def target_handler(cls):
        for i in Targets.all_targets:
            i.summon(cls.game_screen)

    @classmethod
    def reset_variables(cls):
        cls.time = 30
        cls.missed_shots = 0
        cls.kills = 0
        cls.ran_away = 0
        Targets.all_targets.clear()

    @classmethod
    def timer(cls, dt):
        timer_lbl = cls.myfont.render("{}:{}".format('Time', round(cls.time)), True, (0, 0, 0))
        cls.game_screen.blit(timer_lbl, (0, 0))
        cls.time -= dt
        if cls.time <= 0:
            cls.page = 'GameOver'

    missed_shots_add = True

    @classmethod
    def start_game(cls):
        run = True
        while run:
            cls.game_screen.fill((255, 255, 255))
            cls.fps.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if cls.page == 'Game':
                        shot.play()
                        mx, my = pygame.mouse.get_pos()
                        for i in Targets.all_targets:
                            if mx > i.x and mx < i.x + i.width:
                                if my > i.y and my < i.y + i.height:
                                    Targets.all_targets.remove(i)
                                    cls.kills += 1
                                    if len(Targets.all_targets) > 1:
                                        cls.missed_shots -= 1
                            else:
                                if cls.missed_shots_add:
                                    cls.missed_shots += 1
                                    cls.missed_shots_add = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        if cls.page == 'Home':
                            cls.page = 'Game'

                        elif cls.page == 'GameOver':
                            cls.page = 'Home'

            if cls.page == 'Game':
                cls.missed_shots_add = True
                cls.target_handler()
                cls.monster_spawner()
                cls.ui_texts()
                cls.timer(cls.dt)

            elif cls.page == 'Home':
                iontro.home(cls.game_screen, cls.myfont)

            else:
                iontro.game_over(cls.game_screen, cls.myfont, cls.missed_shots, cls.kills, cls.ran_away)

            cls.dt = cls.fps.tick(60)/ 1000

            pygame.display.update()



Puppeteer.start_game()
pygame.quit()
