#!/usr/bin/env python3

"""FoV patch for the NT client binary with SourceMod plugin controllable adjustment support."""

import os
import shutil
import sys


def create_clientdll_backup(file_path):
    """Backs up the file_path as file_path.backup, if the backup doesn't exist yet."""
    backup_file = f"{file_path}.backup"
    if not os.path.exists(backup_file):
        print(f'Backing up file "{file_path}" as "{backup_file}"')
        shutil.copyfile(file_path, backup_file)
        return True
    print(f'Skipping writing of backup file "{backup_file}" since it already exists.')
    return False


def patch_closecaption_to_fovispatched(file_path):
    """Patch the first instance of b"closecaption" to b"fovispatched".

    Expects to find exactly 5 instances of b"closecaption" bytes,
    as is the case with a binary where this hasn't been modified.
    """
    with open(file_path, mode="rb+") as f:
        data = f.read()
        pattern = b"closecaption"
        replace_pattern_with = b"fovispatched"
        assert len(pattern) == len(replace_pattern_with)

        offset = 0
        matches = []
        while True:
            try:
                offset += data[offset:].index(pattern)
                matches.append(offset)
                offset += 1
            except ValueError:
                break
        print(f"{matches=}")
        assert len(matches) == 5
        # The target offset here is the first match.
        closecaption_offset = matches[0]

        f.seek(closecaption_offset)
        f.write(replace_pattern_with)
        print(f"Successfully patched byte(s) at offset: {closecaption_offset}")


def patch_fov_entprop(file_path):
    """Patch the FoV entprop of client."""
    raise NotImplementedError  # FIXME


def main():
    """Entry point."""
    if len(sys.argv) != 2:
        print(
            f'Usage: python "{sys.argv[0]}" '
            r'"C:\path\to\Steam\steamapps\common\NEOTOKYO\NeotokyoSource\bin\client.dll"'
        )
        return
    file_path = sys.argv[1]
    assert os.path.exists(file_path), f"Path doesn't exist: {file_path}"
    assert os.path.isfile(file_path), f"Path is not a file: {file_path}"
    create_clientdll_backup(file_path)
    patch_closecaption_to_fovispatched(file_path)
    patch_fov_entprop(file_path)


if __name__ == "__main__":
    main()
