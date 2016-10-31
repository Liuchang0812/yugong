# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, with_statement

from migrate_tool import storage_service

class LocalFileSystem(storage_service.StorageService):

    def __init__(self, *args, **kwargs):
        self._workspace = kwargs['workspace']
        print(self._workspace)

    def exists(self, path):
        from os import path
        rt = path.join(self._workspace, path)
        return path.exists(rt)

    def download(self, path, localpath):
        src_path = path.join(self._workspace, path)
        import shutil
        return shutil.move(src_path, localpath)

    def upload(self, path, localpath):
        src_path = path.join(self._workspace, path)
        import shutil
        return shutil.move(localpath, src_path)

    def list(self, path=None):

        from os import path as path_
        if path is not None:
            src_path = path_.join(self._workspace, path)
        else:
            src_path = self._workspace
        print("WordDir: " + src_path)
        return os.listdir(src_path)

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
