#!/usr/bin/env python3

from sys import stdin, stderr
from sentencedb import SentenceDB
from entrypoint2 import entrypoint

@entrypoint
def main(sentence=None,
         tag=None,
         append=False,
         replace=False,
         delete=False,
         list_tags=False,
         limit=None,
         db_path=None,
         print_tag=False):
    """Manage/search a DB of example sentences.

    sentence: Sentence search regex or input sentence for append/replace operations.
    tag: Tag search regex or tag for append/replace operations.
    append: Add sentences to a tag. Either use --sentence to specify a single sentence or pipe lines into stdin.
    replace: Like --append, but clears the tag before inserting.
    delete: Delete tag.
    list_tags: List all tags.
    limit: Limit number of search results shown.
    db_path: Alternate path (directory) for tags storage.
    print_tag: Print the tag name in front of every result.'
    """

    db = SentenceDB(db_path)
    if list_tags:
        for tag in db.tags():
            print(tag)
        return

    if append or replace:
        if not tag:
            print('Error: You need to specify a tag.', file=stderr)
            return 1
        sent_in = [sentence] if stdin.isatty() else stdin
        db.add(tag, sent_in, replace=replace)
        return

    if delete:
        if not tag:
            print('Error: You need to specify a tag.', file=stderr)
            return 1
        return

    limit = int(limit) if type(limit) is str else -1
    for res in db.search(tag, sentence):
        print(res['tag'] + ': ' + res['sentence'] if print_tag else res['sentence'])
        limit -= 1
        if not limit:
            return
