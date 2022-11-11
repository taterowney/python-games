from rand import *
from random import random,randint,seed
import tk3
from tkinter import *

def create_terrain(s):
#	seed(rand_int(0,100))
	seed(s)
	start_pos=randint(100,150)
	begin=random()
	if begin < 0.33:
		last='down'
	elif begin > 0.66:
		last='up'
	else:
		last='same'
	prev_pos=start_pos
	terrain=[start_pos]
	for i in range(1,1000):
		val=random()
		if last=='down':
			if val < 0.8:
				dir='down'
				new=prev_pos-1
			elif val > 0.9:
				dir='up'
				new=prev_pos+1
			else:
				dir='same'
				new=prev_pos
		if last=='same':
			if val < 0.8:
				dir='same'
				new=prev_pos
			elif val > 0.9:
				dir='up'
				new=prev_pos+1
			else:
				dir='down'
				new=prev_pos-1
		if last=='up':
			if val < 0.8:
				dir='up'
				new=prev_pos+1
			elif val > 9.0:
				dir='down'
				new=prev_pos-1
			else:
				dir='same'
				new=prev_pos
		terrain.append(new)
		prev_pos=new
		last=dir
	return terrain
#print(terrain,dirs)

def create_background():
#	tk,canvas=tk3.setup(1000,500)
	terrain=create_terrain(5)
	return terrain
def bkrnd(canvas,terrain):
	canvas.create_rectangle(0,0,1000,500,outline='#3191e1',fill='#3191e1')
	for index,t in enumerate(terrain):
		canvas.create_line(index,500,index,500-t,fill='grey')

if __name__ == '__main__':
	tk=Tk()
	canvas=Canvas(tk,width=500,height=500)
	canvas.pack()
	bkrnd(canvas,create_background())
