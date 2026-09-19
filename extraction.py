import os
from typing import Dict

import credentials
import subprocess
from multimodule import MultiModuleFile

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
    text_size_entry = list(filter(lambda x: x[0] == "tracepoint/syscalls/sys_enter_execve", decoded))[0]
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

    sections = dict()
    sizes = dict()
    totalsize = 0
    with open("bin/object.o", "rb") as f:
        rawdata = f.read()
        totalsize = len(rawdata)
    for entry in bpf_entries:
        name, size, _, _, file_off, _ = tuple(entry)

        size = int(size, 16)
        file_off = int(file_off, 16)
        sections[name] = rawdata[file_off:file_off+size]
        sizes[name] = size

    _, bin_size, _, _, _, _ = text_size_entry
    sizes["program_size"] = int(bin_size, 16)
    sizes["total_size"] = totalsize
    sections["metadata_sizes"] = sizes
    return sections

def fetch_pcsections_multimodule(file_name: str) -> MultiModuleFile:
    # copy over the binary
    os.system("rm -rf bin")
    os.system("mkdir bin")
    os.system("mkdir bin/sections")

    os.system("scp " + credentials.gitrepo + file_name + " bin/object.o")
    output = subprocess.check_output(["objdump", "-h", "bin/object.o"]).decode()


    with open("bin/object.o", "rb") as f:
        rawdata = f.read()

    return MultiModuleFile(rawdata, output)