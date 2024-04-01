import pygame
import utils.colors as colors
from random import randint
from settings import Settings
from controls.keys import Keys
from utils.vector2 import Vector2
from ball import Ball

class Game:
    def __init__(self) -> None:
        pygame.init()
        info = pygame.display.Info()
        self.settings = Settings((
            info.current_w,
            info.current_h
        ))
        print(self.settings.get_win_size())
        self.running = True
        self.paused = False
        self.keys = Keys()
        self.surface = pygame.display.set_mode(
            self.settings.get_win_size(),
            pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.balls: list[Ball] = []
        self.gravity = 0.01

    def on_init(self) -> None:
        # self.balls += [
        #     Ball(Vector2(100, 100)),
        #     Ball(Vector2(90, 130)),
        #     Ball(Vector2(110, 130)),
        #     Ball(Vector2(80, 150)),
        #     Ball(Vector2(100, 150)),
        #     Ball(Vector2(120, 150)),
        #     Ball(Vector2(70, 170)),
        #     Ball(Vector2(90, 170)),
        #     Ball(Vector2(110, 170)),
        #     Ball(Vector2(130, 170)),
        # ]
        # for i in range(50):
        #     self. balls.append(Ball(
        #         Vector2(randint(20, 1000),
        #         randint(20, 600)),
        #         radius=10,
        #         mass=100
        #     ))
        scr = self.settings.get_win_size()
        self.balls.append(Ball(pos=Vector2(scr[0]/2, scr[1]/2), radius=20, mass=10000))
        for _ in range(1):
            self.balls.append(Ball(
                Vector2(randint(20, scr[0]-20),
                        randint(20, scr[1]-20)),
                radius=5,
                mass=0.1,
                vel=Vector2(randint(-5, 5), randint(-5, 5))
            ))

    def on_execute(self) -> None:
        self.on_init()

        while self.running:
            dt = self.clock.tick_busy_loop(self.settings.frame_rate)
            for event in pygame.event.get():
                self.handle_event(event)
            if not self.paused: self.update(dt)
            self.render()

        self.on_cleanup()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            self.keys.handle_down(event.key)
            self.handle_key(event.key)
        elif event.type == pygame.KEYUP:
            self.keys.handle_up(event.key)
        elif event.type == pygame.WINDOWRESIZED:
            self.settings.win_size = (event.x, event.y)

    def handle_key(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_SPACE:
            for b in self.balls: b.vel += Vector2(randint(-10, 10), randint(-10, 10))

    def handle_mouse_buttons(self) -> None:
        # mouse buttons: 0 == left, 1 == middle, 2 == right
        # buttons = pygame.mouse.get_pressed()
        pass

    def update(self, dt: int) -> None:
        for i, _ in enumerate(self.balls):
            b = self.balls[i]
            #b.vel.y += self.gravity * dt
            b.pos += b.vel
            b.check_bounds(self.settings.get_win_size())
            for j, _ in enumerate(self.balls):
                if i == j: continue
                b.handle_collision(self.balls[j])
                b.apply_gravity(self.balls[j])
            

    def render(self) -> None:
        self.surface.fill(colors.BLACK)

        for b in self.balls:
            b.render(self.surface)

        pygame.display.flip()

    def on_cleanup(self) -> None:
        pass
