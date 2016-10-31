# -*- coding: utf-8 -*-

import pkg_resources

def main_():
    named_objects = {}
    for ep in pkg_resources.iter_entry_points(group='storage_services'):
        named_objects.update({ep.name: ep.load()()})

    print named_objects
