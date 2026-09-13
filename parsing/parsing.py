import re
import unittest
from typing import Dict, List

from extraction import fetch_pcsections
from parsing.functiondb import parse_functiondb
from parsing.ivdb import parse_iv_db
from parsing.loopdb_class import parse_loopdb_class
from parsing.bytetape import ByteTape
from parsing.symbounds import parse_loopdb_symbounds
from parsing.sym_instr_db import parse_sym_instr_db

percent_integer = re.compile("%[0-9]+")
percent_iv = re.compile("%iv")

def validate(test: unittest.TestCase, symbounds: Dict[int, dict], loopdb: Dict[int, dict], functiondb: Dict[int, dict], ivdb: Dict[int, dict], sym_instr_db: List[int]):
    # Validations to do:
    # - loopdb_class
    # - symbounds
    functions = dict()
    instr_not_found = set()
    for i in range(len(sym_instr_db)):
        if sym_instr_db[i] is not None:
            instr_not_found.add(i)

    for func_ptr, entry in loopdb.items():
        test.assertNotIn(func_ptr, functions)
        functions[func_ptr] = dict()
        functions[func_ptr]["fun_length"] = entry["fun_length"]
        instrs = set()
        for i in range(len(sym_instr_db)):
            if sym_instr_db[i] is not None:
                if func_ptr <= sym_instr_db[i] < (func_ptr + functions[func_ptr]["fun_length"]):
                    instrs.add(i)
                    instr_not_found.remove(i)
        functions[func_ptr]["instrs"] = instrs
        # cross-validate function references
        test.assertIn(func_ptr, functiondb)
        test.assertEqual(functions[func_ptr]["fun_length"], functiondb[func_ptr]["fun_length"])
        functions[func_ptr]["type"] = functiondb[func_ptr]["type"]

        expected_measures_loop_ids = set()
        functions[func_ptr]["loops"] = dict()
        loopids_valid = set()

        for loop_entry in entry["entries"]:
            # No guarantee these actually make it into the binary
            # Especially not the compare ID one
            if "branch_id" in loop_entry:
                test.assertIn(loop_entry["branch_id"], instrs)

            if "compare_id" in loop_entry:
                #test.assertIn(loop_entry["compare_id"], instrs)
                pass

            test.assertNotIn(loop_entry["loop_id"], loopids_valid)
            loopids_valid.add(loop_entry["loop_id"])

            for latch in loop_entry["latches"]:
                test.assertIn(latch, instrs)

            if loop_entry["has_measure"]:
                expected_measures_loop_ids.add(loop_entry["loop_id"])

            res = dict()

            for property in ["ascending", "terminates", "const_max_exit_count", "exact_exit_count", "start", "finish", "stride"]:
                if property in loop_entry:
                    res[property] = loop_entry[property]
            res["comp_type"] = loop_entry["comp_type"]

            functions[func_ptr]["loops"][loop_entry["loop_id"]] = res

        if len(expected_measures_loop_ids) == 0:
            if symbounds is not None:
                test.assertNotIn(func_ptr, symbounds)
        else:
            test.assertIsNotNone(symbounds)
            test.assertIn(func_ptr, symbounds)
            test.assertEqual(symbounds[func_ptr]["fun_length"], functions[func_ptr]["fun_length"])
            encountered_measures_loop_ids = set()

            for symbound_entry in symbounds[func_ptr]["entries"]:
                test.assertIn(symbound_entry["loop_id"], loopids_valid)
                test.assertNotIn(symbound_entry["loop_id"], encountered_measures_loop_ids)
                encountered_measures_loop_ids.add(symbound_entry["loop_id"])

                # Full format string testing requires an entire AST Parser, instead we just test if all our references are here
                # Parse via regex and call it a day
                format_str = symbound_entry["format_string"][:]
                dep_count = len(symbound_entry["deps"])
                for match in percent_integer.findall(format_str):
                    num = int(match[1:])
                    test.assertGreaterEqual(num, 0)
                    test.assertLess(num, dep_count)

                # Don't replace with empty string, otherwise "%%iv5" -> "%5" -> "" succeeds this check
                format_str = re.sub(percent_iv, "R", format_str)
                format_str = re.sub(percent_integer, "R", format_str)
                test.assertNotIn('%', format_str)

                functions[func_ptr]["loops"][symbound_entry["loop_id"]]["format_string"] = symbound_entry["format_string"][:]
                functions[func_ptr]["loops"][symbound_entry["loop_id"]]["format_deps"] = symbound_entry["deps"]

            test.assertSetEqual(expected_measures_loop_ids, encountered_measures_loop_ids)

        loopids_ivdb = set()
        if ivdb is not None and func_ptr in ivdb:
            test.assertEqual(functions[func_ptr]["fun_length"], ivdb[func_ptr]["fun_length"])
            for iv_entry in ivdb[func_ptr]["entries"]:
                test.assertIn(iv_entry["loop_id"], loopids_valid)
                test.assertNotIn(iv_entry["loop_id"], loopids_ivdb)
                loopids_ivdb.add(iv_entry["loop_id"])
                functions[func_ptr]["loops"][iv_entry["loop_id"]]["iv_register"] = iv_entry["register"]

    test.assertSetEqual(instr_not_found, set())
    return functions


def parse_pcsections(pcsections: Dict[str, bytes]):
    symbounds_raw = pcsections["pcsection_loopdb_symbounds"] if "pcsection_loopdb_symbounds" in pcsections else None
    loopdb_raw = pcsections["pcsection_loopdb_class"]
    functiondb_raw = pcsections["pcsection_functiondb"]
    ivdb_raw = pcsections["pcsection_iv_db"] if "pcsection_iv_db" in pcsections else None
    sym_instr_db_raw = pcsections["pcsection_sym_instr_db"]

    symbounds = parse_loopdb_symbounds(ByteTape(symbounds_raw)) if symbounds_raw else None
    loopdb = parse_loopdb_class(ByteTape(loopdb_raw)) if loopdb_raw else None
    functiondb = parse_functiondb(ByteTape(functiondb_raw)) if functiondb_raw else None
    ivdb = parse_iv_db(ByteTape(ivdb_raw)) if ivdb_raw else None
    sym_instr_db = parse_sym_instr_db(ByteTape(sym_instr_db_raw)) if sym_instr_db_raw else None

    # Our primary entry point is the loopdb classifier:
    return symbounds, loopdb, functiondb, ivdb, sym_instr_db, pcsections["metadata_sizes"]

def get_and_parse(remote_name: str):
    return parse_pcsections(fetch_pcsections(remote_name))