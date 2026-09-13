import extraction
bin_name = "hello.bpf.o"
def main():
    # copy over the binary

    for name, data in extraction.fetch_pcsections(bin_name).items():
        if not isinstance(data, bytes):
            continue
        print(name, len(data))
        with open("bin/sections/" + name + ".bin", "wb") as f:
            f.write(data)

if __name__ == "__main__":
    main()