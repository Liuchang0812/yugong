# -*- coding: utf-8 -*-

from collections import namedtuple

# digest is md5/sha1, we use it in URL-list service
Task = namedtuple("Task", ["key", "size", "other", "digest"])
