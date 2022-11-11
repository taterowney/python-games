'''
Galactapi.py
an arcade-based video game made with tkinter
'''
import random
import time
from math import sin, cos, radians
from tk3 import setup
VERSION = "1.1.1"
CANVAS = setup(w=750, h=750)
TK = CANVAS.Tk
CANVAS.create_rectangle(0, 0, 750, 750, outline='black', fill='black')
random.seed(42)
for i in range(30):
	x = random.randint(10, 740)
	y = random.randint(10, 740)
	CANVAS.create_rectangle(x, y, x+3, y+3, fill='white')
CANVAS.create_oval(236, 369, 246-5, 379-5, fill='#ffd800')
CANVAS.create_line(232, 369, 246, 374, fill='#ffd800')
CANVAS.create_oval(236-150, 369+45, 246-5-150, 379-5+45, fill='#ffd800')
CANVAS.create_line(232-150, 369+45, 246-150, 374+45, fill='#ffd800')
CANVAS.create_oval(200+400, 150+300, 215+400, 165+300, fill='blue')
FRAME_TIME = 0.02

def my_range(A, B):
	'''
	making the range function easier to use
	'''
	if A > B:
		A, B = B, A
	return list(range(int(A), int(B)))

def polar(coords, theta, hyp):
	theta = theta % 360
	x = coords[0]
	y = coords[1]
	opposite = sin(radians(theta))*hyp
	aj = cos(radians(theta))*hyp
	return ((x+aj), (y+opposite))

def poly(*args, **kw):
	return CANVAS._create('polygon', unpack(args), kw)

def unpack(args):
	ret = []
	for a in args:
		ret.append(a[0])
		ret.append(a[1])
	return ret

class sprite:
	def __init__(self, game, x, y, type):
		self.x = x
		self.y = y
		self.type = type
		self.angle = 0
		self.widgets = []
		self.dead = False
		self.game = game
		self.draw()
	def delete(self):
		for w in self.widgets:
			CANVAS.delete(w)
	def draw(self):
		global pos
		self.delete()
		angle = self.angle+180
		val = angle % 90
		if val >= 45:
			val -= 45
			val = 45-val
			val /= 2
		self.x_side = my_range(self.x-27-val, self.x+val+27)
		self.y_side = my_range(self.y-5, self.y+val+40)
		start = polar((self.x, self.y), angle+180, 25)
		if self.type == 'blue':
			self.widgets = [
				poly(start, polar(start, angle, 10), polar(polar(start, angle, 10), angle+90, 5), polar(start, angle+90, 5), outline='blue', fill='blue'),
				poly(start, polar(start, angle+300, 20), polar(polar(start, angle, 50), angle+240, 20), polar(start, angle, 50), fill='cyan'),
				poly(start, polar(start, angle, 50), polar(polar(start, angle, 50), angle+270, 10), polar(start, angle+270, 10), fill='blue'),
				poly(start, polar(start, angle, 15), polar(polar(start, angle, 15), angle+265, 30), polar(start, angle+300, 45), polar(start, angle+275, 30), fill='blue')]
#			CANVAS.create_line(self.x, min(self.y_side), self.x, max(self.y_side), fill='orange')
#			CANVAS.create_line(min(self.x_side), self.y, max(self.x_side), self.y, fill='orange')
			start = polar(start, angle, 35)
			self.widgets.append(poly(start, polar(start, angle, 15), polar(polar(start, angle, 15), angle+265, 30), polar(start, angle+255, 40), polar(start, angle+275, 30), fill='blue'))
			start = polar(start, angle, 5)
			self.widgets.append(poly(start, polar(start, angle, 10), polar(polar(start, angle, 10), angle+90, 5), polar(start, angle+90, 5), outline='blue', fill='blue'))
		elif self.type == 'red':
			self.widgets = [
	poly(start, polar(start, angle+300, 20), polar(polar(start, angle, 50), angle+240, 20), polar(start, angle, 50), fill='orange'),
	poly(start, polar(start, angle, 50), polar(polar(start, angle, 50), angle+270, 10), polar(start, angle+270, 10), fill='red'),
	poly(start, polar(start, angle, 15), polar(polar(start, angle, 15), angle+265, 40), polar(start, angle+275, 40), fill='red')]
			start = polar(start, angle, 35)
			self.widgets.append(poly(start, polar(start, angle, 15), polar(polar(start, angle, 15), angle+265, 40), polar(start, angle+275, 40), fill='red'))
		if ((pos-25 in self.x_side) or (pos+25 in self.x_side)) and max(self.y_side) >= 670:
