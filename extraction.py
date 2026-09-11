import os
from typing import Dict

import credentials
import subprocess

def fetch_pcsections(file_name: str) -> Dict[str, bytes]:
    # copy over the binary
    os.system("rm -rf bin")
    os.system("mkdir bin")
    os.system("mkdir bin/sections")

    os.system("scp " + credentials.gitrepo + file_name + " bin/object.o")
    output = subprocess.check_output(["objdump", "-h", "bin/object.o"])
    decoded = [x.split()[1:] for x in output.decode().splitlines()[5:]][0::2]
    # TODO: this requires the file to have .bpf.c in its name!
    bpf_entries = list(filter(lambda x: ".bpf.c" in x[0], decoded))
    if len(bpf_entries) == 0:
        print("No sections found!")
        return

    module_name_extract = bpf_entries[0][0]
    idx = module_name_extract.find(".bpf.c")
    idx += len(".bpf.c")
    module_name = module_name_extract[:idx]
    for i in range(len(bpf_entries)):
        if not bpf_entries[i][0].startswith(module_name):
            print(f"Bad section name: {bpf_entries[i][0]}, expected module name {module_name}")
            return
        bpf_entries[i][0] = "pcsection" + bpf_entries[i][0][len(module_name):]

    print(bpf_entries)
    sections = dict()
    with open("bin/object.o", "rb") as f:
        rawdata = f.read()
    for entry in bpf_entries:
        name, size, _, _, file_off, _ = tuple(entry)

        size = int(size, 16)
        file_off = int(file_off, 16)
        print(name, size, file_off)
        sections[name] = rawdata[file_off:file_off+size]

    print(sections)
    return sections