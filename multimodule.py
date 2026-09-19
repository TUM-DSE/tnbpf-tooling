class MultiModuleFile:
    def __init__(self, raw_data: bytes, objdump_output: str):
        decoded = [x.split()[1:] for x in objdump_output.splitlines()[5:]][0::2]
        properties = ["CODE" in x.split()[1:] for x in objdump_output.splitlines()[5:]][1::2]
        text_size = 0
        for i in range(len(decoded)):
            if properties[i]:
                text_size += int(decoded[i][1], 16)

        self.text_size = text_size
        self.total_size = len(raw_data)

        self.modules = dict()
        self.metadata_sizes = 0

        for entry in filter(lambda x: ".c" in x[0] and ".rel" not in x[0], decoded):
            module_name_extract = entry[0]
            idx = module_name_extract.find(".c")
            idx += len(".c")
            module_name = module_name_extract[:idx]
            section_name = "pcsection" + module_name_extract[idx:]

            if module_name not in self.modules.keys():
                self.modules[module_name] = dict()

            _, size, _, _, file_off, _ = tuple(entry)
            size = int(size, 16)
            file_off = int(file_off, 16)

            self.metadata_sizes += size

            self.modules[module_name][section_name] = raw_data[file_off:file_off + size]

