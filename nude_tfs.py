# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class NudeTfs(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(4)
        if not self.magic == b"\x74\x6E\x46\x53":
            raise kaitaistruct.ValidationNotEqualError(b"\x74\x6E\x46\x53", self.magic, self._io, u"/seq/0")
        self.entries_size = self._io.read_u4le()
        self.header_offset = self._io.read_u4le()
        self.tfs_entry_size = self._io.read_u4le()
        self.tfs_entries = []
        for i in range(self.entries_size):
            self.tfs_entries.append(NudeTfs.TfsEntry(self._io, self, self._root))


    class TfsEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u4le()
            self.size = self._io.read_u4le()
            self.size_2 = self._io.read_u4le()
            self.name_offset = self._io.read_u4le()
            self.idk_1 = self._io.read_u4le()
            self.idk_2 = self._io.read_u4le()
            self.idk_3 = self._io.read_u4le()
            self.idk_4 = self._io.read_u4le()



