LENGTH = 90.0
STOPPAGE = 3.0
STOPPAGE_STDEV = 1.0
FORM_FACTOR = 100*LENGTH
POINTS_W = 3
POINTS_D = 1
POINTS_L = 0

import random
import matplotlib.pyplot as plt
from time import time
import os, sys, subprocess
from math import exp,factorial


path=str(os.path.dirname(os.path.realpath(sys.argv[0])))
sys.path.append(path+str("/fix_positions.py"))
from fix_positions import *
PPRINT=None
COMP=None

try:
	if(sys.argv[1]=="c"):
		COMP=True
	elif(sys.argv[1]=="p"):
		PPRINT=True
	else:
		pass
except IndexError:
	pass
try:
	if(sys.argv[2]=="c"):
		COMP=True
	elif(sys.argv[2]=="p"):
		PPRINT=True
	else:
		pass
except IndexError:
	pass
if(COMP==None):
	COMP=False
if(PPRINT==None):
	PPRINT=False

random.seed()

def match_length():
	return int(round(LENGTH+abs(random.gauss(STOPPAGE,STOPPAGE_STDEV))))

def load_data(name):
	table=[]
	with open(name, 'r') as file:
		for i,row in enumerate(file):
			if(i==0):
				pass
			else:
				pos,team,played,Wh,Dh,Lh,Fh,Ah,Wa,Da,La,Fa,Aa,W,D,L,F,A,GD,PTS = row.split()
				table.append(	{"Position":pos,
								"Team":team,
								"Played":played,
								"HomeWin":Wh,
								"HomeDraw":Dh,
								"HomeLoss":Lh,
								"HomeFor":Fh,
								"HomeAgainst":Ah,
								"AwayWin":Wa,
								"AwayDraw":Da,
								"AwayLoss":La,
								"AwayFor":Fa,
								"AwayAgainst":Aa,
								"Win":W,
								"Draw":D,
								"Loss":L,
								"For":F,
								"Against":A,
								"GoalDifference":GD,
								"Points":PTS})
	return table

def populate_fixtures(name,TEAMS=20):
	global COMP
	if(COMP):
		make=subprocess.Popen(["g++","-std=c++11",str(path+"/fixturegen.cpp"),"-o", str(path+"/fixturegen")],stdout=subprocess.PIPE)
		print("Compiled fixturegen.cpp")
	while True:
		gen=subprocess.Popen([str(path+"/fixturegen"),str(TEAMS)],stdout=subprocess.PIPE)
		gen_out=str(gen.stdout.read()).replace("\'", "").replace("\\n","\n")[1:]
		if(int(gen_out)==0):
			break
	#print(gen_out)
	table=[]
	with open(name, 'r') as file:
		for i,row in enumerate(file):
			if(i%(int((TEAMS/2+1)))==0):
				pass
			else:
				home,away = row.split()
				try:
					table.append((int(home),int(away)))
				except ValueError:
					pass
	return table

def poisson(mean,k=1):
	return (mean**(k))*exp(-mean)/(factorial(k))

class match:
	def home_team(self):
		return self.home.name
	def away_team(self):
		return self.away.name

	def goals(self,t):
		if(t=="H"):
			return self.home_goals
		else:
			return self.away_goals
	
	def result(self):
		return self.rslt
	
	def goal_difference(self,t):
		if t=="H":
			return self.home_goals-self.away_goals
		elif t=="A":
			return self.away_goals-self.home_goals
		else:
			return 0
	
	def print_result(self):
		return str(self.home.name)+" "+self.home_goals+"-"+self.away_goals+str(self.away.name)
		
	def length(self):
		return self.match_length

	def sim(self):
		self.home_goals=0
		self.away_goals=0
		homeProb=((self.home.get("home_F")+self.away.get("away_A"))/2.0)*self.home.get("Form")
		awayProb=((self.home.get("home_A")+self.away.get("away_F"))/2.0)*self.away.get("Form")
		for i in range(0,self.length()):
			randh=random.random()
			randa=random.random()
			if randh<homeProb:
				self.home_goals+=1
			if randa<awayProb:
				self.away_goals+=1
		if self.home_goals> self.away_goals:
			self.rslt="H"
		elif self.away_goals > self.home_goals:
			self.rslt="A"
		else:
			self.rslt="D"

	def __init__(self,H,A,i):
		self.game_number=i
		self.home_goals=0
		self.away_goals=0
		self.match_length=match_length()
		self.home=H
		self.away=A
		self.rslt="D"
		self.sim()


