from setuptools  import setup
# from distutils.core import setup

setup(
    name='migrate_tool',
    version='0.0.1',
    packages=['migrate_tool', 'migrate_tool.services'],
    url='https://www.qcloud.com/',
    license='MIT',
    author='liuchang',
    author_email='liuchang0812@gmail.com',
    description='migrate tool for object storage services',
    entry_points={
        'console_scripts': [
            'yugong=migrate_tool.main:main_'
        ],
        'storage_services': [
            'localfs=migrate_tool.services.LocalFileSystem:LocalFileSystem',
            'oss=migrate_tool.services.oss:OssStorageService',
            'qiniu=migrate_tool.services.qiniu:QiniuStorageService',
            'cosv4=migrate_tool.services.cosv4:CosV4StorageService',
            'url=migrate_tool.services.url_list:UrlListService',
        ]
   }
)
