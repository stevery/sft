import sys
import optparse
from pathlib import Path, PurePath, PurePosixPath
import magic
import hashlib
import pandas as pd
from pandas import DataFrame


class Idpy:
    def __init__(self, in_path):
        self.in_path = self.build_ab_path(in_path)
        self.files = []


    def build_ab_path(self, path):
        if PurePosixPath(path).is_absolute():
            return Path(path)
        else:
            return PurePath(Path.cwd(),path)


    def map_all_files(self, path=None):
        if path == None:
            path = self.in_path

        for child in path.iterdir():
            if child.is_dir():
                self.map_all_files(child)
            elif child.is_file():
                self.files.append(child)                


def main():
    parser = optparse.OptionParser(usage="%prog -p [path]")
    parser.add_option("-p", dest="path", type="string", help="input target path")
    (options, args) = parser.parse_args()
    path = options.path

    if path is None:
        print(parser.usage)
        sys.exit(0)
    else:
        ip = Idpy(path)
        ip.map_all_files()
        result = {}
        for file in ip.files:
            tmp = {file:{}}
            tmp[file].update({'filename':PurePosixPath(file).stem+''.join(PurePosixPath(file).suffixes)})
            tmp[file].update({'size':Path(file).stat().st_size})
            tmp[file].update({'extension':''.join(PurePosixPath(file).suffixes)})
            tmp[file].update({'st_date':Path(file).stat().st_mtime})
            tmp[file].update({'type':magic.from_file(str(file))})
            tmp[file].update({'md5':hashlib.md5(open(file, 'rb').read()).hexdigest()})
            tmp[file].update({'sha1':hashlib.sha1(open(file, 'rb').read()).hexdigest()})
            tmp[file].update({'sha256':hashlib.sha256(open(file, 'rb').read()).hexdigest()})

            result.update(tmp)
            # print(tmp)
            # [filename, size, extension, filetype, md5, sha-1, sha-256]

        #print(result)
        for files in result:
            print(files)
            print(result[files])
        
        df = DataFrame.from_dict(result)
        df = df.transpose()
        print(df.head())
        df.to_csv('result.csv')


if __name__ == "__main__":
    main()