#		   print("BOOM")
			self.game.end_game(sprite=self)
	def explode(self):
		return CANVAS.create_oval(self.x-25, self.y-25, self.x+25, self.y+25, outline='orange', fill='orange')
	def fire_shot(self):
		g.sh.add(self.x, self.y+25, 1.5)
	def move(self, x, y):
#	   if self.dead==True:
#		   self.explode()
#		   del g.sprites[g.sprites.index(s)]
#		   return
		self.x += x
		self.y += y
		self.angle = 0
		self.draw()
	def go_to(self, x, y):
#	   if self.dead==True:
#		   self.explode()
#		   del g.sprites[g.sprites.index(s)]
#		   return
		self.x = x
		self.y = y
		self.draw()
	def follow(self, angle, inc):
		self.angle += angle
		new = polar((self.x, self.y), self.angle+90, inc)
		self.x = new[0]
		self.y = new[1]
		self.draw()

class avatar:
	def __init__(self):
		CANVAS.bind_all('<KeyPress-Left>', self.future_move)
		CANVAS.bind_all('<KeyPress-Right>', self.future_move)
		CANVAS.bind_all('<KeyPress-Up>', self.fire)
		CANVAS.bind_all('<KeyRelease-Up>', self.reset)
		global pos
		pos = 375
		self.pos = 375
		self.last = False
		self.dead = False
		self.count = 0
		self.draw()
	def draw(self):
		self.widgets = [
			CANVAS.create_line(370, 675, 370, 660, fill='red'),
			CANVAS.create_line(380, 675, 380, 660, fill='red'),
			CANVAS.create_line(350, 715, 350, 690, fill='white'),
			CANVAS.create_line(355, 715, 355, 685, fill='white'),
			CANVAS.create_line(400, 715, 400, 690, fill='white'),
			CANVAS.create_line(395, 715, 395, 685, fill='white'),
			CANVAS.create_rectangle(365, 675, 385, 715, outline='white', fill='white'),
			CANVAS.create_polygon(365, 715, 365, 700, 350, 715, outline='red', fill='red'),
			CANVAS.create_polygon(385, 715, 385, 700, 400, 715, outline='red', fill='red'),
			CANVAS.create_polygon(365, 675, 385, 675, 375, 665, outline='white', fill='white')]
	def move(self):
		global pos
		self.count += 1
		self.pos += g.val
		if self.pos > 25 and g.val < 0:
			for w in self.widgets:
				CANVAS.move(w, g.val, 0)
		elif self.pos < 725 and g.val > 0:
			for w in self.widgets:
				CANVAS.move(w, g.val, 0)
		pos = self.pos
	def future_move(self, event):
		if event.keysym == 'Left':
			g.val -= 10
		if event.keysym == 'Right':
			g.val += 10
	def fire(self, event):
		if self.last == False and self.count >= 5:
			g.sh.add(self.pos, 665, -1)
			self.last = True
			self.count = 0
	def reset(self, event):
		self.last = False

class shots:
	def __init__(self):
		self.x = []
		self.y = []
		self.end = []
		self.widgets = []
		self.vec = []
	def add(self, x, y, vec):
		self.x.append(x)
		self.y.append(y)
		self.widgets.append(None)
		self.vec.append(vec*10)
	def delete(self):
		for i in self.widgets:
			CANVAS.delete(i)
	def draw(self):
		for i, x, y, vec in zip(range(len(self.x)), self.x, self.y, self.vec):
			if self.widgets[i] != None:
				CANVAS.delete(self.widgets[i])
			self.widgets[i] = CANVAS.create_line(x, y, x, y+10, fill='orange')
			self.y[i] += vec
			if y > 750 or y < 0:
				self.end.append(i)
		for i in self.end:
			CANVAS.delete(self.widgets[i])
			del self.x[i]
			del self.y[i]
			del self.widgets[i]
			del self.vec[i]
		self.end = []
	def check(self):
		for i, x, y in zip(range(len(self.x)), self.x, self.y):
			if x in my_range(g.a.pos-25, g.a.pos+25) and y > 665:
