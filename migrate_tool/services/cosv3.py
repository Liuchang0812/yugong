# -*- coding: utf-8 -*-


from logging import getLogger
from contextlib import closing

from migrate_tool import storage_service
from migrate_tool.task import Task
from qcloud_cos_v3 import CosClient
from qcloud_cos_v3 import ListFolderRequest
from qcloud_cos_v3 import Auth, CredInfo

import requests

logger = getLogger(__name__)

def to_utf8(s):
  if isinstance(s, unicode):
    return s.encode('utf-8')
  else:
    return s

class CosV3StorageService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):

        appid = int(kwargs['appid'])
        accesskeyid = unicode(kwargs['accesskeyid'])
        accesskeysecret = unicode(kwargs['accesskeysecret'])
        bucket = unicode(kwargs['bucket'])
        if 'prefix' in kwargs:
            self._prefix = kwargs['prefix']
        else:
            self._prefix = None

        self._cos_api = CosClient(appid, accesskeyid, accesskeysecret)
        self._bucket = bucket
        self._appid = appid
	self._http_session = requests.session()
        self._auth = Auth(CredInfo(appid, accesskeyid, accesskeysecret))
    def __sign(self, key):
        import time
        ex = int(time.time()) + 300
        
        return self._auth.sign_download(self._bucket, key, ex)

    def download(self, task, local_path):
        key = task.key
        url_tmpl = 'http://{bucket}-{appid}.cos.myqcloud.com/{key}?sign={sign}'
        import urllib
        uri = url_tmpl.format(bucket=self._bucket, appid=self._appid, key=urllib.quote(to_utf8(key)), sign=self.__sign(key))
        session = self._http_session

	for i in range(5):
	    try:
		with closing(session.get(uri, stream=True)) as ret:
		    if ret.status_code in [200, 206]:
			with open(local_path, 'wb') as f:
			    for chunk in ret.iter_content(chunk_size=1024):
				if chunk:
				    f.write(chunk)
			    f.flush()
		    else:
			raise IOError("download failed " + ret.text)
		from os import path
		if task.size is not None and path.getsize(local_path) != task.size:
		    raise IOError("download failed with retry {times}".format(times=i))
		else:
		    break

	    except Exception:
                logger.exception("download failed with retry {times}".format(times=i))
                import time
	        time.sleep(2**min(5,i))
	else:
	    raise IOError("download failed!")

    def upload(self, task, local_path):
        raise NotImplementedError

    def __dfs_list(self, path):
        logger.info("try to dump file list under {}".format(path))

        _finish = False
        _context = u''
        max_retry = 10
        while not _finish:
            try:
                request = ListFolderRequest(bucket_name=self._bucket, cos_path=path, context=_context)
                ret = self._cos_api.list_folder(request)
            except Exception:
                logger.exception("list failed") 
                max_retry -= 1
                continue

            logger.debug(str(ret))

            if ret['code'] != 0:
                logger.warning("request failed: {}".format(str(ret)))
                max_retry -= 1
            else:
                _finish = not ret['data']['has_more']
                _context = ret['data']['context']
                for item in ret['data']['infos']:
                    if 'filelen' in item:
                        # file
                        key = "{prefix}{filename}".format(prefix=path, filename=item['name'])
                        yield Task(key, item['filelen'], None)
                    else:
                        _sub_dir = "{prefix}{filename}/".format(prefix=path, filename=item['name'])
                        if isinstance(_sub_dir, str):
                          _sub_dir = _sub_dir.decode('utf-8')
                        for i in self.__dfs_list(_sub_dir):
                          yield i
                        # directory

            if max_retry == 0:
                _finish = True
                logger.error("reach max retry times, finish this directory {}".format(path))

        logger.info("finish directory {}".format(path))
            
	
    def list(self):
	to_list_dirs = []
	
	if self._prefix is None:
	    prefix = u'/' 
        else:
            prefix = unicode(self._prefix)

	for i in self.__dfs_list(prefix):
            yield i
	
	
    def exists(self, task):
        raise NotImplementedError
