# -*- coding: utf-8 -*-

import pkg_resources
from ConfigParser import SafeConfigParser
from logging import getLogger, basicConfig, DEBUG
from sys import stderr
basicConfig(stream=stderr, level=DEBUG)

logger = getLogger(__name__)

from argparse import ArgumentParser

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

    logger.debug(str(conf.options('source')))

    input_service_conf  = dict(conf.items('source'))
    output_service_conf = dict(conf.items('destination'))


if __name__ == '__main__':
    main_()