#!/usr/bin/env python3

import sys
from jmdb import JmDB, JmDBError
from entrypoint2 import entrypoint


@entrypoint
def main(search_regex,
         search_fields=None,
         prepare=False,
         jmdict_url=None,
         db_path=None,
         output_format=None):
    """Searches JMDict.

    search_regex: Python regex to use for searching. Matches substrings, use ^ and $ if you need whole matches.
    search_fields: Comma-separated list of fields to search. Valid fields are: kanji, reading, meaning, pos, misc
    prepare: Download JMDict and prepare it for searching before doing anything else. Must be done once before searches are possible.
    jmdict_url: Specify alternate URL to download JMDict from.
    db_path: Specify alternate path for the prepared JMDict DB.
    output_format: Format string to use for search results. Uses Python's str.format(), passes all search_fields. Ex.: '{kanji} [{reading}] ({pos},{misc}): {meaning}' """

    try:
        db = JmDB(db_path)
        if prepare:
            db.prepare(jmdict_url)
        fields = set(search_fields.split(',')) if search_fields else set()
        output_format = output_format or '{kanji} [{reading}] ({pos},{misc}): {meaning}'
        for res in db.search(search_regex, fields=fields):
            print(output_format.format(**{k: ','.join(v) for k, v in res.items()}))
    except JmDBError as ex:
        print('Error: ' + str(ex), file=sys.stderr)
        return 1
