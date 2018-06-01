#!/usr/bin/env python3
# coding = utf-8

from entrypoint2 import entrypoint
from epwdb import EpwDB

@entrypoint
def main(search_regex=None,
         dict_regex=None,
         base_dir=None,
         prepare=False,
         list_dicts=False,
         limit=None,
         format='[{dict}] {heading}:\n{text}\n'):
    """Search EPWING dictionaries.

    search_regex: Regex to use for searching entry headings.
    dict_regex: Regex to match against dictionary names.
    list_dicts: List currently usable dictionaries.
    prepare: Prepare an EPWING dictionary for use. Put your EPWING directories in in the epwing_dicts dir before calling this.
    base_dir: Base dir for looking for the epwing_dicts folder and storing prepared dicts in.
    format: Output format for search results. Uses Python's str.format(), passes variables dict,heading,text. Ex.: '[{dict}] {heading}:\\n{text}\\n'
    limit: Limit number of results output."""
    db = EpwDB(base_dir)
    if prepare:
        db.prepare()

    if list_dicts:
        print('\n'.join(db.dicts()))
        return

    limit = int(limit) if type(limit) is str else -1
    for res in db.search(dict_regex, search_regex):
        print(format.format(**res))
        limit -= 1
        if limit == 0:
            break
