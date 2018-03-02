"""Utilities for working with Revit shared parameter files."""


import codecs
import csv
from collections import namedtuple, defaultdict


# pylama:ignore=D105

# rsparam version
__version__ = '0.1.0'


SharedParamEntries = namedtuple('SharedParamEntries', ['groups', 'params'])


class SharedParamFileItem(object):
    def __init__(self, lineno):
        self.lineno = lineno

    def __contains__(self, key):
        for value in self:
            if key in value:
                return True
        return False

    def __eq__(self, other):
        return hash(self) == hash(other)


class SharedParamGroup(SharedParamFileItem):
    def __init__(self, args, lineno=None):
        super(SharedParamGroup, self).__init__(lineno)
        self.guid = args[0]
        self.desc = args[1]
        self.name = self.desc

    def __str__(self):
        return self.desc

    def __iter__(self):
        return iter([self.guid, self.desc])

    def __repr__(self):
        return '<{} desc:"{}" guid:{}>'.format(self.__class__.__name__,
                                               self.desc, self.guid)

    def __hash__(self):
        return hash(self.guid + self.desc)


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
        return hash(self.guid + self.name
                    + self.datatype + self.datacategory
                    + self.visible + self.desc + self.usermod)


def read_entries(src_file, encoding=None):
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
            if sp.group == spg.guid:
                sp.group = spg

    return SharedParamEntries(spgroups, sparams)


def get_paramgroups(src_file, encoding=None):
    spgroups, sparams = read_entries(src_file, encoding=encoding)
    return spgroups


def get_params(src_file, encoding=None, groupid=None):
    spgroups, sparams = read_entries(src_file, encoding=encoding)
    if groupid:
        return [x for x in sparams if x.group.guid == groupid]

    return sparams


def find_duplicates(src_file, encoding=None, byname=False):
    param_guid_lut = defaultdict(list)
    group_guid_lut = defaultdict(list)

    spgroups, sparams = read_entries(src_file, encoding=encoding)

    duplparam = 'name' if byname else 'guid'

    for sparam in sparams:
        param_guid_lut[getattr(sparam, duplparam)].append(sparam)

    for spgroup in spgroups:
        group_guid_lut[getattr(spgroup, duplparam)].append(spgroup)

    duplgroups = [v for k, v in group_guid_lut.items() if len(v) > 1]
    duplparams = [v for k, v in param_guid_lut.items() if len(v) > 1]

    return SharedParamEntries(duplgroups, duplparams)


def find(src_file, searchstr, encoding=None):
    spgroups, sparams = read_entries(src_file, encoding=encoding)
    matchedgroups = [x for x in spgroups if searchstr in x]
    matchedparams = [x for x in sparams if searchstr in x]

    return SharedParamEntries(matchedgroups, matchedparams)


def compare(first_file, second_file, encoding=None):
    spgroups1, sparams1 = read_entries(first_file, encoding=encoding)
    spgroups2, sparams2 = read_entries(second_file, encoding=encoding)

    uniqgroups1 = [x for x in spgroups1 if x not in spgroups2]
    uniqparams1 = [x for x in sparams1 if x not in sparams2]
    uniqgroups2 = [x for x in spgroups2 if x not in spgroups1]
    uniqparams2 = [x for x in sparams2 if x not in sparams1]

    return SharedParamEntries(uniqgroups1, uniqparams1), \
        SharedParamEntries(uniqgroups2, uniqparams2)
