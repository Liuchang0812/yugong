# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, with_statement
import os
from os import path
from migrate_tool.task import Task
from migrate_tool import storage_service


class LocalFileSystem(storage_service.StorageService):

    def __init__(self, *args, **kwargs):
        self._workspace = kwargs['workspace']

    def exists(self, path_):
        rt = path.join(self._workspace, path_)
        return path.exists(rt)

    def download(self, task, localpath):
        path_ = task['key']
        src_path = path.join(self._workspace, path_)
        import shutil
        return shutil.copyfile(src_path, localpath)

    def upload(self, task, localpath):
        path_ = task['key']
        src_path = path.join(self._workspace, path_)
        try:
            import os
            os.makedirs(path.dirname(src_path))
        except OSError:
            pass

        import shutil
        return shutil.copyfile(localpath, src_path)

    def list(self):
        for file in os.listdir(self._workspace):
            from os import path
            yield Task(file, path.getsize(file), None, None)


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
