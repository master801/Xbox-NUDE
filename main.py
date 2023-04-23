#!/usr/bin/env python3
# Created by Master on 4/22/2023 at 6:00 PM CDT

import argparse
import io
import os
import glob
import json
import struct

import nude_tfs


def create_tfs(tfs_files: list[str], tfs_metadata_files: list[str], name: str, output_directory: str):
    io_tfs: io.BytesIO = io.BytesIO()

    # magic / header section
    io_tfs.write(b'tnFS')  # 4
    io_tfs.write(struct.pack('<I', len(tfs_files)))  # divide by 2 since we expect metadata json files
    io_tfs.write(struct.pack('<I', 0x10))  # header offset - don't know why this is here tbh
    io_tfs.write(struct.pack('>I', 0xDEADBEEF))  # tfs entries section size - dummy packing

    # header section
    io_tfs.write((b'\x00' * 32) * len(tfs_files))  # pack dummy data as header

    # write names section and pad
    for i in range(len(tfs_files)):
        tfs_file = tfs_files[i]
        tfs_metadata_file = tfs_metadata_files[i]

        discard: int = io_tfs.tell()
        io_tfs.seek(0x10 + (i * 0x20) + 0x0C)  # name_offset
        io_tfs.write(struct.pack('<I', discard - 0x10))
        io_tfs.seek(discard)  # seek to original pos
        del discard

        discard: int = io_tfs.tell()
        with open(tfs_metadata_file, mode='rt+', encoding='utf-8') as io_tfs_metadata:
            tfs_metadata: dict = json.loads(io_tfs_metadata.read())
            pass
        io_tfs.seek(0x10 + (i * 0x20) + 0x10)  # idk_1
        io_tfs.write(struct.pack('<I', tfs_metadata['idk_1']))
        io_tfs.seek(0x10 + (i * 0x20) + 0x14)  # idk_2
        io_tfs.write(struct.pack('<I', tfs_metadata['idk_2']))
        io_tfs.seek(0x10 + (i * 0x20) + 0x18)  # idk_3
        io_tfs.write(struct.pack('<I', tfs_metadata['idk_3']))
        io_tfs.seek(0x10 + (i * 0x20) + 0x1C)  # idk_4
        io_tfs.write(struct.pack('<I', tfs_metadata['idk_4']))
        io_tfs.seek(discard)  # seek to original pos
        del tfs_metadata
        del discard

        io_tfs.write(tfs_file[tfs_file.rindex(os.path.sep) + 1:].encode(encoding='ascii'))
        io_tfs.write(b'\x00')
        continue
    del tfs_file
    del tfs_metadata_file

    discard: int = io_tfs.tell()
    io_tfs.seek(0x0C)
    io_tfs.write(struct.pack('<I', discard - 0x10))  # tfs_entry_size
    io_tfs.seek(discard)
    del discard

    while io_tfs.tell() % 2048 != 0:
        io_tfs.write(b'\x00')
        continue

    for i in range(len(tfs_files)):
        tfs_file = tfs_files[i]

        discard: int = io_tfs.tell()
        io_tfs.seek(0x10 + (i * 0x20) + 0x00)  # offset
        io_tfs.write(struct.pack('<I', discard))
        io_tfs.seek(discard)  # seek to original pos
        del discard

        with open(tfs_file, mode='rb+') as io_tfs_entry:
            data_tfs_entry = io_tfs_entry.read()
            io_tfs.write(data_tfs_entry)
            pass

        discard: int = io_tfs.tell()
        io_tfs.seek(0x10 + (i * 0x20) + 0x04)  # size
        io_tfs.write(struct.pack('<I', len(data_tfs_entry)))
        io_tfs.seek(0x10 + (i * 0x20) + 0x08)  # size_2
        io_tfs.write(struct.pack('<I', len(data_tfs_entry)))
        io_tfs.seek(discard)  # seek to original pos
        del discard

        while io_tfs.tell() % 2048 != 0:  # pad
            io_tfs.write(b'\x00')
            continue
        continue
    del tfs_file

    out_fp = output_directory
    if os.path.exists(out_fp):
        out_mode = 'w+'
        pass
    else:
        out_mode = 'x'
        pass

    if not output_directory.endswith('.tfs'):
        out_fp = os.path.join(out_fp, name)
        pass

    with open(out_fp, mode=f'{out_mode}b') as io_write_tfs:
        io_tfs.seek(0, io.SEEK_SET)
        io_write_tfs.write(io_tfs.read())
        pass
    return


