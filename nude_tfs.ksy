meta:
  id: nude_tfs
  file-extension: nude_tfs
  endian: le
seq:
  - id: magic
    contents: [ 0x74, 0x6E, 0x46, 0x53 ]  # tnFS
    size: 4
  - id: entries_size
    type: u4le
  - id: header_offset
    type: u4le
  - id: tfs_entry_size
    type: u4le
  - id: tfs_entries
    type: tfs_entry
    repeat: expr
    repeat-expr: entries_size
types:
  tfs_entry:
    seq:
      - id: offset
        type: u4le
      - id: size
        type: u4le
      - id: size_2  # Not sure
        type: u4le
      - id: name_offset  # after header (+0x10)
        type: u4le
      - id: idk_1
        type: u4le
      - id: idk_2
        type: u4le
      - id: idk_3
        type: u4le
      - id: idk_4
        type: u4le