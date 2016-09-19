import random

random.seed()

def contains_reverse(pairings,pick,GW,num_teams=20):
	if GW>num_teams-1:
		return False
	else:
		flag=False
		for e in pairings:
			if (e[1],e[0])==pick:
				flag=True
				break
		return flag

def rand_pair(m,M):
	a=random.randint(m,M);
	while True:
		b=random.randint(m,M)
		if a!=b:
			break
	return (a,b)

def gen_fixtures(num_teams=20):
	weeks=int((num_teams-1)*2)
	game_week=int(num_teams/2)
	pairings=[]
	tmp_list=[]
	used=[]
	for i in range(0,num_teams):
		for j in range(0,num_teams):
			if(j==i):
				pass
			else:
				tmp_list.append((i,j))
	for x in range(0,weeks):
		ls=[p for p in range(0,num_teams)]
		for y in range(0,game_week):
			while True:
				rand_int=random.randint(0,len(tmp_list)-1)
				pick=tmp_list[rand_int]
				if (not contains_reverse(pairings,pick,x+1,num_teams)) and (pick[0] in ls) and (pick[1] in ls) and (rand_int not in used):
					pairings.append(pick)
					ls.remove(pick[0])
					ls.remove(pick[1])
					used.append(rand_int)
					del tmp_list[rand_int]
					break
		print(pairings)
		
	
gen_fixtures(10)