def create(_input: str, output_dir: str):
    tfs_files: list[str] = []
    tfs_metadata_files: list[str] = []
    for i in os.scandir(_input):
        if i.is_file():
            if i.name.endswith('.json'):
                tfs_metadata_files.append(i.path)
                pass
            else:
                tfs_files.append(i.path)
                pass
            pass
        elif i.is_dir():
            create(i.path, output_dir)
            pass
        continue
    del i

    if len(tfs_files) != len(tfs_metadata_files):
        print('Not equal!')
        return

    if len(tfs_files) < 1:
        print(f'No tfs files in directory \"{_input}\"!')
        return

    if os.path.sep in _input:
        name = _input[_input.rindex(os.path.sep)+1:]
        pass
    else:
        name = 'BAD_NAME'
        print('A fatal error has occurred!')
        pass

    print(f'Found {len(tfs_files)} tfs entries')
    print(f'Creating \"{name}.tfs\"...')
    create_tfs(tfs_files, tfs_metadata_files, f'{name}.tfs', output_dir)
    print(f'Created tfs file \"{os.path.join(output_dir, name)}.tfs\"!\n')
    return


def extract_tfs(root_dir: str, path_tfs: str, output_dir: str):
    path: str = f'{root_dir}{os.path.sep}{path_tfs}'
    folder: str = path
    if os.path.sep in folder:
        folder = folder[folder.rindex(os.path.sep)+1:]
        pass
    if folder.endswith('.tfs'):
        folder = folder[0:folder.index('.tfs')]
        pass
    folder = os.path.join(output_dir, folder)
    if not os.path.isdir(folder):
        os.makedirs(folder)
        pass
    with open(path, mode='rb+') as io_tfs:
        tfs: nude_tfs.NudeTfs = nude_tfs.NudeTfs.from_io(io_tfs)

        print(f'Found {tfs.tfs_entry_size} entries to extract!')

        for tfs_entry in tfs.tfs_entries:
            io_tfs.seek(tfs_entry.name_offset + 0x10, io.SEEK_SET)
            buffer: bytearray = bytearray()
            buffer_byte = io_tfs.read(1)
            while buffer_byte != b'\x00':
                buffer += buffer_byte
                buffer_byte = io_tfs.read(1)
                continue
            tfs_name: str = buffer.decode('ascii')  # Japanese game - but uses ascii for file names...

            tfs_fp: str = os.path.join(folder, tfs_name)
            if os.path.isfile(tfs_fp):
                tfs_entry_mode = 'w+'
                pass
            else:
                tfs_entry_mode = 'x'
                pass

            with open(tfs_fp, mode=f'{tfs_entry_mode}b') as io_tfs_entry:
                io_tfs.seek(tfs_entry.offset, io.SEEK_SET)
                bytes_tfs_entry: bytes = io_tfs.read(tfs_entry.size)
                io_tfs_entry.write(bytes_tfs_entry)
                pass
            print(f'Extracted tfs entry \"{tfs_name}\" to file \"{tfs_fp}\"!')

            tfs_metadata_fp: str = f'{tfs_fp}.json'
            if os.path.isfile(tfs_metadata_fp):
                tfs_metadata_mode = 'w+'
                pass
            else:
                tfs_metadata_mode = 'x'
                pass
            with open(tfs_metadata_fp, mode=f'{tfs_metadata_mode}t', encoding='utf-8') as io_tfs_metadata:
                tfs_metadata: str = json.dumps(
                    {
                        'idk_1': tfs_entry.idk_1,
                        'idk_2': tfs_entry.idk_2,
                        'idk_3': tfs_entry.idk_3,
                        'idk_4': tfs_entry.idk_4
                    }
                )
                io_tfs_metadata.write(tfs_metadata)
                pass
            continue
        pass
    return


def extract(_input: str, output_dir: str):
    if os.path.isfile(_input):
        extract_tfs('.', _input, output_dir)
        pass
    elif os.path.isdir(_input):
        for i in glob.glob('*.tfs', root_dir=_input, recursive=False):
            print(f'Extracting tfs file \"{i}\"...')
            extract_tfs(_input, i, output_dir)
            print('Done extracting!\n')
            continue
        pass
    return


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--extract', action='store_true')
    argparser.add_argument('--create', action='store_true')
    argparser.add_argument('--input', required=True)
    argparser.add_argument('--output', required=True)
    args = argparser.parse_args()

    if args.extract and args.create:
        print('Cannot extract and create at the same time!\nPlease specify only one option.')
        return
    elif not args.extract and not args.create:
        print('No option specified!')
        return

    if args.extract:
        if not os.path.exists(args.input):
            print(f'Path \"{args.input}\" does not exist!\nCannot extract TFS file!')
            return
        extract(args.input, args.output)
        pass
    elif args.create:
        if not os.path.exists(args.input):
            print(f'Path \"{args.input}\" does not exist!\nCannot create TFS file!')
            return
        create(args.input, args.output)
        pass
    else:
        print('No option selected!')
        pass

    return


if __name__ == '__main__':
    main()
    pass
