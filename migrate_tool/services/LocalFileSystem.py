# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, with_statement
import os
from os import path

from migrate_tool import storage_service


class LocalFileSystem(storage_service.StorageService):

    def __init__(self, *args, **kwargs):
        self._workspace = kwargs['workspace']

    def exists(self, path_):
        rt = path.join(self._workspace, path_)
        return path.exists(rt)

    def download(self, path_, localpath):
        src_path = path.join(self._workspace, path_)
        import shutil
        return shutil.move(src_path, localpath)

    def upload(self, path_, localpath):
        src_path = path.join(self._workspace, path_)
        try:
            import os
            os.makedirs(path.dirname(src_path))
        except OSError:
            pass

        import shutil
        return shutil.move(localpath, src_path)

    def list(self):
        return os.listdir(self._workspace)


def make():
    """ hook function for entrypoints

    :return:
    """
    return LocalFileSystem

if __name__ == "__main__":
    import os
    fs = LocalFileSystem(workspace=os.getcwd())
    for f in fs.list():
        print(f)
