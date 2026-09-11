import unittest
import parsing.parsing



def gather(test: unittest.TestCase, name):
    symbounds, loopdb, functiondb, ivdb, sym_instr_db = parsing.parsing.get_and_parse(name)
    #test.assertIsNotNone(symbounds)
    test.assertIsNotNone(loopdb)
    test.assertIsNotNone(functiondb)
    test.assertIsNotNone(ivdb)
    test.assertIsNotNone(sym_instr_db)
    return parsing.parsing.validate(test, symbounds, loopdb, functiondb, ivdb, sym_instr_db)

class AscendingGeneric(unittest.TestCase):
    src = "ascending_generic.bpf.o"
    def test_something(self):
        print(gather(self, self.src))  # add assertion here
class DescendingGeneric(unittest.TestCase):
    src = "descending_generic.bpf.o"
    def test_something(self):
        print(gather(self, self.src))  # add assertion here
class EdgecaseDescendingMiss(unittest.TestCase):
    src = "edgecase_descending_miss.bpf.o"
    def test_something(self):
        print(gather(self, self.src))  # add assertion here
class PhiEnd(unittest.TestCase):
    src = "phi_end.bpf.o"
    def test_something(self):
        print(gather(self, self.src))  # add assertion here
class WrongWaySigned(unittest.TestCase):
    src = "wrongway_signed.bpf.o"
    def test_something(self):
        print(gather(self, self.src))  # add assertion here
class WrongWayUnsigned(unittest.TestCase):
    src = "wrongway_unsigned.bpf.o"
    def test_something(self):
        print(gather(self, self.src))  # add assertion here
class AscendingStride(unittest.TestCase):
    src = "ascending_stride.bpf.o"
    def test_something(self):
        print(gather(self, self.src))  # add assertion here
class EdgecaseAscendingMiss(unittest.TestCase):
    src = "edgecase_ascending_miss.bpf.o"
    def test_something(self):
        print(gather(self, self.src))  # add assertion here
class EdgecaseUnsigned(unittest.TestCase):
    src = "edgecase_unsigned.bpf.o"
    def test_something(self):
        print(gather(self, self.src))  # add assertion here
class SignedUnsigned(unittest.TestCase):
    src = "signed_unsigned.bpf.o"
    def test_something(self):
        print(gather(self, self.src))  # add assertion here


if __name__ == '__main__':
    unittest.main()
