import struct
from enum import Enum

from parsing.bytetape import ByteTape


class EntryTypes(Enum):
    Inst = 0
    Const = 1
    Arg = 2

def parse_loopdb_symbounds(symbounds: ByteTape):
    symtable_entries = dict()
    while not symbounds.done():
        fun_ptr = symbounds.next_u32()
        fun_len = symbounds.next_u32()
        entry_count = symbounds.next_u64()
        if fun_ptr in symtable_entries:
            # duplicate entry
            raise "Duplicate entry!"
        symtable_entries[fun_ptr] = dict()
        symtable_entries[fun_ptr]["fun_length"] = fun_len
        symtable_entries[fun_ptr]["entries"] = []
        for j in range(entry_count):
            entry = dict()
            loop_id = symbounds.next_u64()
            str_len = symbounds.next_u64()
            format_string = symbounds.next_string(str_len).decode()
            dep_count = symbounds.next_u64()
            entry["loop_id"] = loop_id
            entry["format_string"] = format_string
            dependencies = []
            for k in range(dep_count):
                # parse a dependency
                dep_type = symbounds.next_u64()
                dep = dict()
                dep["type"] = EntryTypes(dep_type)
                if dep["type"] == EntryTypes.Arg:
                    dep["arg_no"] = symbounds.next_u64()
                elif dep["type"] == EntryTypes.Const:
                    constval_size = symbounds.next_u64()
                    dep["size"] = constval_size
                    if constval_size == 1:
                        dep["val"] = symbounds.next_u8()
                    elif constval_size == 2:
                        dep["val"] = symbounds.next_u16()
                    elif constval_size == 4:
                        dep["val"] = symbounds.next_u32()
                    elif constval_size == 8:
                        dep["val"] = symbounds.next_u64()
                    else:
                        dep["val"] = symbounds.next_bytes(constval_size)
                elif dep["type"] == EntryTypes.Inst:
                    dep["inst_tag_id"] = symbounds.next_u64()
                else:
                    raise "Invalid dependency type!"

                dependencies.append(dep)
            entry["deps"] = dependencies
            symtable_entries[fun_ptr]["entries"].append(entry)


    if not symbounds.exact_done():
        return None
    return symtable_entries
