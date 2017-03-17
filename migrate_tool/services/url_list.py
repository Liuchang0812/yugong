# -*- coding: utf-8 -*-


from migrate_tool import storage_service
from migrate_tool import task
from logging import getLogger
import requests
import urlparse

logger = getLogger(__name__)


class UrlListService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):
        self._url_list_file = kwargs['url_list_file']
        self._timeout = float(kwargs['timeout'])
        self._chunk_size = 1024

    def download(self, task, local_path):

        url_path = task.other

        for i in range(5):
            try:
                ret = requests.get(url_path, timeout=self._timeout)
                if ret.status_code == 200:
                    with open(local_path, 'wb') as fd:
                        for chunk in ret.iter_content(self._chunk_size):
                            fd.write(chunk)
                        fd.flush()
                    break
                else:
                    # print "task: ", task
                    raise IOError("NOTICE: download failed")
            except:
                logger.exception("download failed")
        else:
            raise IOError("NOTICE: download failed with retry 5")

    def upload(self, task, local_path):
        raise NotImplementedError

    def list(self):
        with open(self._url_list_file, 'r') as f:
            for line in f:
                try:
                    ret = urlparse.urlparse(line)
                    if ret.path == '':
                        logger.warn("{} is invalid, No path".format(line))
                    logger.info("yield new object: {}".format(str({'store_path': ret.path.strip(), 'url_path': line.strip()})))
                    yield task.Task(ret.path.strip()[1:], None, line.strip())

                except Exception:
                    logger.warn("{} is invalid".format(line))

    def exists(self, _path):
        raise NotImplementedError
