class team:
	def get(self,prop):
		return self.properties[prop]
	def set(self,prop,val):
		self.properties[prop]=val
	def __init__(self,pts,gd,fo):
		self.properties={"Points":int(pts),"GoalDifference":int(gd),"For":int(fo),"Position":int(0)}

def print_table(teams):
	#sort by pos pretty print
	print("#"," F"," GD"," Pts")
	index=[x for x in range(0,len(teams))]
	pos=[int(teams[y].get("Position")) for y in range(0,len(teams))]
	index=[x for (y,x) in sorted(zip(pos,index))]
	t=[teams[y] for y in index]
	for i in t:
		print(i.get("Position"),i.get("For"),i.get("GoalDifference"),i.get("Points"))

def sort(ls,ls2):
	copy=[0]*len(ls2)
	length=len(ls)
	a=ls[:]
	b=ls2[:]
	b.sort()
	#fr=0
	fr=[]
	to=[]

	while(len(fr)<length):
		k=max(a)
		for i in range(0,length):
			if(ls[i]==k and (i not in fr)):
				fr.append(i)
				a.remove(k)
				break
	for k,i in enumerate(fr):
		copy[i]=b[k]
	#print(fr)
	"""for i in range(0,len(a)):
		for j in range(0,len(ls)):
			if a[i]==ls[j]:
				fr=j
				break;
		copy[fr]=b[i]"""
	return copy

def fix_positions(teams):
	index=[x for x in range(0,len(teams))]
	pts=[int(teams[y].get("Points")) for y in range(0,len(teams))]
	index=[x for (y,x) in sorted(zip(pts,index))]
	index.reverse()
	for i in range(0,len(teams)):
		teams[index[i]].set("Position",i+1)
	
	points=0
	points_prev=teams[index[0]].get("Points")
	position=[]
	sorted_pos=[]
	gd=[]
	
	for i,pos in enumerate(index):
		points=teams[pos].get("Points")
		if points==points_prev:
			position.append(pos)
			sorted_pos.append(teams[pos].get("Position"))
			gd.append(teams[pos].get("GoalDifference"))
		elif len(position)>1:
			#sort is problem should be [1, 5, 6, 3, 4, 2]
			und=sort(gd,sorted_pos)
			print(und)
			for p in range(0,len(position)):
				teams[position[p]].set("Position",und[p])
			sorted_pos=[]
			position=[]
			gd=[]
			points_prev=points
			position.append(int(teams[pos].get("Position")))
			gd.append(int(teams[pos].get("GoalDifference")))
			sorted_pos.append(pos)
		else:
			sorted_pos=[]
			position=[]
			gd=[]
			points_prev=points
			position.append(int(teams[pos].get("Position")))
			gd.append(int(teams[pos].get("GoalDifference")))
			sorted_pos.append(pos)

	#check order then to create new index then do goalsfor



			
"""teams=[team(15,2,5),team(20,8,2),team(15,8,5),team(20,8,5),team(10,6,4),team(20,1,4),team(20,30,4)]
fix_positions(teams)
print_table(teams)
a=[30, 1, 6, 8, 16, 8]
b=[1, 2, 3, 4, 5, 6]
print(sort(a,b))

print([1,6,5,3,2,4])"""


"""goald=0
	goald_prev=int(teams[0].get("GoalDifference"))
	sorted_gd=[]
	gd=[]
	pt=0
	pt_prev=int(teams[0].get("Points"))
	sorted_pts=[]
	for j,i in enumerate(index):
		pt=int(teams[i].get("Points"))
		goald=int(teams[i].get("GoalDifference"))
		if pt==pt_prev and goald==goald_prev:
			#print(pt)
			sorted_gd.append(int(teams[i].get("Position")))
			gd.append(int(teams[i].get("For")))
			sorted_pts.append(i)
		else:
			pt_prev=pt
			goald_prev=goald
			sorted_gd=[x for (y,x) in sorted(zip(gd,sorted_gd))]
			sorted_gd.reverse()
			for k,inde in enumerate(sorted_pts):
				teams[inde].set("Position",sorted_gd[k])
				print("l")
			sorted_gd=[]
			gd=[]
			sorted_pts=[]
			pt=-1
			goald=-1
			
			if(j<len(teams)):
				sorted_gd.append(int(teams[i].get("Position")))
				gd.append(int(teams[i].get("For")))
				sorted_pts.append(i)
"""		