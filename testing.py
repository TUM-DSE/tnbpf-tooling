import unittest
from typing import Dict

import extraction
import parsing.parsing
from printing import humanbytes, pretty_print
csv_data = ["tname,msize,csize,pbin\n"]

def pretty_print_sizes(test:unittest.TestCase, d: Dict[str, int]):
    program_size = float(d["program_size"])
    total_size = d["total_size"]
    print(f"Total binary size: {humanbytes(total_size)}")
    print(f"Program text section size: {humanbytes(program_size)} ({((program_size * 100.0) / total_size):.2f}% of binary)")
    print("Section\t\t\t\t\t\t\t\tSize in bytes\t\tSize wrt. code segment\t\tPercent of binary")
    metadata_footprint = 0
    for name, size in d.items():
        if not name.startswith("pcsection"):
            continue
        metadata_footprint += size
        print(f"{name:<32}\t{humanbytes(size)}\t\t\t\t{((size * 100.0) / program_size):.2f}%\t\t\t\t\t\t{((size * 100.0) / total_size):.2f}%")

    csv_data.append(f"{test.__class__.__name__},{humanbytes(metadata_footprint)},{((metadata_footprint * 100.0) / program_size):.2f},{((metadata_footprint * 100.0) / total_size):.2f}\n")
    print(f"{"Total Metadata Footprint":<32}\t{humanbytes(metadata_footprint)}\t\t\t\t{((metadata_footprint * 100.0) / program_size):.2f}%\t\t\t\t\t\t{((metadata_footprint * 100.0) / total_size):.2f}%")
def gather(test: unittest.TestCase, name):
    symbounds, loopdb, functiondb, ivdb, sym_instr_db, sizes = parsing.parsing.get_and_parse(name)
    #test.assertIsNotNone(symbounds)
    test.assertIsNotNone(loopdb)
    test.assertIsNotNone(functiondb)
    #test.assertIsNotNone(ivdb)
    test.assertIsNotNone(sym_instr_db)
    pretty_print_sizes(test, sizes)
    return parsing.parsing.validate(test, symbounds, loopdb, functiondb, ivdb, sym_instr_db)



class AscendingGeneric(unittest.TestCase):
    src = "ascending_generic.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here
class DescendingGeneric(unittest.TestCase):
    src = "descending_generic.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here
class EdgecaseDescendingMiss(unittest.TestCase):
    src = "edgecase_descending_miss.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here
class PhiEnd(unittest.TestCase):
    src = "phi_end.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here
class WrongWaySigned(unittest.TestCase):
    src = "wrongway_signed.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here
class WrongWayUnsigned(unittest.TestCase):
    src = "wrongway_unsigned.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here
class AscendingStride(unittest.TestCase):
    src = "ascending_stride.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here
class EdgecaseAscendingMiss(unittest.TestCase):
    src = "edgecase_ascending_miss.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here
class EdgecaseUnsigned(unittest.TestCase):
    src = "edgecase_unsigned.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here
class SignedUnsigned(unittest.TestCase):
    src = "signed_unsigned.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here
class PointerLoop(unittest.TestCase):
    src = "pointerloop.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here
class VariableStride(unittest.TestCase):
    src = "variable_stride.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here

class NestedRegular(unittest.TestCase):
    src = "nested_regular.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here

class NestedInterdependent(unittest.TestCase):
    src = "nested_interdep.bpf.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        pretty_print(gather(self, self.src))  # add assertion here


class MultiModuleTest(unittest.TestCase):
    src = "tetragon/bpf/objs/bpf_multi_kprobe_v511.o"
    def test_something(self):
        print("[" + self.__class__.__name__ + "]")
        multi = extraction.fetch_pcsections_multimodule(self.src)
        # somehow duplicated entries
        #parsing.parsing.parse_multi(multi, self)

# We name it like this to ensure unittest runs it last
class ZZZEmitToCSV(unittest.TestCase):
    def test_emit(self):
        print("[" + self.__class__.__name__ + "]")
        with open("results.csv", "w") as f:
            f.writelines(csv_data)

if __name__ == '__main__':
    unittest.main()
