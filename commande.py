import numpy as np
import RPi.GPIO as GPIO


# Deux parties dans ce fichier :

# - la classe commande s'occupe d'allumer ou eteinde le relais en 
# fonction de la temperature de consigne 

# - la calsse consigne s'occupe de lire le fichier consigne_chocolat.txt
# et de mettre a jour la consigne au fure et à mesure que le temps passe


OFF = 'OFF!'
ON = 'ON!'

class command():

	def __init__(self, hysteresis, tgt=21, io=14, fake=False):
		self.h = hysteresis
		self.tgt = tgt
		self.fake = fake
		self.state = OFF
		if not self.fake:
			self.io = io
			GPIO.setmode(GPIO.BCM) 
			GPIO.setup(self.io, GPIO.OUT)
		self._off()
	
	def _toogle(self):
		if self.state == OFF: self.state = ON
		else:  self.state = OFF
		self._set_state()

	def _set_state(self):
		if self.fake:
			print(self.state)
		elif(self.state == OFF):
			GPIO.output(self.io, GPIO.LOW)
		elif(self.state == ON):
			GPIO.output(self.io, GPIO.HIGH)
	
	def _off(self):
		if self.state != OFF:
			self._toogle()

	def _on(self):
		if self.state != ON:
			self._toogle()

	def set_target(self, tgt):
		self.tgt = tgt

	def update(self, curr_tmp):
		if self.state == ON and curr_tmp > self.tgt + self.h:
			self._off()
		elif self.state == OFF and curr_tmp < self.tgt - self.h:
			self._on()


class consigne():

	def __init__(self, fichier='/home/pi/Desktop/consigne_chocolat.txt',
				 hysteresis = .1):
		csv = np.loadtxt(open(fichier), delimiter=';', skiprows=1)
		self.temp = csv[:,1]
		self.tps = csv[:,0]
		self.N, _ = csv.shape
		for i in range(1, self.N):
			self.tps[i] = self.tps[i] + self.tps[i-1]
			
		self.cmd = command(hysteresis = hysteresis, tgt = self.temp[0])
		self.curr_idx = 0
		print('%d s: switching to %d°' % (0, self.temp[self.curr_idx]))

	def run(self, time, temp):
		if hasattr(self, 'done'): return
		if time > self.tps[self.curr_idx]:
			if self.curr_idx < self.N-1:
				self.curr_idx += 1
				print('%d s: switching to %d°' % (time, self.temp[self.curr_idx]))
			else:
				self.done=1
				print('done!')
				self.cmd._off()
		self.cmd.set_target(self.temp[self.curr_idx])
		self.cmd.update(temp)
	
	def clean(self):
		self.cmd._off()
		GPIO.cleanup()
		
		
		
		
