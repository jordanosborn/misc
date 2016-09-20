#include <iostream>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <random>

bool contains_reverse(std::vector<std::vector<std::vector<int> > >& pairings, std::vector<int>& pick, int GW, int num_teams=20){
	if(GW>(num_teams-1)){
		return false;
	}
	else{
		bool flag = false;
		for(int i=0; i<pairings.size();i++){
			for(int j=0; j<pairings[i].size();i++){
				if(pairings[i][j]==pick){
					flag=true;
					break;
				}
			}
			if(flag){break;}
		}
		return flag;
	}

}

bool not_played(std::vector<std::vector<int> >& gameweek, std::vector<int> game,int n = 0){
	bool flag=true;
	int count=0;
	for(int i=0;i<gameweek.size();i++){
		if(gameweek[i][0]==game[0] or gameweek[i][0]==game[1] or gameweek[i][1]==game[0] or gameweek[i][1]==game[0]){
			count++;
			if(count>n){
				flag=false;
				break;
			}
			
		}
	}
	return flag;
}

bool played_reverse(std::vector<std::vector<std::vector<int> > >& pairings, std::vector<int>& pick, int GW, int num_teams=20){
	int start,end;
	bool flag=false;
	if(GW<num_teams-1){
		start=0;
		end=pairings.size()/2 - 1;
	}
	else{
		start=pairings.size()/2;
		end=pairings.size()-1;
	}
	for(int i=start;i<=end;i++){
		for(int j=0;j<pairings[i].size();j++){
			if(pairings[i][j]==pick){
				flag=true;
				break;
			}
		}
		if(flag){
			break;
		}
	}
	return flag;
}

bool isIn(std::vector<int>& vec, int i){
	bool flag=false;
	for(int x=0;x<vec.size();x++){
		if(vec[x]==i){
			flag=true;
			break;
		}
	}
	return flag;
}

bool isIn(std::vector<std::vector<std::vector<int> > >& vec, std::vector<int> pick){
	bool flag=false;
	for(int x=0;x<vec.size();x++){
		for(int y=0;y<vec[x].size();y++){
			if(vec[x][y]==pick){
				flag=true;
				break;
			}
		}
		if(flag){break;}
	}
	return flag;
}

int find(std::vector<int>& vec, int i){
	int tmp=-1;
	for(int x=0;x<vec.size();x++){
		if(vec[x]==i){
			tmp=x;
			break;
		}
	}
	return tmp;
}

std::vector<int> redefine(int num_teams=20){
	std::vector<int> tmp;
	for(int i=0;i<num_teams;i++){
		tmp.push_back(i);
	}
	return tmp;
}
std::random_device rd;
std::mt19937 generator(rd());
std::vector<int> rand_pair(int low, int high){
	int a,b;
	std::uniform_int_distribution<int> dist(low,high);
	a=dist(generator);
	while(true){
		b=dist(generator);
		if(a!=b){
			break;
		}
	}
	return std::vector<int>({a,b});
	
}

void print(std::vector<std::vector<int> >& vec){
	for(int i=0; i< vec.size();i++){
		std::cout << vec[i][0] << " " << vec[i][1] << std::endl; 
	}
}
void print(std::vector<int>& vec){
	for(int i=0; i< vec.size();i++){
		std::cout << vec[i] << ","; 
	}
	std::cout << std::endl;
}

void print(std::vector<std::vector<std::vector<int> > >& vec){
	for(int i=0;i<vec.size();i++){
		for(int j =0 ; j<vec[i].size();j++){
			std::cout << vec[i][j][0] << " " << vec[i][j][1] << std::endl;
		}
	}
}

