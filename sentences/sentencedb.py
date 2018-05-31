import re
import gzip
import os
from typing import List, Dict, Union
from concurrent import futures

_DEFAULT_DB = os.path.join(os.path.dirname(__file__), 'tags')


class SentenceDB(object):
    DEFAULT_DB = _DEFAULT_DB
    BAD_CHARS = '\\/:?%*|'

    def __init__(self, db_path: str = _DEFAULT_DB):
        self.db_path = db_path or self.DEFAULT_DB
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)

    @classmethod
    def escape_filename(cls, name: str) -> str:
        return ''.join(c if c not in cls.BAD_CHARS else '_' for c in name)

    def search(self, tag_re: Union[str, None], sentence_re: Union[str, None]) -> List[Dict[str, str]]:
        tr = re.compile(tag_re) if tag_re else None
        sr = re.compile(sentence_re) if sentence_re else None

        futs = []
        for tag in os.listdir(self.db_path):
            path = os.path.join(self.db_path, tag)
            if os.path.isdir(path) or (tr and not tr.search(tag)):
                continue
            try:
                with gzip.open(path, 'rt') as gz:
                    for line in gz:
                        line = line.rstrip()
                        if not sr or sr.search(line):
                            yield {'tag': tag, 'sentence': line}
            except OSError:
                pass

    def add(self, tag: str, sentences: List[str], replace: bool = False, unique: bool = False) -> None:
        tag = self.escape_filename(tag)
        seen = set()
        with gzip.open(os.path.join(self.db_path, tag), 'wt' if replace else 'at', compresslevel=4) as gz:
            for sentence in sentences:
                sentence = sentence.strip()
                if unique:
                    h = hash(sentence)
                    if h in seen:
                        continue
                    seen.add(h)
                if sentence:
                    gz.write(sentence + '\n')

    def delete(self, tag: str) -> bool:
        path = os.path.join(self.db_path, tag)
        if not os.path.isfile(path):
            return False
        os.unlink(path)
        return True

    def tags(self) -> set:
        return {tag for tag in os.listdir(self.db_path) if os.path.isfile(os.path.join(self.db_path,tag))}
