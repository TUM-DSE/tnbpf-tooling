// Enter your pattern code here and click on the Play button
// below to execute your code. The results will then be visible
// in the Pattern Data view.
// 
// More information can be found in the documentation.
// 
// 
// Simple example:
// 
// import std.io;
// 
// struct Pattern {
//     u32 int;
//     float floating_point;
// };
// 
// Pattern my_pattern @ 0x00;
// std::print("0x{:08X}", my_pattern.int);

#include "std/mem.pat"

import type.magic;
import std.io;
import std.mem;

enum EntryTypes : u64 {
    Inst,
    Const,
    Arg
};

struct InstructionDependency {
    u64 inst_tag_id;
};
struct ConstantDependency {
    u64 constval_size;
    if (constval_size == 1) {
        u8 uint8_data;
    } else if (constval_size == 2) {
        u16 uint16_data;
    } else if (constval_size == 4) {
        u32 uint32_data;
    } else if (constval_size == 8) {
        u64 uint64_data;
    } else {
        u8 misc_data[constval_size];
    }
};
struct ArgumentDependency {
    u64 arg_no;
};

struct Dependency {
    EntryTypes type;
    if (type == EntryTypes::Inst) {
        InstructionDependency inst_dep;
    } else if (type == EntryTypes::Const) {
        ConstantDependency const_dep;
    } else {
        ArgumentDependency arg_dep;
    }
};
enum BoundType : u64 {
    Start,
    Finish,
    Stride
};
struct LoopEntry {
    u64 loopid;
    BoundType bound_type;
    
    std::string::SizedString<u64> format_string;
    u64 dependency_count;
    Dependency deps[dependency_count];
};
struct MasterHeader {
    u32 function_pointer;
    u32 function_length;
    u64 entry_count;
    LoopEntry entries[entry_count];
};
MasterHeader headers[while($ < std::mem::size())] @ 0x0;