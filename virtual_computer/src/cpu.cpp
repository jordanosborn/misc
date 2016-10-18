#include "cpu.h"

#include <iostream>

namespace cs{
    std::map<std::string,uint8_t> op_codes={{"ADD",0x00}};

    cpu::cpu(uint speed, uint ssize,memory_map &mm){
        clock_speed=speed;
        stack_size=ssize;
        bit_size=sizeof(uint)*8;
        program_counter = 0x0;
        registers={{"A",0x0},{"B",0x0},{"C",0x0},{"D",0x0},{"E",0x0},{"F",0x0},
                    {"G",0x0},{"H",0x0},{"I",0x0},{"J",0x0},{"K",0x0},{"L",0x0},
                     {"M",0x0},{"N",0x0},{"O",0x0},{"P",0x0}};    
        read=0;
        zero=0;
        carry=0;
        interrupt=0;
        mmap=&mm;

    }
    void cpu::increment_pc(){
        program_counter+=1;
    }
    void cpu::set_pc(uint val){
        program_counter=val;
    }
    cpu::~cpu(){}


};
int main(int argc, char* argv[]){
    cs::memory_map y;
    cs::cpu x(10000,1,y);
    std::cout << &x.clock_speed <<" "  << x.clock_speed <<std::endl;
        return 0;
    }

