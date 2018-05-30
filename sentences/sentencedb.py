import os
import sqlite3
from typing import Tuple, List, Dict, Union

_DEFAULT_DB = os.path.join(os.path.dirname(__file__), 'sentences.sqlite3')


class SentenceDB(object):
    DEFAULT_DB = _DEFAULT_DB

    def __init__(self, db_path: str = _DEFAULT_DB):
        self.db = sqlite3.connect(db_path or self.DEFAULT_DB)
        self.db.row_factory = self.dict_factory
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS sentences(
                category TEXT,
                sentence TEXT,
                CONSTRAINT unique_sent UNIQUE(category, sentence)
            );""")
        self.db.commit()

    @staticmethod
    def dict_factory(cursor, row):
        return dict(zip([col[0] for col in cursor.description], row))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.db.close()

    def search(self, category_glob: str, sentence_glob: str, limit: Union[int, None] = None) -> List[Dict[str, str]]:
        return self.db.execute("""
            SELECT *
            FROM sentences
            WHERE category GLOB ?
            AND sentence GLOB ?{};""".format(' LIMIT ' + str(limit) if limit else ''),
            (category_glob, sentence_glob))

    def add(self, sentences: List[Tuple]) -> None:
        self.db.executemany("INSERT OR IGNORE INTO sentences(category, sentence) VALUES(?,?);", sentences)
        self.db.commit()

    def delete(self, category_glob: str, sentence_glob: str) -> int:
        res = self.db.execute("DELETE FROM sentences WHERE category GLOB ? AND sentence GLOB ?;", (category_glob, sentence_glob))
        self.db.commit()
        return res.rowcount

    def categories(self) -> List[str]:
        return self.db.execute("SELECT category, count(*) as count FROM sentences GROUP BY category;")
