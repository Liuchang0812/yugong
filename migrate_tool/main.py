# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pkg_resources
from ConfigParser import SafeConfigParser
from logging import getLogger, basicConfig, DEBUG
from sys import stderr
from argparse import ArgumentParser
import os

from migrate_tool.migrator import ThreadMigrator

logger = getLogger(__name__)

services_ = {}


def loads_services():
    global services_
    for ep in pkg_resources.iter_entry_points(group='storage_services'):
        services_.update({ep.name: ep.load()})


def create_parser():
    parser_ = ArgumentParser()
    parser_.add_argument('-c', '--conf', type=file, required=True, help="specify your config")
    return parser_


def main_():

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

    loads_services()

    os.makedirs(conf.get('common', 'workspace'))
    output_service = services_[output_service_conf['type']](**output_service_conf)
    input_service = services_[input_service_conf['type']](**input_service_conf)


    migrator = ThreadMigrator(input_service=input_service, output_service=output_service, work_dir=conf.get('common', 'workspace'), threads=_threads)
    migrator.start()

    import time
    while True:
        state = migrator.status()

        if state['finish']:
            break
        time.sleep(3)

    migrator.stop()

if __name__ == '__main__':
    main_()
