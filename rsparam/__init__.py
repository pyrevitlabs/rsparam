"""Utilities for working with Revit shared parameter files."""


import codecs
import csv
from collections import namedtuple


SharedParam = namedtuple('SharedParam', ['guid',
                                         'name',
                                         'datatype',
                                         'datacategory',
                                         'group',
                                         'visible',
                                         'description',
                                         'usermodifiable'])


def find_duplicates(src_file):
    pass


# collected_params = {}
#
#
# def is_duplicate(param, attr='guid'):
#     comp_attr = getattr(param, attr)
#     if comp_attr in collected_params.keys():
#         return True
#     else:
#         collected_params[comp_attr] = param
#
#     return False
#
#
# with codecs.open(sharedparam_file, 'r', 'utf-16') as spf:
#     for line in csv.reader(spf, delimiter="\t"):
#         if len(line) >= 1:
#             if line[0] == 'PARAM':
#                 sparam = SharedParam(*line[1:])
#                 if args['--name']:
#                     if is_duplicate(sparam, attr='name'):
#                         print(colorful.white(f'Duplicate Param Found:\n'
#                                              f'\t{sparam.name}\n'))
#                 else:
#                     if is_duplicate(sparam):
#                         print(colorful.white(f'Duplicate Param Found:\n'
#                                              f'\t{sparam.name}\n'
#                                              f'\t{sparam.guid}\n'))
