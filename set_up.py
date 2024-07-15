#!/usr/bin/env python3
# Created by Master on 7/14/2024

import os
import glob
import subprocess
import shutil
import pathlib

STAGES = [
    'EXTRACT',
    'PATCH',
    'BUILD'
]

FN_XBE = 'default.xbe'
FN_XBE_BK = 'default.xbe.bk'

DN_RESOURCES = 'Resources'

DIR_GAME = f'..{os.path.sep}GAME'
DIR_GAME_RESOURCES = os.path.join(DIR_GAME, DN_RESOURCES)
FILE_GAME_XBE = os.path.join(DIR_GAME, FN_XBE)

DIR_XBE = 'XBE'
FILE_XBE_XBE = os.path.join(DIR_XBE, FN_XBE)

DIR_ORIGINAL = 'ORIGINAL'
DIR_ORIGINAL_TFS = os.path.join(DIR_ORIGINAL, 'TFS')

DIR_EXTRACTED = 'EXTRACTED'
DIR_EXTRACTED_TFS = os.path.join(DIR_EXTRACTED, 'TFS')

DIR_WORKING = 'WORKING'
DIR_WORKING_TFS = os.path.join(DIR_WORKING, 'TFS')

DIR_MODIFIED = 'MODIFIED'
DIR_MODIFIED_RESOURCES = os.path.join(DIR_MODIFIED, DN_RESOURCES)
FILE_MODIFIED_XBE = os.path.join(DIR_MODIFIED, FN_XBE)


def build(exe_tfs: pathlib.Path):
    print('Building...\n')

    if not os.path.exists(DIR_MODIFIED):
        os.makedirs(DIR_MODIFIED)
        pass
    if not os.path.exists(DIR_MODIFIED_RESOURCES):
        os.makedirs(DIR_MODIFIED_RESOURCES)
        pass

    print(f'Copying \"{FN_XBE}\"...')
    if os.path.exists(FILE_XBE_XBE):
        shutil.copyfile(
            FILE_XBE_XBE,
            FILE_MODIFIED_XBE,
            follow_symlinks=False
        )
        pass
    else:
        if os.path.exists(FILE_GAME_XBE):
            shutil.copyfile(
                FILE_GAME_XBE,
                FILE_MODIFIED_XBE,
                follow_symlinks=False
            )
            pass
        else:
            print(f'Files \"{FILE_GAME_XBE}\" and \"{FILE_MODIFIED_XBE}\" do not exist!')
            print('Either one needs to exist!')
            print('Please extract!')
            return
        pass
    print('Done copying\n')

    print('Packing TFS files...')
    subprocess.run([
        'py',
        '-3',
        exe_tfs.absolute(),
        '--create',
        f'--input={DIR_WORKING_TFS}',
        f'--output={DIR_MODIFIED_RESOURCES}'
    ])
    print('Done packing\n')

    print('Copying game files...')
    for i in glob.glob('*', root_dir=DIR_GAME_RESOURCES):
        fp_src = f'{DIR_GAME_RESOURCES}{os.path.sep}{i}'
        fp_dst = f'{DIR_MODIFIED_RESOURCES}{os.path.sep}{i}'
        if not i.endswith('.tfs'):
            print(f'Copying file \"{fp_src}\" to \"{fp_dst}\"...')
            shutil.copyfile(fp_src, fp_dst, follow_symlinks=False)
            print('Done copying file\n')
            pass
        del fp_dst
        del fp_src
        del i
        continue
    print('Done copying\n')

    print('Done')
    return


def patch():
    print('Patching...\n')

    print('Patching XBE...')
    print('TODO')
    print('Done patching XBE\n')

    print('Done patching')
    return


def extract(exe_tfs: pathlib.Path):
    print('Extracting...\n')

    if not os.path.exists(DIR_XBE):
        print(f'Directory \"{DIR_XBE}\" does not exist')
        print('Creating...')
        os.makedirs(DIR_XBE)
        pass

    if not os.path.exists(DIR_ORIGINAL):
        print(f'Directory \"{DIR_ORIGINAL}\" does not exist')
        print('Creating...')
        os.makedirs(DIR_ORIGINAL)
        pass
    if not os.path.exists(DIR_ORIGINAL_TFS):
        print(f'Directory \"{DIR_ORIGINAL_TFS}\" does not exist')
        print('Creating...')
        os.makedirs(DIR_ORIGINAL_TFS)
        pass

    if not os.path.exists(DIR_EXTRACTED):
        print(f'Directory \"{DIR_EXTRACTED}\" does not exist')
        print('Creating...')
        os.makedirs(DIR_EXTRACTED)
        pass
    if not os.path.exists(DIR_EXTRACTED_TFS):
        print(f'Directory \"{DIR_EXTRACTED_TFS}\" does not exist')
        print('Creating...')
        os.makedirs(DIR_EXTRACTED_TFS)
        pass

    print('Copying game files...')
    shutil.copyfile(
        FILE_GAME_XBE,
        FILE_XBE_XBE
    )
    print('Done copying\n')

    for i in glob.glob('*.tfs', root_dir=DIR_GAME_RESOURCES):
        print(f'Found `TFS` file \"{i}\"')

        print('Copying...')
        shutil.copyfile(
            os.path.join(DIR_GAME_RESOURCES, i),
            f'{DIR_ORIGINAL_TFS}{os.path.sep}{i}',
            follow_symlinks=False
        )
        print('Done copying...\n')

        print('Extracting TFS...')
        subprocess.run([
            'py',
            '-3',
            exe_tfs.absolute(),
            '--extract',
            f'--input={DIR_GAME_RESOURCES}{os.path.sep}{i}',
            f'--output={DIR_EXTRACTED_TFS}'
        ])
        print('Done extracting TFS\n')
        del i
        continue

    print('Done extracting\n')

    if os.path.exists(DIR_WORKING):
        print(f'Directory \"{DIR_WORKING}\" already exists! Cannot copy files!')
        return
    else:
        print(f'Copying \"{DIR_EXTRACTED}\" to \"{DIR_WORKING}\"...')
        shutil.copytree(
            f'{DIR_EXTRACTED}',
            f'{DIR_WORKING}',
            dirs_exist_ok=False,
            symlinks=False
        )
        print('Done copying\n')
        pass

    print('Done')
    return


def check_paths(exe_tfs: pathlib.Path):
    # GAME
    if not os.path.exists(DIR_GAME):
        print(f'Directory \"{DIR_GAME}\" does not exist!')
        pass
    if not os.path.exists(DIR_GAME_RESOURCES):
        print(f'Directory \"{DIR_GAME_RESOURCES}\" does not exist!')
        pass
    if not os.path.exists(FILE_GAME_XBE):
        print(f'File \"{FILE_GAME_XBE}\" does not exist!')
        pass

    # EXE
    if not os.path.exists(exe_tfs):
        print(f'Executable \"{exe_tfs}\" does not exist!')
        pass
    return


def main():
    import argparse
    arg = argparse.ArgumentParser()
    arg.add_argument('--stage', required=True, choices=STAGES)
    arg.add_argument('--tfs', required=True)  # path to tfs/main.py
    args = arg.parse_args()
    del arg

    exe_tfs = pathlib.Path(args.tfs)

    check_paths(exe_tfs)

    if args.stage == STAGES[0]:  # extract
        extract(exe_tfs)
        pass
    elif args.stage == STAGES[1]:  # patch
        patch()
        pass
    elif args.stage == STAGES[2]:  # build
        build(exe_tfs)
        pass
    else:
        print(f'Unknown stage \"{args.stage}\"!')
        pass
    return


if __name__ == '__main__':
    main()
    pass
