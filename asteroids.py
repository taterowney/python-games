from tk3 import *
tk,canvas=setup(700,700)
bkrnd=canvas.create_rectangle(0,0,700,700,outline='black',fill='black')
import time,random
from math import sin,cos,tan
directions=[1,0,-1,0]

class sprite:
	def __init__(self,game,location,start_x_vector,start_y_vector,size='small'):
		self.x_vector=start_x_vector
		self.y_vector=start_y_vector
		self.size=size
		self.index=len(game.sprites)
		game.sprites.append(self)
		if self.size=='small':
			self.y_vector*=10
			self.x_vector*=10
			self.size_mod=10
		if self.size=='medium':
			self.x_vector*=8
			self.y_vector*=8
			self.size_mod=20
		if self.size=='large':
			self.x_vector*=6
			self.y_vector*=6
			self.size_mod=30
		self.x=location[0]
		self.y=location[1]
		self.x_side=my_range(self.x,self.x+self.size_mod)
		self.y_side=my_range(self.y,self.y+self.size_mod)
		self.widgets=[]
		self.destroyed=False
		self.draw()
	def explode(self):
		self.delete()
#		print('triggered')
		del g.sprites[self.index]
		if self.size=='large':
			self.x_vector/=6
			self.y_vector/=6
			create_new(self,'medium')
			self.destroyed=True
		if self.size=='medium':
			self.x_vector/=8
			self.y_vector/=8
			create_new(self,'small')
			self.destroyed=True
		if self.size=='small':
			self.destroyed=True
	def delete(self):
		for w in self.widgets:
			canvas.delete(w)
	def draw(self):
		print(self.destroyed)
		if self.size=='small' and self.destroyed==True:
			raise TypeError('annoying thing happened in round %s'% g.round)
		if not self.destroyed:
			self.delete()
			self.widgets=[canvas.create_oval(self.x,self.y,self.x+self.size_mod,self.y+self.size_mod,outline='white',fill='white')]
#			if random.random() > 0.75:
#				self.x_vector=random.randint(-5,5)*5
#			if random.random() > 0.75:
#				self.y_vector=random.randint(-5,5)*5
			self.x+=self.x_vector
			self.y+=self.y_vector
			if self.x > 700:
				self.x=0
			if self.x < 0:
				self.x=690
			if self.y > 700:
				self.y=0
			if self.y < 0:
				self.y=690
			self.x_side=my_range(self.x,self.x+self.size_mod)
			self.y_side=my_range(self.y,self.y+self.size_mod)
#			print(self.x,self.y)

def create_new(a,size):
	x_1=-int(a.x_vector)
	y_1=int(a.y_vector)
	x_2=int(a.x_vector)
	y_2=-int(a.y_vector)
	s1=sprite(g,[a.x,a.y],x_1,y_1,size=size)
	s2=sprite(g,[a.x,a.y],x_2,y_2,size=size)
#	print('splitting')

class avatar:
	def __init__(self):
		self.x=350
		self.y=350
		self.theta=60
		canvas.bind_all('<KeyPress-Left>',self.turn)
		canvas.bind_all('<KeyPress-Right>',self.turn)
		canvas.bind_all('<KeyPress-Down>',self.thrust)
		canvas.bind_all('<KeyPress-Up>',self.fire)
		self.widgets=[]
		self.draw()
	def fire(self,event):
		b=bullet(self.x,self.y,(self.theta+180) % 360)
	def delete(self):
		for w in self.widgets:
			canvas.delete(w)
	def explode(self):
		self.delete()
		canvas.create_text(350,350,font=('Helvetica',30),text='GAME  OVER',fill='white')
		tk.update()
		time.sleep(2)
		tk.destroy()
	def draw(self):
		self.delete()
		xval1,yval1=get_polar_coords(self.x,self.y,self.theta,15)
		xval2,yval2=get_polar_coords(self.x,self.y,self.theta-20,15)
		self.x_side=my_range(int(self.x),int(self.x+16))
		self.y_side=my_range(int(self.y),int(self.y+16))
