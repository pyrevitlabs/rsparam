"""Utilities for working with Revit shared parameter files."""


import codecs
import csv
from collections import namedtuple


class SharedParamFileItem(object):
    def __init__(self, lineno):
        self.lineno = lineno


class SharedParamGroup(SharedParamFileItem):
    def __init__(self, args, lineno=None):
        super(SharedParamGroup, self).__init__(lineno)
        self.id = args[0]
        self.desc = args[1]

    def __str__(self):
        return self.desc

    def __iter__(self):
        return iter([self.id, self.desc])

    def __repr__(self):
        return '<{} desc:"{}" id:{}>'.format(self.__class__.__name__,
                                             self.desc, self.id)

    def __hash__(self):
        return self.id


class SharedParam(SharedParamFileItem):
    def __init__(self, args, lineno=None):
        super(SharedParam, self).__init__(lineno)
        self.guid = args[0]
        self.name = args[1]
        self.datatype = args[2]
        self.datacategory = args[3]
        self.group = args[4]
        self.visible = args[5]
        self.desc = args[6]
        self.usermod = args[7]

    def __str__(self):
        return self.desc

    def __iter__(self):
        return iter([self.guid, self.name, self.datatype,
                     self.datacategory, self.group, self.visible,
                     self.desc, self.usermod])

    def __repr__(self):
        return '<{} name:"{}" guid:{}>'.format(self.__class__.__name__,
                                               self.name, self.guid)

    def __hash__(self):
        return self.guid


def get_params(src_file, encoding=None):
    # open file and collect shared param and groups
    spgroups = []
    sparams = []
    with codecs.open(src_file, 'r', encoding) as spf:
        count = 0
        for line in csv.reader(spf, delimiter="\t"):
            if len(line) >= 1:
                if line[0] == 'PARAM':
                    sparam = SharedParam(line[1:], lineno=count)
                    sparams.append(sparam)
                elif line[0] == 'GROUP':
                    spgroup = SharedParamGroup(line[1:], lineno=count)
                    spgroups.append(spgroup)
            count += 1

    # now update sparams with group obj
    for sp in sparams:
        for spg in spgroups:
            if sp.group == spg.id:
                sp.group = spg

    return spgroups, sparams


def find_duplicates(src_file):
    collected_params = {}
    pass


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
