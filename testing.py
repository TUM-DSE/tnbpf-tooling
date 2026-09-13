import unittest
from typing import Dict

import parsing.parsing

def pretty_format(d, depth=0, startindent=True):
    if isinstance(d, dict):
        s = (" " * depth if startindent else "") + "{\n"
        for key, value in d.items():
            s += (" " * (depth+1)) + str(key) + ": " + pretty_format(value, depth+1 , False) + ",\n"
        s += " " * depth + "}"
        return s
    elif isinstance(d, list):
        s = (" " * depth if startindent else "") + "[" + ("\n" if len(d) > 0 else "")
        for value in d:
            s += (" " * (depth+1)) + pretty_format(value, depth+1 , False) + ",\n"
        s += (" " * depth if len(d) > 0 else "") + "]"
        return s
    else:
        return (" " * depth if startindent else "") + str(d)

def pretty_print(p):
    print(pretty_format(p))

def pretty_print_sizes(d: Dict[str, int]):
    program_size = float(d["program_size"])
    total_size = d["total_size"]
    print("Section\t\t\t\t\t\t\t\tSize in bytes\t\tSize wrt. code segment\t\tPercent of binary")
    metadata_footprint = 0
    for name, size in d.items():
        if name == "total_size":
            continue
        if name.startswith("pcsection"):
            metadata_footprint += size
        print(f"{name:<32}\t{size}\t\t\t\t\t{((size * 100.0) / program_size):.2f}%\t\t\t\t\t\t{((size * 100.0) / total_size):.2f}%")
    print(f"{"Total Metadata Footprint":<32}\t{metadata_footprint}\t\t\t\t\t{((metadata_footprint * 100.0) / program_size):.2f}%\t\t\t\t\t\t{((metadata_footprint * 100.0) / total_size):.2f}%")
def gather(test: unittest.TestCase, name):
    symbounds, loopdb, functiondb, ivdb, sym_instr_db, sizes = parsing.parsing.get_and_parse(name)
    #test.assertIsNotNone(symbounds)
    test.assertIsNotNone(loopdb)
    test.assertIsNotNone(functiondb)
    #test.assertIsNotNone(ivdb)
    test.assertIsNotNone(sym_instr_db)
    pretty_print_sizes(sizes)
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


if __name__ == '__main__':
    unittest.main()
