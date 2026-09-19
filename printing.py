# https://stackoverflow.com/a/31631711 , accessed on 13.09.2026
def humanbytes(B):
    """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776

    if B < KB:
        return '{0} B'.format(B)
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    else:
        return '{0:.2f} TB'.format(B / TB)



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