#!/usr/bin/env python3

from sys import stdin, stderr
from sentencedb import SentenceDB
from entrypoint2 import entrypoint


@entrypoint
def main(sentence=None,
         category=None,
         append=False,
         replace=False,
         delete=False,
         list_categories=False,
         limit=None,
         db_path=None,
         format='{category}: {sentence}'):
    """Manage/search a DB of example sentences.

    sentence: Globbing sentence search pattern or input sentence for append/replace operations.
    category: Globbing category search pattern or category for append/replace operations.
    append: Add sentences to a category. Either use --sentence to specify a single sentence or pipe lines into stdin.
    replace: Like --append, but clears the category before inserting.
    delete: Delete sentences matching the --sentence AND --category patterns.
    limit: Limit number of search results shown.
    db_path: Alternate path for sqlite3 DB.
    format: Format string to use for search results. Uses Python's str.format(), available fields: category, sentence. Ex.: '{category}: {sentence}'
    """

    db = SentenceDB(db_path)
    if list_categories:
        for res in db.categories():
            print('{category}: {count}'.format(**res))
        return

    if append or replace:
        category = category or ''
        if replace:
            db.delete(category, '*')
        sent_in = [sentence] if stdin.isatty() else stdin
        db.add([(category, line.strip()) for line in sent_in])
        return

    if delete:
        if not sentence:
            print('Error: You need to specify at least --sentence to delete.', file=stderr)
            return 1
        print('Deleted {} sentences.'.format(db.delete(category, sentence)))
        return

    sentence = sentence or '*'
    category = category or '*'
    limit = int(limit) if type(limit) is str else None
    for res in db.search(category, sentence, limit):
        print(format.format(**res))
