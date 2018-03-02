#!/usr/bin/env python
"""Utilities for working with Revit shared parameter files

Usage:
    rsparam.py (-h | --help)
    rsparam.py (-V | --version)
    rsparam.py [-q -e <encod>] list [-a] <src_file>
    rsparam.py [-q -e <encod>] list [-p -g] <src_file>
    rsparam.py [-q -e <encod>] list -p [-f <groupid>] <src_file>
    rsparam.py [-q -e <encod>] find dupl [-n -a -p -g] <src_file>
    rsparam.py [-q -e <encod>] find <search_string> [-p -g] <src_file>
    rsparam.py [-q -e <encod>] comp [-p -g -1 -2] <first_file> <second_file>
    rsparam.py [-q -e <encod>] merge <dest_file> <src_files>...
    rsparam.py [-q -e <encod>] sort [-n] <src_file> <dest_file>

Options:
    -h, --help                          Show this help.
    -V, --version                       Show version.
    -q, --quiet                         Quiet mode.
    -e <encod>, --encode <encod>        File encoding.
    -a, --all                           All items.
    -p, --params                        Parameters only.
    -g, --groups                        Parameter groups only.
    -f <groupid>, --filter <groupid>    Filter by group id.
    -n, --byname                        Compare by name.
    -1, --first                         First file only.
    -2, --second                        Second file only.
"""


from docopt import docopt
import colorful
from tabulate import tabulate

# temp manual link for testing
import sys
sys.path.append(r'C:\Users\eirannejad\Desktop\gits\rsp')

import rsparam


_quiet = False              # global quiet mode flag
_encoding = None            # global encoding for reading files


def report(message):
    if not _quiet:
        print(message)


def report_globals():
    enc_report = 'encoding={}'.format(_encoding) if _encoding \
        else 'encoding not set'
    report(colorful.yellow(enc_report))


def report_filenames(sparam_files,
                     title='shared parameter file: ',
                     colorfunc=colorful.blue):
    if not isinstance(sparam_files, list):
        sparam_files = [sparam_files]
    for sparam_file in sparam_files:
        report(colorfunc(f'{title}{sparam_file}'))


def list_params(src_file, sparams=None, groupid=None):
    if not sparams:
        sparams = rsparam.get_params(src_file,
                                     encoding=_encoding, groupid=groupid)

    sparamdata = []
    for sp in sparams:
        sparamdata.append((sp.guid, sp.name, sp.datatype, sp.group, sp.lineno))
    print(tabulate(sparamdata,
                   headers=('Guid', 'Name', 'Datatype', 'Group', 'Line #')))


def list_groups(src_file, spgroups=None):
    if not spgroups:
        spgroups = rsparam.get_paramgroups(src_file, encoding=_encoding)

    spgroupdata = []
    for spg in spgroups:
        spgroupdata.append((spg.guid, spg.name, spg.lineno))
    print(tabulate(spgroupdata, headers=('Id', 'Description', 'Line #')))


def list_all(src_file):
    list_groups(src_file)
    list_params(src_file)


def find_param_dupls(src_file, byname=False):
    spentries = rsparam.find_duplicates(src_file, byname=byname)
    duplparam = 'name' if byname else 'guid'
    dupldata = []
    report(colorful.yellow('\nduplicate params by {}:'.format(duplparam)))
    for dlist in spentries.params:
        for d in dlist:
            dupldata.append((d.name if byname else d.guid,
                             d.guid if byname else d.name,
                             d.datatype, d.group, d.lineno))
        print(colorful.yellow('\ndupicates by {}: {}'.format(duplparam,
                                                             dupldata[0][0])))
        print(tabulate(dupldata,
                       headers=('Name' if byname else 'Guid',
                                'Guid' if byname else 'Name',
                                'Datatype', 'Group', 'Line #')))


def find_group_dupls(src_file, byname=False):
    spentries = rsparam.find_duplicates(src_file, byname=byname)
    duplparam = 'name' if byname else 'guid'
    dupldata = []
    report(colorful.yellow('\nduplicate groups by {}:'.format(duplparam)))
    for dlist in spentries.groups:
        for d in dlist:
            dupldata.append((d.name if byname else d.guid,
                             d.guid if byname else d.name,
                             d.lineno))
        print(colorful.yellow('\ndupicates by {}: {}'.format(duplparam,
                                                             dupldata[0][0])))
        print(tabulate(dupldata,
                       headers=('Name' if byname else 'Guid',
                                'Guid' if byname else 'Name',
                                'Line #')))


