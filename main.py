import math
from tkinter import *
import random
import time

random.seed(59009876548765432)

GAME_TICK_SPEED = 100
PLAYER_MAX_SPEED = 30
PLAYER_FALL_ANGLE = 0.8
TERRAIN_RESOLUTION = 5
WIDTH = 500
HEIGHT = 500
FLAT = 0
RISING = 1
FALLING = 2
ACCELERATION = 3

tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
canvas.pack()


def my_polygon(a, b, c, d, color='black'):
    return canvas.create_polygon(a[0], a[1], b[0], b[1], c[0], c[1], d[0], d[1], outline=color, fill=color)


class Terrain:
    def __init__(self, template=()):
        if template == ():
            self.height_map = self.random_terrain_gen(5000)
        else:
            self.height_map = template
        self.min_bound = 0
        self.max_bound = len(self.height_map) - 1
        self.angle_map = []
        for j in range(1, len(self.height_map)):
            self.angle_map.append(math.atan(-(self.height_map[j] - self.height_map[j - 1]) / TERRAIN_RESOLUTION))
        self.current_index = self.min_bound
        self.widgets = []
        self.left_edge = 0
        self.right_edge = WIDTH
        self.running_total = 0
        self.render()

    def random_terrain_gen(self, length):
        status = FLAT
        prev = 100
        slope = 0
        gen_buffer = []
        for i in range(length):
            r = random.randint(0, 25)
            if r == 1:
                new = random.randint(1, 2)
                status = (status + new) % 3
            if prev < 25:
                status = RISING
                slope = 0
            if prev > HEIGHT - 150:
                status = FALLING
                slope = 0
            if status == FLAT:
                if random.randint(0, 2) == 0:
                    new = random.randint(-2, 2)
                    gen_buffer.append(prev + new)
                    slope = new
                    prev += slope
                else:
                    gen_buffer.append(prev + slope)
                    prev += slope
            elif status == RISING:
                if random.randint(0, 2) == 0:
                    new = random.randint(1, 5)
                    gen_buffer.append(prev + new)
                    slope = new
                    prev += slope
                else:
                    gen_buffer.append(prev + slope)
                    prev += slope
            elif status == FALLING:
                if random.randint(0, 2) == 0:
                    new = random.randint(-5, -1)
                    gen_buffer.append(prev + new)
                    slope = new
                    prev += slope
                else:
                    gen_buffer.append(prev + slope)
                    prev += slope
        return gen_buffer

    def render(self):
        for i in range(len(self.height_map) - 1):
            poly = my_polygon([i * TERRAIN_RESOLUTION, 500], [(i + 1) * TERRAIN_RESOLUTION, 500],
                              [(i + 1) * TERRAIN_RESOLUTION, 500 - self.height_map[i + 1]],
                              [i * TERRAIN_RESOLUTION, 500 - self.height_map[i]])
            self.widgets.append(poly)

    def height(self):
        return 500 - self.height_map[int(self.current_index + 50)]

    def angle(self):
        return self.angle_map[int(self.current_index + 50)]

    def update(self, distance):
        for w in self.widgets:
            canvas.move(w, -distance, 0)
        self.running_total += distance / TERRAIN_RESOLUTION
        self.current_index = round(self.running_total)


class Player:
    def __init__(self, terrain):
        self.altitude = terrain.height()
        self.speed = 10
        self.angle = 0
        self.target_speed = 10
        self.on_ground = True
        self.prev_height = self.altitude
        self.widgets = [canvas.create_rectangle(245, terrain.height(), 255, terrain.height() - 10, fill='green')]
        self.jump_trigger = False
        canvas.bind_all('<Up>', self.set_speed)
        canvas.bind_all('<Down>', self.set_speed)
        canvas.bind_all('<space>', self.jump)
    #       print(self.altitude)

    def update(self, terrain):
        self.prev_height = self.altitude
        if self.speed != self.target_speed:
            if self.speed < self.target_speed:
                if self.speed - ACCELERATION >= self.target_speed:
                    self.speed += 3
                else:
                    self.speed = self.target_speed
            elif self.speed > self.target_speed:
                if self.speed + ACCELERATION <= self.target_speed:
                    self.speed -= 3
                else:
                    self.speed = self.target_speed
        terrain.update(math.cos(self.angle) * self.speed)
        self.altitude += (math.sin(self.angle) * self.speed)
        #        print(self.altitude, terrain.height())
        if self.altitude >= terrain.height():
            self.altitude = terrain.height()
            self.on_ground = True
            if self.angle - 1.2 > terrain.angle():
                self.explode()
            self.angle = terrain.angle()
        else:
            self.on_ground = False
        if self.on_ground:
            self.angle = terrain.angle()
        else:
            if self.angle < 1:
                self.angle += (PLAYER_FALL_ANGLE * (1 / self.speed))
#                print(self.angle)
        if self.jump_trigger and self.on_ground:
            self.angle -= 0.5
            self.altitude -= 10
        self.jump_trigger = False
        self.render(self.altitude)

    def explode(self):
        print('oops, you died!')

    def set_speed(self, event):
        if self.on_ground:
            if event.keysym == 'Up':
                if self.target_speed < PLAYER_MAX_SPEED:
                    self.target_speed += 1
            elif event.keysym == 'Down':
                if self.target_speed > 0:
                    self.target_speed -= 1

    def jump(self, event):
        self.jump_trigger = True

    def render(self, h):
        for w in self.widgets:
            canvas.delete(w)
        x = 2
        y = 2
        cosine = math.cos(-self.angle)*x
        sine = math.sin(-self.angle)*y
        self.widgets = [my_polygon([cosine * x + sine * y + 250, -sine * x + cosine * y + h + 0.5 * y],
                                   [cosine * -x + sine * y + 250, -sine * -x + cosine * y + h + 0.5 * y],
                                   [cosine * -x + sine * -y + 250, -sine * -x + cosine * -y + h + 0.5 * y],
                                   [cosine * x + sine * -y + 250, -sine * x + cosine * -y + h + 0.5 * y],
                                   color='green')]
#        self.widgets = [my_polygon([245 - math.cos(self.angle) * 10, h - math.sin(self.angle) * 10],
#                                   [245 + math.cos(self.angle) * 10, (h - 10) - math.sin(self.angle) * 10],
#                                   [250 + math.cos(self.angle) * 10, (h - 10) + math.sin(self.angle) * 10],
#                                   [250 - math.cos(self.angle) * 10, h + math.sin(self.angle) * 10],
#                                   )]


# t=Terrain([100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 112, 114, 116, 118, 120, 125, 130, 135, 140, 145,
# 150, 100, 100, 99, 98, 100, 150, 145, 140, 135, 130, 125, 120, 118, 116, 114, 112, 110, 109, 108, 107, 106, 105,
# 104, 103, 102, 101, 100])
t = Terrain()
p = Player(t)
tk.update()
p.update(t)

if __name__ == '__main__':
    time.sleep(1)
    while 1:
        p.update(t)
        tk.update()
        time.sleep(0.05)
