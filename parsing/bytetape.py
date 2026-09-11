import struct


class ByteTape:
    def __init__(self, source):
        self._src = source
        self._idx = 0

    def next_u1(self):
        res = struct.unpack_from("=?", self._src, self._idx)[0]
        self._idx += 1
        return res

    def next_u8(self):
        res = struct.unpack_from("=B", self._src, self._idx)[0]
        self._idx += 1
        return res

    def next_u16(self):
        res = struct.unpack_from("=H", self._src, self._idx)[0]
        self._idx += 2
        return res

    def next_u32(self):
        res = struct.unpack_from("=I", self._src, self._idx)[0]
        self._idx += 4
        return res

    def next_u64(self):
        res = struct.unpack_from("=Q", self._src, self._idx)[0]
        self._idx += 8
        return res

    def next_string(self, size: int) -> bytes:
        res = struct.unpack_from("=" + str(size) + "s", self._src, self._idx)[0]
        self._idx += size
        return res

    def next_bytes(self, size: int):
        res = struct.unpack_from("=" + str(size) + "b", self._src, self._idx)[0]
        self._idx += size
        return res

    def done(self):
        return self._idx >= len(self._src)

    def exact_done(self):
        return self._idx == len(self._src)