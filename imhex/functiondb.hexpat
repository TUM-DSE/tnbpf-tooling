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

enum TypeID : u64 {
    // PrimitiveTypes
    HalfTyID = 0,  ///< 16-bit floating point type
    BFloatTyID,    ///< 16-bit floating point type (7-bit significand)
    FloatTyID,     ///< 32-bit floating point type
    DoubleTyID,    ///< 64-bit floating point type
    X86_FP80TyID,  ///< 80-bit floating point type (X87)
    FP128TyID,     ///< 128-bit floating point type (112-bit significand)
    PPC_FP128TyID, ///< 128-bit floating point type (two 64-bits, PowerPC)
    VoidTyID,      ///< type with no size
    LabelTyID,     ///< Labels
    MetadataTyID,  ///< Metadata
    X86_AMXTyID,   ///< AMX vectors (8192 bits, X86 specific)
    TokenTyID,     ///< Tokens

    // Derived types... see DerivedTypes.h file.
    IntegerTyID,        ///< Arbitrary bit width integers
    ByteTyID,           ///< Arbitrary bit width bytes
    FunctionTyID,       ///< Functions
    PointerTyID,        ///< Pointers
    StructTyID,         ///< Structures
    ArrayTyID,          ///< Arrays
    FixedVectorTyID,    ///< Fixed width SIMD vector type
    ScalableVectorTyID, ///< Scalable SIMD vector type
    TypedPointerTyID,   ///< Typed pointer used by some GPU targets
    TargetExtTyID,      ///< Target extension type
  };

struct TypeForm {
    TypeID type_id;
    if (type_id == TypeID::IntegerTyID) {
        u64 int_bit_width;
    } else if (type_id == TypeID::ByteTyID) {
        u64 byte_bit_width;
    } else if (type_id == TypeID::FunctionTyID) {
        u64 isVarArg;
        TypeForm return_type;
        u64 param_count;
        TypeForm param_types[param_count];
    } else if (type_id == TypeID::StructTyID) {
        u64 is_packed;
        u64 is_opaque;
        if (is_opaque == 0) {
            u64 struct_entry_count;
            TypeForm struct_entries[struct_entry_count];
        }
    } else if (type_id == TypeID::ArrayTyID) {
        u64 array_elem_count;
        TypeForm array_elem_type;
    } else if (type_id == TypeID::FixedVectorTyID) {
        u64 fixed_vec_elem_count;
        TypeForm fixed_vec_elem_type;
    } else if (type_id == TypeID::ScalableVectorTyID) {
        TypeForm scalable_vec_elem_type;
    } else if (type_id == TypeID::TypedPointerTyID) {
        TypeForm pointer_elem_type;
    }
};

struct MasterHeader {
    u32 function_pointer;
    u32 function_length;
    TypeForm type;
};
// newest comment
MasterHeader headers[while($ < std::mem::size())] @ 0x0;