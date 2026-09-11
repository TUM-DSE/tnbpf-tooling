import struct
from enum import Enum
from typing import Dict

from parsing.bytetape import ByteTape


class BPFRegister(Enum):
    NoRegister=0
    R0 = 1
    R1 = 2
    R2 = 3
    R3 = 4
    R4 = 5
    R5 = 6
    R6 = 7
    R7 = 8
    R8 = 9
    R9 = 10
    R10 = 11
    R11 = 12
    W0 = 13
    W1 = 14
    W2 = 15
    W3 = 16
    W4 = 17
    W5 = 18
    W6 = 19
    W7 = 20
    W8 = 21
    W9 = 22
    W10 = 23
    W11 = 24

def parse_iv_db(ivdb: ByteTape) -> Dict[int, dict] | None:
    try:
        ivdb_entries = dict()
        while not ivdb.done():
            fun_ptr = ivdb.next_u32()
            fun_len = ivdb.next_u32()
            entry_count = ivdb.next_u64()
            if fun_ptr in ivdb_entries:
                # duplicate entry
                return None
            ivdb_entries[fun_ptr] = dict()
            ivdb_entries[fun_ptr]["fun_length"] = fun_len
            ivdb_entries[fun_ptr]["entries"] = []
            for j in range(entry_count):
                loop_id = ivdb.next_u64()
                iv_register = BPFRegister(ivdb.next_u32())
                ivdb_entries[fun_ptr]["entries"].append({"loop_id": loop_id, "register": iv_register})
        if not ivdb.exact_done():
            return None
        return ivdb_entries
    except struct.error:
        return None
