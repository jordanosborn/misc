#ifndef MEMORY_MAP_H
#define MEMORY_MAP_H
#include <vector>
//#include "peripherals.h"
//#include "memory.h"



namespace cs{
typedef uint8_t byte;
typedef uint32_t uint;


class memory_map{
    private:
        std::vector<uint> memory_addr; //beginning 
        std::vector< std::vector<byte>* > memory_arr;
    public:
        memory_map();
        ~memory_map();
       // void add_ram(ram&);
        //void add_rom(rom&);
       // void add_hdd(hdd&);
        //void add_keyboard(keyboard&);
        //void add_screen(screen&);
       // void add_speaker(speaker&);
        void set_memory(uint,uint); //if memory_addr[i]<=uint a<memory_addr[i+1] *(memory_arr[i][i-memory_addr[i]])=uint b;
        byte get_memory(uint);

};


};

#endif
