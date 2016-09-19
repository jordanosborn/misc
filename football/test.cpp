#include <iostream>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <random>

bool contains_reverse(std::vector<std::vector<int> >& pairings, std::vector<int>& pick, int GW, int num_teams=20){
	if(GW>(num_teams-1)){
		return false;
	}
	else{
		bool flag = false;
		for(int i=0; i<pairings.size();i++){
			if(pairings[i]==pick){
				flag=true;
				break;
			}
		}
		return flag;
	}

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

bool isIn(std::vector<std::vector<int> >& vec, std::vector<int> pick){
	bool flag=false;
	for(int x=0;x<vec.size();x++){
		if(vec[x]==pick){
			flag=true;
			break;
		}
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

std::vector<std::vector<int> > gen_fixtures(int num_teams=20){
	int iter_count;
    std::vector<int> pick_tmp;
	std::vector<std::vector<int> > reverse_catch;
	std::vector<int> pick;
	int weeks=(num_teams-1)*2;
	int game_week=num_teams/2;
	std::vector<std::vector<int> > pairings;
	std::vector<int> ls;

	for(int x =0; x<weeks;x++){
		ls=redefine();
		for(int y =0; y<game_week; y++){
			iter_count=0;
			while(true){
				pick_tmp=rand_pair(0, ls.size()-1);
				pick={ls[pick_tmp[0]],ls[pick_tmp[1]]};
				//std::cout << pick[0] << "," << pick[1] << std::endl;
				//getchar();
				if( !(contains_reverse(pairings,pick,x,num_teams)) and (isIn(ls,pick[0])) and (isIn(ls,pick[1])) and (not isIn(pairings,pick))){
					pairings.push_back({pick[0],pick[1]});
					ls.erase(ls.begin()+find(ls,pick[0]));
					ls.erase(ls.begin()+find(ls,pick[1]));
					break;
				}
				iter_count++;
				if(iter_count>5){
					reverse_catch.push_back({pick[0],pick[1]});
					break;
				}
			}
		}
	}
	
	//print(pairings);
	std::cout << pairings.size() << std::endl;
	std::cout << reverse_catch.size() << std::endl;
	for(int i =0; i<reverse_catch.size();i++){
		pairings.push_back(reverse_catch[i]);
	}
	return pairings;
}

void write(std::vector<std::vector<int> >&p ,std::string name,int num=20){
	std::ofstream file;
	file.open("fixtures.csv",std::ios::out | std::ios::trunc);
	for(int i=0;i<p.size();i++){
		file << p[i][0] << "," <<p[i][1] << std::endl;
	}
	file.close();
}



int main(int argc, char* argv[]){
	int num=20;
	if(argc>1){
		num=std::atoi(argv[1]);
	}
	std::vector<std::vector<int> > fixtures= gen_fixtures(num);
	write(fixtures,"fixtures.csv",num);
	return 0;
}