#			   print("BOOM")
#			   global g
				g.end_game()
				CANVAS.delete(self.widgets[i])
				del self.x[i]
				del self.y[i]
				del self.widgets[i]
				del self.vec[i]
			for s in g.sprites:
				if x in s.x_side and y in s.y_side:
					s.dead = True
					CANVAS.delete(self.widgets[i])
					del self.x[i]
					del self.y[i]
					del self.widgets[i]
					del self.vec[i]
					s.delete()
					g.explosions.append(s.explode())
					g.explosions_rounds.append(0)
					del g.sprites[g.sprites.index(s)]

class game:
	def __init__(self):
		self.val = 0
		self.a = avatar()
		self.s = sprite(self, 100, 100, 'blue')
		self.sh = shots()
		self.sprites = [self.s]
		self.explosions = []
		self.explosions_rounds = []
		self.frames = 0.0
#		s=sprite(0, 0, 'blue')
		self.play()
	def play(self):
		try:
			while 1:
				for s in self.sprites:
					s.move(7, 7)
					if self.frames % 30 == 0:
						s.fire_shot()
					if s.y >= 750:
						s.go_to(100, 100)
				self.a.move()
				self.sh.draw()
				self.val = 0
				self.sh.check()
				self.update_explosions()
				if self.sprites == []:
					self.end_game(outcome="You Win!")
				TK.update()
				self.frames += 1.0
				time.sleep(FRAME_TIME)
		except:
			return
	def update_explosions(self):
		for w, r in zip(self.explosions, range(len(self.explosions_rounds))):
			if self.explosions_rounds[r] < 40:
				self.explosions_rounds[r] += 1
			else:
				CANVAS.delete(w)
	def end_game(self, outcome="Game Over", sprite=None):
		global pos
		if outcome == "Game Over":
			for w in self.a.widgets:
				CANVAS.delete(w)
			CANVAS.create_oval(pos+25, 660, pos-25, 715, outline="orange", fill="orange")
		if sprite != None:
			sprite.delete()
			sprite.explode()
		self.sh.delete()
		for i in range(3):
#		   val=CANVAS.create_text(375, 375, font=("Helvetica", 50), fill="orange", text=outcome)
			val = CANVAS.create_text(375, 375, font=("courier new", 50), fill="white", text=outcome)
			TK.update()
			time.sleep(0.5)
			CANVAS.delete(val)
			TK.update()
			time.sleep(0.5)
		try:
			TK.destroy()
		except:
			pass
global _start
_start = False
def begin(_junk):
	global _start
	_start = True
CANVAS.bind_all('<KeyPress- >', begin)
def begin_menu():
	message = []
	last = ''
	for letter in "galactapi   ":
		message.append((last+letter).strip())
		last = (last+letter).strip()
	#print(message)
	_i = 0
	val1 = None
	while 1:
		global start
		if _i != 0:
			CANVAS.delete(val1)
		else:
			val2 = CANVAS.create_text(375, 285, font=("courier new", 20), fill="white", text="version "+VERSION)
			val3 = CANVAS.create_text(375, 475, font=("courier new", 40), fill="orange", text="Press Space To Play!")
			val4 = CANVAS.create_text(375, 550, font=("courier new", 20), fill="white", text="press return button for instructions")
		val1 = CANVAS.create_text(375, 225, font=("courier new", 70), fill="white", text=message[_i%12])
		_i += 1
		if _start == True:
			global g
			CANVAS.delete(val1)
			CANVAS.delete(val2)
			CANVAS.delete(val3)
			CANVAS.delete(val4)
			g = game()
			g.play()
			break
		else:
			TK.update()
			time.sleep(0.25)
if __name__ == '__main__':
	begin_menu()
