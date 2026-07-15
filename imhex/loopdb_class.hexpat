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

import std.io;
import std.mem;

enum ComparisonType : u16 {
    //Bitmasking enabled comparison enum
    //        < = >
    FALSE,  //0 0 0
    GT,     //0 0 1
    EQ,     //0 1 0
    GEQ,    //0 1 1
    LT,     //1 0 0
    NEQ,    //1 0 1
    LEQ,    //1 1 0
    TRUE,   //1 1 1
    C_UNK,
};
struct Entry {
    u64 loop_id;
    u64 start;
    u64 finish;
    u64 stride;
    u64 exact_exit_count;
    u64 const_max_exit_count;
    ComparisonType comp_type;
    bool isAscending;
    bool loopTerminates;
    bool hasIsAscending;
    bool hasStart;
    bool hasFinish;
    bool hasStride;
    bool hasLoopTerminates;
    bool hasExactExitCount;
    bool hasConstMaxExitCount;
    bool hasTranslationTableStart;
    bool hasTranslationTableFinish;
    bool hasTranslationTableStride;
};
struct MasterHeader {
    u32 function_pointer;
    u32 function_length;
    u64 entry_count;
    Entry entries[entry_count];
};
// newest comment
MasterHeader headers[while($ < std::mem::size())] @ 0x0;