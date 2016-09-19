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

random.seed()

def match_length():
	return LENGTH+abs(random.gauss(STOPPAGE,STOPPAGE_STDEV))

def select_picks(TEAMS):
	pairings=[]
	game_week=TEAMS/2.0
	tlp=[]
	for i in range(0,TEAMS*(TEAMS-1)):
		ls=[x for x in range(0,TEAMS)]
		if a<=int(TEAMS*(TEAMS-1.0)/2.0)
			for i in range(0,game_week):
				while True:
					rand1=random.randint(0,len(ls))

					rand2=random.randint(0,len(ls))
					pick=()
					if doesnt_contain_reverse(pairings,pick):
						pairings.append(pick)
						del ls[]
		else:



def doesnt_contain_reverse(ls,pick):
	flag=True
	for element in ls:
		if (element[1],element[0]) == pick:
			flag= False
			break
	return flag

def not_played_GW(pairings,pick,TEAMS):
	a=len(pairings)
	games=TEAMS/2.0
	start=int(int(a/games)*TEAMS/2.0)
	end=int(start+a%int(games))
	flag=True
	for p in pairings[start:end]:
		print(p,pick)
		input()
		if(p[0]==pick[0] or p[0]==pick[1] or p[1]==pick[0] or p[1]==pick[1]):
			flag=False
			break
	print(flag)
	return flag


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

def populate_fixtures(TEAMS=20):
	pairings=[]
	tmp_list=[]
	used=[]
	for i in range(0,TEAMS):
		for j in range(0,TEAMS):
			if(j==i):
				pass
			else:
				tmp_list.append((i,j))
	while len(tmp_list)>0:
		while True:
			rand_int=random.randint(0,len(tmp_list)-1)
			
			pick=tmp_list[rand_int]
			if len(tmp_list)<=int(TEAMS*(TEAMS-1.0)/2.0) and not_played_GW(pairings,pick,TEAMS):
				pairings.append(pick)
				del tmp_list[rand_int]
				break
			else:
				if doesnt_contain_reverse(pairings,pick) and not_played_GW(pairings,pick,TEAMS):
					#print(rand_int,len(tmp_list))
					pairings.append(pick)
					del tmp_list[rand_int]
					break
	return pairings

def fix_positions(teams):
	pass

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

class team:
	def get(self, prop):
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
		except ValueError:
			print("Error ")
			exit

	def set_form(self):
		#implement based on last 5 games, multiplier for goal probabilities if away/home factor?
		if(self.results[-1].home.get("Name")==self.properties["Name"]):
			GD=self.results[-1].goal_difference("H")
		else:
			GD=self.results[-1].goal_difference("H")
		self.properties["Form"]+=GD*FORM_FACTOR

	def set(self,prop,val):
		self.properties[prop]=val

	def __init__(self,name,HF,HA,AF,AA,TEAMS=20):
		self.properties={"Name":name,"Form":1.0,"Points":0,"For":0,"Against":0,"Position":0,"Win":0,"Draw":0,"Lose":0,"Played":0}
		self.probability={"home_F":float(HF)/(LENGTH*(TEAMS-1)),"home_A":float(HA)/(LENGTH*(TEAMS-1)),
					"away_F":float(AF)/(LENGTH*(TEAMS-1)),"home_A":float(AA)/(LENGTH*(TEAMS-1))}
		self.results=[]

def populate_teams(table):
	tmp_list=[]
	for i in range(0,len(table)):
		tmp_list.append(team(table[i].get("Team"),table[i].get("HomeFor"),table[i].get("HomeAgainst"),table[i].get("AwayFor"),table[i].get("AwayAgainst")))
	return tmp_list
#must edit teams as well
#should populate sequentially
def populate_matches(teams,fixtures,GW=None):
	if GW==None:
		start=0
		end=len(teams)*(len(teams)-1)
	else:
		start=int((GW-1)*(len(teams)/2))
		end=int(start+(len(teams)/2))
	tmp_list=[]
	for i in range(start,end):
		tmp_list.append(match(teams[fixtures[i][0]],teams[fixtures[i][1]],i))
		teams[fixtures[i][0]].set_match(tmp_list[-1],"H")
		teams[fixtures[i][1]].set_match(tmp_list[-1],"A")
		teams[fixtures[i][0]].set_form()
		teams[fixtures[i][1]].set_form()

		print(teams[fixtures[i][0]].get("Name")," vs ",teams[fixtures[i][1]].get("Name")," Played")
	return tmp_list

def print_table(teams):
	#sort by pos
	for i in teams:
		print(i.get("Position"),i.get("Name"),i.get("Played"),i.get("Win"),i.get("Draw"),i.get("Lose"),i.get("For"),i.get("Against"),i.get("Points"))

def plot_graphs(teams,matches):
	pass

data=load_data("data/premtable1415.csv")
TEAMS = len(data)
fixtures=populate_fixtures(TEAMS)
teams=populate_teams(data)
matches=populate_matches(teams,fixtures,5)
print_table(teams)

