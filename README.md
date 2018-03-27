# rsparam
Command-line utility and python module for managing Revit Shared Parameter files.


## Installation

``` bash
pip install rsparam
```

## Usage: Command line utility

``` text
Utilities for working with Revit shared parameter files

Usage:
    rsparam (-h | --help)
    rsparam (-V | --version)
    rsparam [-q -e <encod>] list [-a] <src_file>
    rsparam [-q -e <encod>] list [-p -g] <src_file>
    rsparam [-q -e <encod>] list -p [-f <groupid>] <src_file>
    rsparam [-q -e <encod>] find dupl [-n -a -p -g] <src_file>
    rsparam [-q -e <encod>] find <search_string> [-p -g] <src_file>
    rsparam [-q -e <encod>] comp [-p -g -1 -2] <first_file> <second_file>
    rsparam [-q -e <encod>] merge <dest_file> <src_files>...
    rsparam [-q -e <encod>] sort [-n] <src_file> <dest_file>

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
```
#### Examples
`rsparam list -p /path/to/file.txt` List all parameters in source file

`rsparam list -g /path/to/file.txt` List all groups in source file

`rsparam list -pf 100 /path/to/file.txt` List all parameters in group with id 100

`rsparam find dupl -p /path/to/file.txt` List all duplicate parameters

`rsparam find dupl -pn /path/to/file.txt` List all duplicate parameters compared by name

`rsparam find Mech -g /path/to/file.txt` List any group matching string

`rsparam comp -p2 /path/to/file1.txt /path/to/file2.txt` List all unique parameters in second file

## Usage: python module

``` python
import rsparam


# returned entries are a tuple of `groups` and `params`
# rsparam.SharedParamEntries
def print_entries(entries):
    for g in entries.groups:
        # each group is rsparam.SharedParamGroup
        print(g)

    for p in entries.params:
        # each parameter is rsparam.SharedParam
        print (p)


# getting groups and parameters
spentries = rsparam.read_entries(src_file, encoding='utf-16')
print_entries(spentries)

# getting groups only
groups = rsparam.get_paramgroups(src_file)

# getting parameters only
params = rsparam.get_params(src_file)

# finding duplicate groups and params by guid (set byname=True to compare by name)
dupl_entries = rsparam.find_duplicates(src_file, byname=False)
print_entries(dupl_entries)

# find groups and parameters matching string
matched_entries = rsparam.find(src_file, searchstr)
print_entries(matched_entries)

# comparing two shared param files
uniq_first_entries, unique_second_entries = rsparam.compare(first_file, second_file)
print_entries(uniq_first_entries)
print_entries(unique_second_entries)
```
