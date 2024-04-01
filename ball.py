from math import sqrt, atan
import pygame.draw as draw
import utils.colors as colors
from pygame.surface import Surface
from utils.vector2 import Vector2

class Ball:
    def __init__(
            self,
            pos: Vector2,
            radius = 10,
            mass = 1,
            vel = Vector2(0, 0),
            color = colors.WHITE) -> None:
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.mass = mass
        self.color = color

    def render(self, surface: Surface) -> None:
        draw.circle(surface, self.color, self.pos.get(), self.radius)
        # end_pos = self.pos + (self.vel * Vector2(10, 10))
        # draw.line(surface, colors.RED, self.pos.get(), end_pos.get(), 2)

    def dot(self, v1: Vector2, v2: Vector2) -> float:
        return v1.x*v2.x + v1.y*v2.y

    def get_new_vel(self, b1: "Ball", b2: "Ball") -> Vector2:
        masses = (b2.mass) / (b1.mass + b2.mass)
        dot = self.dot(b1.vel - b2.vel, b1.pos - b2.pos)
        diff = b1.pos - b2.pos
        norm = sqrt(diff.x**2 + diff.y**2)
        d1 = 0 if norm == 0 else dot / norm**2

        return b1.vel - (masses * (d1*diff) )

    def apply_gravity(self, b: "Ball", constant: float = 1) -> None:
        '''
        https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation#Gravity_field
        '''
        d = sqrt((b.pos.x - self.pos.x)**2 + (b.pos.y - self.pos.y)**2)
        if d == 0: return
        diff = b.pos - self.pos
        norm = Vector2(diff.x / d, diff.y / d)
        f = -self.mass*constant / d**2
        v = f * norm
        b.vel = v + b.vel

    def handle_collision(self, b: "Ball") -> None:
        '''
        https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects
        '''
        dist = sqrt((b.pos.x - self.pos.x)**2 + (b.pos.y - self.pos.y)**2)
        min_diff = self.radius + b.radius
        if dist < min_diff:
            diff = self.pos - b.pos
            mag = sqrt(diff.x**2 + diff.y**2)
            overlap = mag - min_diff
            norm = Vector2(0, 0) if mag == 0 else Vector2(diff.x / mag, diff.y / mag)
            re_pos = Vector2( (norm.x*overlap) , (norm.y*overlap)  )
            b.pos += re_pos

            
            v1new = self.get_new_vel(self, b)
            v2new = self.get_new_vel(b, self)

            self.vel = v1new
            b.vel = v2new

    def check_bounds(self, bounds: tuple[int, int]) -> None:
        left_diff = self.get_left_edge()
        right_diff = bounds[0] - self.get_right_edge()
        top_diff = self.get_top_edge()
        bottom_diff = bounds[1] - self.get_bottom_edge()

        slowdown = 0.75
        if left_diff < 0:
            self.pos.x += abs(left_diff)
            self.vel.x = -self.vel.x*slowdown
        if right_diff < 0:
            self.pos.x -= abs(right_diff)
            self.vel.x = -self.vel.x*slowdown
        if top_diff < 0:
            self.pos.y += abs(top_diff)
            self.vel.y = -self.vel.y*slowdown
        if bottom_diff < 0:
            self.pos.y -= abs(bottom_diff)
            self.vel.y = -self.vel.y*slowdown

    def get_left_edge(self) -> float:
        return self.pos.x - self.radius

    def get_right_edge(self) -> float:
        return self.pos.x + self.radius

    def get_top_edge(self) -> float:
        return self.pos.y - self.radius

    def get_bottom_edge(self) -> float:
        return self.pos.y + self.radius
    