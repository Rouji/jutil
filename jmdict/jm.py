#!/usr/bin/env python3

import sys
from jmdb import JmDB, JmDBError
from entrypoint2 import entrypoint


@entrypoint
def main(regex,
         fields=None,
         prepare=False,
         jmdict_url=None,
         db_path=None,
         format=None,
         limit=None):
    """Searches (English) JMDict.

    regex: Python regex to use for searching. Matches substrings, use ^ and $ if you need whole matches.
    fields: Comma-separated list of fields to search. Valid fields are: kanji, reading, meaning, pos, misc
    prepare: Download JMDict and prepare it for searching before doing anything else. Must be done once before searches are possible.
    jmdict_url: Specify alternate URL to download JMDict from.
    db_path: Specify alternate path for the prepared JMDict DB.
    format: Format string to use for search results. Uses Python's str.format(), passes all search_fields. Ex.: '{kanji} [{reading}] ({pos},{misc}): {meaning}'
    limit: Limit number of results shown."""

    try:
        db = JmDB(db_path)
        if prepare:
            db.prepare(jmdict_url)
        fields = set(fields.split(',')) if fields else set()
        format = format or '{kanji} [{reading}] ({pos},{misc}): {meaning}'
        limit = int(limit) if type(limit) is str else -1
        for res in db.search(regex, fields=fields):
            print(format.format(**{k: ','.join(v) for k, v in res.items()}))
            limit -= 1
            if limit == 0:
                break
    except JmDBError as ex:
        print('Error: ' + str(ex), file=sys.stderr)
        return 1
