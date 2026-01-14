#!/usr/bin/python3

import argparse
import datetime
import os
from builtins import NotADirectoryError
import shutil
import tempfile


boards = {
    "LR3PRO": {
        "PCB": "X7",
        "PCBREV": "LR3PRO",
        "DEFAULT_MODE": "2",
    },
    "LR2": {
        "PCB": "X7",
        "PCBREV": "LR2",
        "DEFAULT_MODE": "2",
    },
}

translations = [
    "EN",
]


def timestamp():
    return datetime.datetime.now().strftime("%y%m%d")


def build(board, translation, srcdir):
    generator = os.environ.get("CMAKE_GENERATOR", "Ninja")
    cmake_options = " ".join(["-D%s=%s" % (key, value) for key, value in boards[board].items()])
    toolchain = os.path.join(srcdir, "cmake", "toolchain", "arm-none-eabi.cmake")
    cwd = os.getcwd()
    if not os.path.exists("output"):
        os.mkdir("output")
    path = tempfile.mkdtemp()
    os.chdir(path)
    command = "cmake -G \"%s\" %s -DTRANSLATIONS=%s -DBETAFPV_RELEASE=YES -DEdgeTX_SUPERBUILD=OFF -DNATIVE_BUILD=OFF -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=\"%s\" %s" % (
        generator,
        cmake_options,
        translation,
        toolchain,
        srcdir,
    )
    print(command)
    os.system(command)
    os.system("cmake --build . --target firmware --parallel 16")
    os.chdir(cwd)
    index = 0
    while 1:
        suffix = "" if index == 0 else "_%d" % index
        filename = "output/firmware_%s_%s_%s%s.bin" % (board.lower(), translation.lower(), timestamp(), suffix)
        if not os.path.exists(filename):
            shutil.copy("%s/arm-none-eabi/firmware.bin" % path, filename)
            break
        index += 1
    shutil.rmtree(path)


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def main():
    parser = argparse.ArgumentParser(description="Build BETAFPV firmware")
    parser.add_argument("-b", "--boards", action="append", help="Destination boards", required=True)
    parser.add_argument("-t", "--translations", action="append", help="Translations", required=True)
    parser.add_argument("srcdir", type=dir_path)

    args = parser.parse_args()

    for board in (boards.keys() if "ALL" in args.boards else args.boards):
        for translation in (translations if "ALL" in args.translations else args.translations):
            build(board, translation, args.srcdir)


if __name__ == "__main__":
    main()
