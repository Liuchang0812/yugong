# -*- coding: utf-8 -*-


from migrate_tool import storage_service

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
        if isinstance(task, dict) and 'url_path' in task:

            url_path = task['url_path']

            ret = requests.get(url_path, timeout=self._timeout)

            with open(local_path, 'wb') as fd:
                for chunk in ret.iter_content(self._chunk_size):
                    fd.write(chunk)

        else:
            print "task: ", task
            raise ValueError("task is invalid, task should be a dict and contains url_path")


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
                    yield {'store_path': ret.path.strip()[1:], 'url_path': line.strip()}
                except Exception:
                    logger.warn("{} is invalid".format(line))

    def exists(self, _path):
        raise NotImplementedError
