from setuptools  import setup
# from distutils.core import setup

setup(
    name='migrate_tool',
    version='0.0.1',
    packages=['migrate_tool', 'migrate_tool.services'],
    url='',
    license='MIT',
    author='liuchang',
    author_email='liuchang0812@gmail.com',
    description='migrate tool for object storage services',
    entry_points={
        'console_scripts': [
            'yugong=migrate_tool.main:main_'
        ],
        'storage_services': [
            'localfs=migrate_tool.services.LocalFileSystem:make'
        ]
   }
)
