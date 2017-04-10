# -*- coding: utf-8 -*-


from migrate_tool import storage_service
from migrate_tool import task
from logging import getLogger
import requests
import urlparse
import hashlib

logger = getLogger(__name__)


class UrlListService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):
        self._url_list_file = kwargs['url_list_file']
        self._timeout = float(kwargs['timeout'])
        self._chunk_size = 1024
        self._validator_method = None
        if 'validator' in kwargs:
            self._validator_method = kwargs['validator']

    def download(self, task, local_path):

        url_path = task.other
        expected_crc = task.size  # size stores the sha1 or md5 of file

        for i in range(5):
            validator = None
            if self._validator_method:
                if self._validator_method == "sha1":
                    validator = hashlib.sha1()
                elif self._validator_method == "md5":
                    validator = hashlib.md5()
                else:
                    validator = None

            try:
                ret = requests.get(url_path, timeout=self._timeout)
                if ret.status_code == 200:
                    with open(local_path, 'wb') as fd:
                        for chunk in ret.iter_content(self._chunk_size):
                            if validator:
                                validator.update(chunk)
                            fd.write(chunk)
                        fd.flush()
                    # validate
                    if validator:
                        actual_crc = validator.hexdigest()
                        actual_crc_upper = actual_crc.upper()
                        if actual_crc != expected_crc and actual_crc_upper != expected_crc:
                            logger.debug("{}".format(str({'expected_crc:': expected_crc, 'actual_crc:': actual_crc})))
                            raise IOError("NOTICE: downloaded file content not valid")
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
                    field = line.split()
                    if len(field) < 1:
                        logger.warn("{} is invalid".format(line))
                        continue
                    check_value = None
                    url_path = None
                    if len(field) == 1:
                        url_path = field[0]
                    else:
                        check_value = field[0].strip()
                        url_path = field[1]
                    ret = urlparse.urlparse(url_path)
                    if ret.path == '':
                        logger.warn("{} is invalid, No path".format(line))
                    logger.info("yield new object: {}".format(str({'store_path': ret.path.strip(), 'url_path': url_path.strip()})))
                    yield task.Task(ret.path.strip()[1:], check_value, url_path.strip())

                except Exception:
                    logger.warn("{} is invalid".format(line))

    def exists(self, _path):
        raise NotImplementedError
