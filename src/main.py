import argparse
from sys import argv
from os import getcwd
from pathlib import Path
from PyAutoHotKey import PyAutoHotKey

def main():
    instance = PyAutoHotKey()

    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='The file path to execute')
    args = parser.parse_args(argv[1:])
    file_path = Path(f'{getcwd()}/{args.file_path}').resolve()

    instance.execute_file(file_path)

if __name__ == '__main__':
    main()