std::vector<std::vector<std::vector<int> > > gen_fixtures(int num_teams=20){
	int iter_count;
    std::vector<int> pick_tmp;
	std::vector<std::vector<int> > reverse_catch;
	std::vector<int> pick;
	int weeks=(num_teams-1)*2;
	int game_week=num_teams/2;
	std::vector<std::vector<std::vector<int> > > pairings;
	std::vector<int> ls;

	for(int i=0;i<weeks;i++){
		pairings.push_back({});
	}

	for(int x =0; x<weeks;x++){
		ls=redefine();
		for(int y =0; y<game_week; y++){
			iter_count=0;
			while(ls.size()>0){
				pick_tmp=rand_pair(0, ls.size()-1);
				pick={ls[pick_tmp[0]],ls[pick_tmp[1]]};
				//std::cout << pick[0] << "," << pick[1] << std::endl;
				//getchar();
				if( !(contains_reverse(pairings,pick,x,num_teams)) and (isIn(ls,pick[0])) and (isIn(ls,pick[1])) and (not isIn(pairings,pick))){
					pairings[x].push_back({pick[0],pick[1]});
					ls.erase(ls.begin()+find(ls,pick[0]));
					ls.erase(ls.begin()+find(ls,pick[1]));
					break;
				}
				iter_count++;
				if(iter_count>5){
					reverse_catch.push_back({pick[0],pick[1]});
					ls.erase(ls.begin()+find(ls,pick[0]));
					ls.erase(ls.begin()+find(ls,pick[1]));
					break;
				}
			}
		}
	}
	/*std::vector<int> count={0,0,0,0,0,0,0,0,0,0};
	for(int i=0; i<pairings.size();i++){
		if(pairings[i].size()<game_week){
			count[(game_week-1)-pairings[i].size()]+=1;
		}
	}
	print(count);*/

	int iter=0;
	for(int i=0;i<pairings.size();i++){
		iter=0;
		while(pairings[i].size()!=game_week){
			for(int j=0;j<reverse_catch.size();j++){
				//less than game_week might be implicitly checked by not_played
				//getchar();
				//std::cout <<i <<"," << not_played(pairings[i],reverse_catch[j]) << "," << (not played_reverse(pairings,reverse_catch[j],i,num_teams)) << std::endl;
				if(not_played(pairings[i],reverse_catch[j]) and (not played_reverse(pairings,reverse_catch[j],i,num_teams)) ){
					pairings[i].push_back(reverse_catch[j]);
					reverse_catch.erase(reverse_catch.begin()+j);
					break;
				}
			}
			iter++;
			if(iter>game_week){
				break;
			}
		}
		
	}
	iter=0;
	for(int i=0;i<pairings.size();i++){
		iter=0;
		while(pairings[i].size()!=game_week){
			for(int j=0;j<reverse_catch.size();j++){
				//less than game_week might be implicitly checked by not_played
				//getchar();
				//std::cout <<i <<"," << not_played(pairings[i],reverse_catch[j]) << "," << (not played_reverse(pairings,reverse_catch[j],i,num_teams)) << std::endl;
				if(not_played(pairings[i],reverse_catch[j],1) ){//and (not played_reverse(pairings,reverse_catch[j],i,num_teams)) ){
					pairings[i].push_back(reverse_catch[j]);
					reverse_catch.erase(reverse_catch.begin()+j);
					break;
				}
			}
			iter++;
			if(iter>game_week){
				break;
			}
		}
		
	}
	
	std::cout << reverse_catch.size() << std::endl;
	//pairings.push_back(reverse_catch);
	return pairings;
}

void write(std::vector<std::vector<std::vector<int> > >&p ,std::string name,int num=20){
	std::ofstream file;
	file.open("fixtures.csv",std::ios::out | std::ios::trunc);
	file << "Home\tAway" << "\n"; 
	for(int i=0;i<p.size();i++){
		for(int j=0;j<p[i].size();j++){
			file << p[i][j][0] << "\t" <<p[i][j][1] << "\n";
		}
		file << "GW\t" << i << std::endl;
	}
	file.close();
}



int main(int argc, char* argv[]){
	int num=20;
	if(argc>1){
		num=std::atoi(argv[1]);
	}
	std::vector<std::vector<std::vector<int> > > fixtures= gen_fixtures(num);
	write(fixtures,"fixtures.csv",num);
	return 0;
}