#		self.x_side=[]
#		self.y_side=[]
#		for i in range(15):
#			x,y=get_polar_coords(self.x,self.y,self.theta,i)
#			self.x_side.append(x)
#			self.y_side.append(y)
		self.widgets=[canvas.create_polygon(self.x,self.y,xval1,yval1,xval2,yval2,outline='white',fill='white')]
	def thrust(self,event):
		self.x,self.y=get_polar_coords(self.x,self.y,(self.theta+180) % 360,30)
		if self.x > 700:
			self.x=700
		if self.x < 0:
			self.x=0
		if self.y > 700:
			self.y=700
		if self.y < 0:
			self.y=0
	def turn(self,event):
		if event.keysym=='Left':
			self.theta+=15
		elif event.keysym=='Right':
			self.theta-=15

class bullet:
	def __init__(self,x,y,theta):
		self.theta=theta
		self.x=x
		self.y=y
		add_bullet(self)
		self.widgets=[]
#		print(self.theta)
		self.draw()
	def delete(self):
		for w in self.widgets:
			canvas.delete(w)
	def draw(self):
		xval,yval=get_polar_coords(self.x,self.y,self.theta,20)
		self.x=xval
		self.y=yval
		xval,yval=get_polar_coords(self.x,self.y,self.theta,5)
		self.delete()
#		print(self.x,self.y,xval,yval)
		self.widgets=[canvas.create_line(self.x,self.y,xval,yval,fill='white')]
		x_val,y_val=get_polar_coords(self.x,self.y,self.theta,80)
		val1,val2=int(self.x),int(x_val)
		val3,val4=int(self.x),int(x_val)
		self.x_side=my_range(val2,val1)
		self.y_side=my_range(val4,val3)
#		print(int(self.x),int(xval))
#		print(self.x_side)

def add_bullet(b):
	g.bullets.append(b)

def get_polar_coords(x,y,theta,hyp):
        opposite=sin(radians(theta))*hyp
        aj=cos(radians(theta))*hyp
#       canvas.create_line(x,y,x+aj,y-opposite)
        return x+aj, y+opposite

def my_range(val1,val2):
	ret=[]
	if val2>val1:
		for i in range(val1,val2):
#			print('triggered')
			ret.append(i)
	else:
		for i in range(val2,val1):
#			print('triggered')
			ret.append(i)
	return ret

class game:
	def __init__(self):
		self.bullets=[]
		self.sprites=[]
		s1=sprite(self,[900,700],1,1,size='large')
#		s2=sprite(self,[250,250],-1,1,size='large')
#		s3=sprite(self,[450,150],-1,-1,size='medium')
		self.a=avatar()
		self.round=0
		self.main()
	def main(self):
		tk.update()
		self.round+=1
#		print(self.bullets)
#		time.sleep(0.025)
		for s in self.sprites:
			print('triggered')
			s.draw()
#		s2.draw()
#		s3.draw()
		self.a.draw()
		self.update_bullets()
		self.rm_shots()
		self.check_collisions()
		print()
		print(len(self.sprites))
		tk.after(50,self.main)
	def check_collisions(self):
#		print(len(self.sprites))
		for b in self.bullets:
#			print(b.x_side)
			for x,y in zip(b.x_side,b.y_side):
				for s in self.sprites:
#					print(s.x_side,s.y_side)
					if x in s.x_side and y in s.y_side:
						if not s.destroyed:
							print('KABOOM')
							s.explode()
		for s in self.sprites:
#			print(s.x,s.y)
			for x in s.x_side:
				for y in s.y_side:
					for a_x,a_y in zip(self.a.x_side,self.a.y_side):
						if a_x==x and a_y==y:
							self.a.explode()
	def update_bullets(self):
		for b in self.bullets:
			b.draw()
	def rm_shots(self):
		for index,b in enumerate(self.bullets):
			if b.x > 700 or b.x < 0 or b.y > 700 or b.y < 0:
				del self.bullets[index]

if __name__ == '__main__':
#	print(my_range(0,10))
	g=game()
