from math import ceil, log,floor
from matplotlib import pyplot as pplt
from random import randint
#p lose all rounds always less than p0
p0=0.01
p=18/38

N=log(p0)/log(1-p)
T=100
S=0
for i in range(1,ceil(N)+1): 
	S+=2**(i-1)
B=T/S
print("Amount to bet initially: ", round(B,2))
print("Number of failed bets allowed: " , ceil(N))
S=0
for i in range(1,ceil(N)+1): 
	S+=B*2**(i-1)
print("Total Money:",round(S,2))
print("Probability lose all rounds: ", (1-p)**ceil(N))

#per round
exp_gain=p*B+(1-p)*(-B)
proportion = exp_gain/B
print(proportion)

def color(a):
	if a==-1:
		return '00'
	elif a==0:
		return '0'
	elif a%2!=0 and a!=None:
		return 'r'
	elif a!=None:
		return 'b'
	else:
		return "ERROR"
class roulette:
	#decimal odd
	def __init__(self): 
		self.bet_type = {"A":36,"B":18,"C":12,"D":9,"E":7,"F":6,"G":3,"H":3,"I":2,"J":2,"K":2,"L":2,"M":18}
		self.value=None
	def spin():
		self.value=randint(-1,36)
	def is_winner(char, value=None):
		pass

class roller:
	def __init__(self,money,style):#cautious, moderate, aggressive
		self.style=style
		self.total=money
		self.bets={"A":[],"B":[],"C":[],"D":[],"E":[],"F":[],"G":[],"H":[],"I":[],"J":[],"K":[],"L":[],"M":[]}

	def add_bet(self):
		pass
	def ideal_bet(self):
		pass

class system:
	def __init__(self):
		pass
	def add_roller(self,money,style):
		pass
	def add_table(self):
		pass
	def start():
		pass


