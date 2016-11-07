# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pkg_resources
from ConfigParser import SafeConfigParser
from logging import getLogger, basicConfig, DEBUG
from sys import stderr
from argparse import ArgumentParser
import os
from os import path

from migrate_tool.migrator import ThreadMigrator

import signal
from logging.config import dictConfig
from threading import Thread
import sys
reload(sys)
sys.setdefaultencoding('utf8') 

log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'error': {
            'format': '%(asctime)s\t%(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'error_file': {
            'level': 'INFO',
            'formatter': 'error',
            'class': 'logging.FileHandler',
            'filename': 'fail_files.txt',
            'mode': 'a'
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'migrate_tool.fail_file': {
            'handlers': ['error_file'],
            'level': 'WARN',
            'propagate': False
        },
    }
}


services_ = {}


def loads_services():
    global services_
    for ep in pkg_resources.iter_entry_points(group='storage_services'):
        services_.update({ep.name: ep.load()})


def create_parser():
    parser_ = ArgumentParser()
    parser_.add_argument('-c', '--conf', type=file, required=True, help="specify your config")
    return parser_


def main_thread():

    parser = create_parser()
    opt = parser.parse_args()
    conf = SafeConfigParser()
    conf.readfp(opt.conf)

    output_service_conf  = dict(conf.items('source'))
    input_service_conf = dict(conf.items('destination'))
    if conf.has_option('common', 'threads'):
        _threads = conf.getint('common', 'threads')
    else:
        _threads = 10
    workspace_ = conf.get('common', 'workspace')
    try:
        os.makedirs(workspace_)
    except OSError:
        pass

    log_config['handlers']['error_file']['filename'] = path.join(workspace_, 'failed_files.txt')
    dictConfig(log_config)

    loads_services()
    output_service = services_[output_service_conf['type']](**output_service_conf)
    input_service = services_[input_service_conf['type']](**input_service_conf)


    migrator = ThreadMigrator(input_service=input_service, output_service=output_service, work_dir=conf.get('common', 'workspace'), threads=_threads)
    migrator.start()

    import time
    try:
        while True:
            state = migrator.status()

            if state['finish']:
                break
            time.sleep(3)

    except KeyboardInterrupt:
       state = migrator.status()
       print state
       import sys
       sys.exit()

    migrator.stop()
    state = migrator.status()
    print state

def main_():
    thread_ = Thread(target=main_thread)
    thread_.daemon=True
    thread_.start()
    try:
        while thread_.is_alive():
            thread_.join(2)
    except KeyboardInterrupt:
        print 'exiting'
    
if __name__ == '__main__':
    main_()
