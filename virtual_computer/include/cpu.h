#ifndef CPU_H
#define CPU_H

#include <map>
#include <vector>
#include <stack>
#include <cstdlib>
#include "memory_map.h"

namespace cs{

extern std::map<std::string,uint8_t> op_codes;
class cpu{
    public:
        uint program_counter;
        uint address;
        uint data;
        uint clock_speed;
        bool read;
        bool zero;
        bool carry;
        bool interrupt;
        uint bit_size;
        uint stack_size; 
        std::stack<byte> stack;
        memory_map *mmap;
        std::map<std::string,uint> registers;
    public:
        cpu(uint,uint,memory_map&);
        void start();
        void operation(byte);
        void increment_pc();
        void set_pc(uint);
        void set_register(std::string,uint);
        void write_address(uint,uint);
        void read_address(uint,uint);
        uint combine_bytes(byte[4]);
        void reset();
        void sleep();
        void shutdown();
        
        ~cpu();

};
}


#endif
