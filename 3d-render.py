from numpy import *

from tkinter import *

# cam rotation

theta_x = 0
theta_y = 0
theta_z = 0

# cam position

view_x = 0
view_y = 0
view_z = 0

# display surface (relative coords)

e_x = 0
e_y = 0
e_z = 0.1

FOV_factor = 1500

tk = Tk()
canvas = Canvas(tk, width=500, height=500)
canvas.pack()

render_stack = []


class UpdateHandler:
    @classmethod
    def add_to_render_stack(cls, polygon):
        cls.render_stack.append(polygon)

    @classmethod
    def render(cls):
        polygons = []
        projected = []
        for polygon in cls.render_stack:
            polygons.append(polygon.vertex_locations)
            val = []
            for vertex in polygon.vertex_locations:
                val.append(project(vertex))
            projected.append(val)
        while polygons:
            mindist = 0
            for polygon in polygons:
                mindist = None
#        for polygon in cls.render_stack:
#            polygon.render()


UpdateHandler.render_stack = []


def project(point):
    d = array([[1, 0, 0], [0, cos(theta_x), sin(theta_x)], [0, sin(theta_x), cos(theta_x)]]) @ array(
        [[cos(theta_x), 0, -sin(theta_x)], [0, 1, 0], [sin(theta_x), 0, cos(theta_x)]]) @ array(
        [[cos(theta_x), sin(theta_x), 0], [-sin(theta_x), cos(theta_x), 0], [0, 0, 1]]) @ (
                    array([point[0], point[1], point[2]]) - array([view_x, view_y, view_z]))
    b = [(e_z / d[2]) * d[0] + e_x, (e_z / d[2]) * d[1] + e_y]
    return b


def get_relative_coords(point):
    d = array([[1, 0, 0], [0, cos(theta_x), sin(theta_x)], [0, sin(theta_x), cos(theta_x)]]) @ array(
        [[cos(theta_x), 0, -sin(theta_x)], [0, 1, 0], [sin(theta_x), 0, cos(theta_x)]]) @ array(
        [[cos(theta_x), sin(theta_x), 0], [-sin(theta_x), cos(theta_x), 0], [0, 0, 1]]) @ (
                    array([point[0], point[1], point[2]]) - array([view_x, view_y, view_z]))
    return d


class Polygon:
    def __init__(self, *args):
        self.vertices = 0
        self.vertex_locations = []
        for a in args:
            self.vertices += 1
            self.vertex_locations.append(a)

    def render(self):
        projected = []
        for v in self.vertex_locations:
            val = project(v)
            projected.append(val[0]*FOV_factor+250)
            projected.append(val[1]*FOV_factor+250)
        canvas.create_polygon(projected, outline='black', fill='gray', width=2)


class Solid:
    def __init__(self, faces):
        self.polygons = []
        for f in faces:
            self.polygons.append(f)

    def render(self):
        for face in self.polygons:
            UpdateHandler.add_to_render_stack(face)

class RectPrismOrtho(Solid):
    def __init__(self, x, y, z, dx=1, dy=1, dz=1):
        faces = [Polygon([x, y, z], [x+dx, y, z], [x+dx, y+dy, z], [x, y+dy, z]),
                 Polygon([x, y, z], [x+dx, y, z], [x+dx, y, z+dz], [x, y, z+dz]),
                 Polygon([x, y, z], [x, y+dy, z], [x, y + dy, z+dz], [x, y, z+dz]),
                 Polygon([x+dx, y+dy, z+dz], [x, y+dy, z+dz], [x, y, z+dz], [x+dx, y, z+dz]),
                 Polygon([x + dx, y + dy, z + dz], [x, y + dy, z + dz], [x, y+dy, z], [x + dx, y+dy, z]),
                 Polygon([x + dx, y + dy, z + dz], [x+dx, y, z + dz], [x+dx, y, z], [x + dx, y + dy, z])]
        super().__init__(faces)


if __name__ == '__main__':
#    poly = Polygon([1, 1, 2], [1, -1, 2], [-1, -1, 1], [-1, 1, 1])
#    UpdateHandler.add_to_render_stack(poly)
    cube = RectPrismOrtho(1, -0.5, 1, 1, 1, 1)
    cube.render()
    UpdateHandler.render()
    tk.mainloop()
