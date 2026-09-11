import struct
from enum import Enum
from typing import List, Dict

from parsing.bytetape import ByteTape


class TypeID(Enum):
    HalfTyID = 0
    BFloatTyID = 1
    FloatTyID = 2
    DoubleTyID = 3
    X86_FP80TyID = 4
    FP128TyID = 5
    PPC_FP128TyID = 6
    VoidTyID = 7
    LabelTyID = 8
    MetadataTyID = 9
    X86_AMXTyID = 10
    TokenTyID = 11
    IntegerTyID = 12
    ByteTyID = 13
    FunctionTyID = 14
    PointerTyID = 15
    StructTyID = 16
    ArrayTyID = 17
    FixedVectorTyID = 18
    ScalableVectorTyID = 19
    TypedPointerTyID = 20
    TargetExtTyID = 21

def read_class(source: ByteTape) -> dict:
    type_id = TypeID(source.next_u64())
    res = dict()
    res["type"] = type_id
    if type_id == TypeID.IntegerTyID:
        res["int_bit_width"] = source.next_u64()

    elif type_id == TypeID.ByteTyID:
        res["byte_bit_width"] = source.next_u64()

    elif type_id == TypeID.FunctionTyID:
        is_var_arg = source.next_u64()

        if is_var_arg < 0 or is_var_arg > 1:
            raise struct.error()
        res["is_var_arg"] = is_var_arg == 1
        res["return_type"] = read_class(source)
        param_count = source.next_u64()
        res["param_count"] = param_count

        params = []
        for i in range(param_count):
            params.append(read_class(source))
        res["params"] = params
    elif type_id == TypeID.StructTyID:
        is_packed = source.next_u64()

        if is_packed < 0 or is_packed > 1:
            raise struct.error()
        res["packed"] = is_packed == 1
        is_opaque = source.next_u64()

        res["opaque"] = is_opaque == 1
        if is_opaque < 0 or is_opaque > 1:
            raise struct.error()
        if not is_opaque:
            entry_count = source.next_u64()

            res["entry_count"] = entry_count
            entries = []
            for i in range(entry_count):
                entries.append(read_class(source))
            res["entries"] = entries

    elif type_id == TypeID.ArrayTyID or type_id == TypeID.FixedVectorTyID:
        elem_count = source.next_u64()

        res["elem_count"] = elem_count
        res["elem_type"] = read_class(source)

    elif type_id == TypeID.ScalableVectorTyID:
        res["elem_type"] = read_class(source)
    elif type_id == TypeID.TypedPointerTyID:
        res["ptr_type"] = read_class(source)

    return res

def parse_functiondb(functiondb: ByteTape) -> Dict[int, dict] | None:
    try:
        entries = dict()
        while not functiondb.done():
            fp = functiondb.next_u32()
            flen = functiondb.next_u32()
            ftype = read_class(functiondb)
            entries[fp] = dict()
            entries[fp]["fun_length"] = flen
            entries[fp]["type"] = ftype

        if not functiondb.exact_done():
            return None
        return entries
    except struct.error:
        return None