#alter goal probabilities based on wins
class team:
	def get(self, prop):
		if(prop=="home_F" or prop=="home_A" or prop=="away_F" or prop=="away_A"):
			return self.probability[prop]
		else:
			return self.properties[prop]
	def get_result(self,r):
		return self.results[r].result()
	def set_match(self,r,t):
		self.results.append(r)
		try:
			if t=="H":
				self.properties["For"]+=self.results[-1].goals("H")
				self.properties["Against"]+=self.results[-1].goals("A")
				if self.results[-1].result()=="H":
					self.properties["Points"]+=POINTS_W
					self.properties["Win"]+=1
				elif self.results[-1].result()=="D":
					self.properties["Points"]+=POINTS_D
					self.properties["Draw"]+=1
				else:
					self.properties["Points"]+=POINTS_L
					self.properties["Lose"]+=1

			elif t=="A":
				self.properties["For"]+=self.results[-1].goals("A")
				self.properties["Against"]+=self.results[-1].goals("H")
				if self.results[-1].result()=="A":
					self.properties["Points"]+=POINTS_W
					self.properties["Win"]+=1
				elif self.results[-1].result()=="D":
					self.properties["Points"]+=POINTS_D
					self.properties["Draw"]+=1
				else:
					self.properties["Points"]+=POINTS_L
					self.properties["Lose"]+=1
			else:
				raise ValueError
			self.properties["Played"]+=1
			self.properties["GoalDifference"]=self.properties["For"]-self.properties["Against"]
		except ValueError:
			print("Error ")
			exit

	def set_form(self):
		#implement based on last 5 games, multiplier for goal probabilities if away/home factor?
		if(self.results[-1].home.get("Name")==self.properties["Name"]):
			GD=self.results[-1].goal_difference("H")
		else:
			GD=self.results[-1].goal_difference("A")
		self.properties["Form"]+=GD/FORM_FACTOR

	def set(self,prop,val):
		self.properties[prop]=val

	def __init__(self,table,TEAMS=20):
		self.properties={"Name":table["Team"],"Form":1.0,"Points":0,"For":0,"Against":0,"GoalDifference":0,"Position":0,"Win":0,"Draw":0,"Lose":0,"Played":0}
		self.probability={"home_F":poisson(float(table["HomeFor"])/(LENGTH*(TEAMS-1))),"home_A":poisson(float(table["HomeAgainst"])/(LENGTH*(TEAMS-1))),
					"away_F":poisson(float(table["AwayFor"])/(LENGTH*(TEAMS-1))),"away_A":poisson(float(table["AwayAgainst"])/(LENGTH*(TEAMS-1)))}
		self.results=[]

def populate_teams(table):
	tmp_list=[]
	for i in range(0,len(table)):
		tmp_list.append(team(table[i]))
	return tmp_list
#must edit teams as well
#should populate sequentially
def populate_matches(teams,fixtures,GW=None):
	TEAMS=len(teams)
	if GW==None:
		start=0
		end=TEAMS*(TEAMS-1)
	else:
		start=int((GW-1)*(TEAMS/2))
		end=int(start+(TEAMS/2))
	tmp_list=[]
	for i in range(start,end):
		tmp_list.append(match(teams[fixtures[i][0]],teams[fixtures[i][1]],i))
		teams[fixtures[i][0]].set_match(tmp_list[-1],"H")
		teams[fixtures[i][1]].set_match(tmp_list[-1],"A")
		teams[fixtures[i][0]].set_form()
		teams[fixtures[i][1]].set_form()
		if(GW!=None):#add result
			print(teams[fixtures[i][0]].get("Name")," vs ",teams[fixtures[i][1]].get("Name")," Played")
		if(((i)%(TEAMS/2)==0 and i!=0) or i==(end-1)):
			#fix_positions(teams)
			if(PPRINT):
				input()
				if(i!=end-1):
						print("Game Week ",int(i/(TEAMS/2)))
				else:
					print("Game Week ",(TEAMS-1)*2)
				for j in range(i-int(TEAMS/2),i):
					print(teams[fixtures[j][0]].get("Name")," vs ",teams[fixtures[j][1]].get("Name")," ",tmp_list[j].home_goals,"-",tmp_list[j].away_goals)
	return tmp_list

def print_table(teams):
	#sort by pos pretty print
	fix_positions(teams)
	print("# ","Team ","P "," W"," D"," L"," F"," A"," GD"," Pts")
	index=[x for x in range(0,len(teams))]
	pos=[int(teams[y].get("Position")) for y in range(0,len(teams))]
	index=[x for (y,x) in sorted(zip(pos,index))]
	t=[teams[y] for y in index]
	for i in t:
		print(i.get("Position"),i.get("Name"),i.get("Played"),i.get("Win"),i.get("Draw"),i.get("Lose"),i.get("For"),i.get("Against"),i.get("GoalDifference"),i.get("Points"))

def plot_graphs(teams,matches):
	pass

if __name__=="__main__":
	data=load_data(path+"/data/premtable1415.csv")
	TEAMS = len(data)
	#fixtures=populate_fixtures(path+"/fixtures.csv",TEAMS)
	fixtures=[]
	for i in range(0,20):
		for j in range(0,20):
			if(i!=j):
				fixtures.append((i,j))
	teams=populate_teams(data)
	matches=populate_matches(teams,fixtures)
	print_table(teams)
print([x.get("Position") for x in teams])