def find_all_dupls(src_file, groupsonly=False, paramsonly=False):
    if not paramsonly:
        find_group_dupls(src_file)
        find_group_dupls(src_file, byname=True)

    if not groupsonly:
        find_param_dupls(src_file)
        find_param_dupls(src_file, byname=True)


def find_matching(src_file, search_str, groupsonly=False, paramsonly=False):
    spentries = rsparam.find(src_file, search_str, encoding=_encoding)
    if spentries.groups and not paramsonly:
        report(colorful.yellow('\ngroups matching: {}'.format(search_str)))
        list_groups(None, spgroups=spentries.groups)

    if spentries.params and not groupsonly:
        report(colorful.yellow('\nparams matching: {}'.format(search_str)))
        list_params(None, sparams=spentries.params)


def comp(first_file, second_file,
         listfirstonly=False, listsecondonly=False,
         groupsonly=False, paramsonly=False):
    uniq1, uniq2 = rsparam.compare(first_file, second_file, encoding=_encoding)
    if uniq1.groups and not paramsonly and not listsecondonly:
        report(colorful.yellow('\nunique groups in first'))
        list_groups(None, spgroups=uniq1.groups)

    if uniq2.groups and not paramsonly and not listfirstonly:
        report(colorful.yellow('\nunique groups in second'))
        list_groups(None, spgroups=uniq2.groups)

    if uniq1.params and not groupsonly and not listsecondonly:
        report(colorful.yellow('\nunique parameters in first'))
        list_params(None, sparams=uniq1.params)

    if uniq2.params and not groupsonly and not listfirstonly:
        report(colorful.yellow('\nunique parameters in second'))
        list_params(None, sparams=uniq2.params)


def merge(dest_file, source_files):
    raise NotImplementedError()


def sort(source_file, dest_file, byname=False):
    raise NotImplementedError()


def main():
    args = docopt(__doc__, version='rsparam {}'.format(rsparam.__version__))

    # set global flags
    _quiet = args['--quiet']
    _encoding = args['--encode']
    report_globals()

    # process command line args
    # print(args)
    # exit()
    if args['list']:
        src_file = args['<src_file>']
        report_filenames(src_file, title='source file: ')
        if args['--groups'] and not args['--params']:
            # list groups only
            list_groups(src_file)
        elif args['--params'] and not args['--groups']:
            # list params only
            list_params(src_file, groupid=args['--filter'])
        else:
            # list everything
            list_all(src_file)

    elif args['find']:
        src_file = args['<src_file>']
        report_filenames(src_file, title='source file: ')
        if args['dupl']:
            if args['--params']:
                if args['--all']:
                    find_all_dupls(src_file, paramsonly=True)
                else:
                    find_param_dupls(src_file, byname=args['--byname'])
            elif args['--groups']:
                if args['--all']:
                    find_all_dupls(src_file, groupsonly=True)
                else:
                    find_group_dupls(src_file, byname=args['--byname'])
            else:
                find_all_dupls(src_file)
        else:
            find_matching(src_file, args['<search_string>'],
                          paramsonly=args['--params'],
                          groupsonly=args['--groups'])

    elif args['comp']:
        first_file = args['<first_file>']
        report_filenames(first_file, title='first file: ')
        second_file = args['<second_file>']
        report_filenames(second_file, title='second file: ')
        comp(first_file, second_file,
             listfirstonly=args['--first'], listsecondonly=args['--second'],
             paramsonly=args['--params'], groupsonly=args['--groups'])

    elif args['merge']:
        dest_file = args['<dest_file>']
        report_filenames(dest_file, title='destination file: ')
        src_files = args['<src_files>']
        report_filenames(src_files, title='source file: ')
        merge(dest_file, src_files)

    elif args['sort']:
        source_file = args['<src_file>']
        report_filenames(source_file, title='source file: ')
        dest_file = args['<dest_file>']
        report_filenames(dest_file, title='destination file: ')
        sort(source_file, dest_file, byname=args['--byname'])

    report('')
