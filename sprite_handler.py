from tkinter import *
import math

TOP = 0


class PlayingField:
    def __init__(self, h=500, w=500):
        self.tk = Tk()
        self.canvas = Canvas(self.tk, height=h, width=w)
        self.canvas.pack()
        self.widgets = []

    def add(self, widget):
        if widget.order == TOP:
            self.widgets = [widget].append(self.widgets)
        else:
            self.widgets.append(widget)


class Widget:
    def __init__(self, field, render, stack_order=None):
        self.stack_order = stack_order
        self.render_func = render
        self.field = field
        self.field.add(self)

    def render(self):
        self.render_func(self.field.canvas)


class DecorationWidget(Widget):
    pass


class Sprite(Widget):
    pass


def square(canvas):
    canvas.create_rectangle(250, 250, 300, 300)


if __name__ == '__main__':
    f = PlayingField()
    W = Widget(f, square, stack_order=TOP)
