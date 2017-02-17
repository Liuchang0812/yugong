from setuptools  import setup
# from distutils.core import setup
from platform import python_version_tuple


def requirements():

    with open('requirements.txt', 'r') as fileobj:
        requirements = [line.strip() for line in fileobj]

        version = python_version_tuple()

        if version[0] == 2 and version[1] == 6:
            requirements.append("argparse==1.4.0")
        return requirements

def long_description():
    with open('README.rst', 'r') as fileobj:
        return fileobj.read()

setup(
    name='cos_migrate_tool',
    version='0.0.7',
    packages=['migrate_tool', 'migrate_tool.services'],
    url='https://www.qcloud.com/',
    license='MIT',
    author='liuchang',
    author_email='liuchang0812@gmail.com',
    description='migrate tool for object storage services',
    long_description=long_description(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'cos_migrate_tool=migrate_tool.main:main_'
        ],
        'storage_services': [
            'localfs=migrate_tool.services.LocalFileSystem:LocalFileSystem',
            'oss=migrate_tool.services.oss:OssStorageService',
            'ossmock=migrate_tool.services.oss_mock:OssMockStorageService',
            'qiniu=migrate_tool.services.qiniu:QiniuStorageService',
            'cosv4=migrate_tool.services.cosv4:CosV4StorageService',
            'url=migrate_tool.services.url_list:UrlListService',
            's3=migrate_tool.services.s3:S3StorageService',
        ]
    },
    install_requires=requirements()
)
