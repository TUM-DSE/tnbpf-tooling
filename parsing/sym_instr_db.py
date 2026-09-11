import struct
from typing import List

from parsing.bytetape import ByteTape


def parse_sym_instr_db(instrdb: ByteTape) -> List[int] | None:
    try:
        instructions = []

        while not instrdb.done():
            instr_pointer = instrdb.next_u32()
            tag_id = instrdb.next_u64()
            if len(instructions) < tag_id + 1:
                instructions += [None] * (tag_id + 1 - len(instructions))
            elif instructions[tag_id] is not None:
                return None
            instructions[tag_id] = instr_pointer

        if not instrdb.exact_done():
            return None
        return instructions
    except struct.error:
        return None