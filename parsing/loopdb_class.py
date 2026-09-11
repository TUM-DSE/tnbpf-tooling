import struct
from enum import Enum

from parsing.bytetape import ByteTape


class ComparisonType(Enum):
    FALSE = 0
    GT = 1
    EQ = 2
    GEQ = 3
    LT = 4
    NEQ = 5
    LEQ = 6
    TRUE = 7
    C_UNK = 8

def parse_loopdb_class(loopdb: ByteTape):
    try:
        loopdb_entries = dict()
        while not loopdb.done():
            fun_ptr = loopdb.next_u32()
            fun_len = loopdb.next_u32()
            entry_count = loopdb.next_u64()
            if fun_ptr in loopdb_entries:
                # duplicate entry
                return None
            loopdb_entries[fun_ptr] = dict()
            loopdb_entries[fun_ptr]["fun_length"] = fun_len
            loopdb_entries[fun_ptr]["entries"] = []
            for j in range(entry_count):
                entry = dict()
                loop_id = loopdb.next_u64()
                start= loopdb.next_u64()
                finish= loopdb.next_u64()
                stride= loopdb.next_u64()
                exact_exit_count= loopdb.next_u64()
                const_max_exit_count= loopdb.next_u64()
                branch_id= loopdb.next_u64()
                compare_id= loopdb.next_u64()
                comp_type = loopdb.next_u16()
                isAscending = loopdb.next_u1()
                loopTerminates = loopdb.next_u1()
                hasIsAscending = loopdb.next_u1()
                hasStart = loopdb.next_u1()
                hasFinish = loopdb.next_u1()
                hasStride = loopdb.next_u1()
                hasLoopTerminates = loopdb.next_u1()
                hasExactExitCount = loopdb.next_u1()
                hasConstMaxExitCount = loopdb.next_u1()
                hasTranslationTableMeasure = loopdb.next_u1()
                hasBranchID = loopdb.next_u1()
                hasCompareID = loopdb.next_u1()
                latchCount = loopdb.next_u64()

                if hasIsAscending:
                    entry["ascending"] = isAscending
                if hasLoopTerminates:
                    entry["terminates"] = loopTerminates
                if hasBranchID:
                    entry["branch_id"] = branch_id
                if hasCompareID:
                    entry["compare_id"] = compare_id
                if hasConstMaxExitCount:
                    entry["const_max_exit_count"] = const_max_exit_count
                if hasExactExitCount:
                    entry["exact_exit_count"] = exact_exit_count
                if hasStart:
                    entry["start"] = start
                if hasFinish:
                    entry["finish"] = finish
                if hasStride:
                    entry["stride"] = stride
                entry["has_measure"] = hasTranslationTableMeasure
                entry["loop_id"] = loop_id
                if comp_type < 0 or comp_type > ComparisonType.C_UNK.value:
                    return None
                entry["comp_type"] = comp_type

                latches = []
                for k in range(latchCount):
                    latch = loopdb.next_u64()
                    latches.append(latch)

                entry["latches"] = latches

                loopdb_entries[fun_ptr]["entries"].append(entry)
        if not loopdb.exact_done():
            return None
        return loopdb_entries
    except struct.error:
        return None
