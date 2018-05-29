from typing import Generator, List, Dict
from contextlib import closing
from urllib.request import urlopen
from lxml import etree
import os.path
import gzip
import re

_DEFAULT_DB = os.path.join(os.path.dirname(__file__), 'jm.db')
_DEFAULT_URL = 'http://ftp.monash.edu.au/pub/nihongo/JMdict_e.gz'


class JmDBError(Exception):
    pass


class JmDB(object):
    FS = '\uE0000'  # field seperator
    IS = '\uE0001'  # item seperator
    FIELDS = ['kanji', 'reading', 'meaning', 'pos', 'misc']
    DEFAULT_URL = _DEFAULT_URL
    DEFAULT_DB = _DEFAULT_DB

    def __init__(self, db_path: str = _DEFAULT_DB):
        self.db_path = db_path or JmDB.DEFAULT_DB

    def prepare(self, jmdict_src=_DEFAULT_URL) -> None:
        jmdict_src = jmdict_src or JmDB.DEFAULT_URL
        with open(self.db_path, 'w') as db, \
                closing(urlopen(jmdict_src)) as gz, \
                gzip.GzipFile(fileobj=gz, mode='r') as unzip:
            parser = etree.XMLParser(resolve_entities=False, load_dtd=False)
            tree = etree.parse(unzip, parser=parser)

            def strip(s: str):
                return s.strip('&;')

            for entry in tree.iter('entry'):
                line = JmDB.FS.join([
                    JmDB.IS.join([e.text for e in entry.iterfind('.//keb')]),
                    JmDB.IS.join([e.text for e in entry.iterfind('.//reb')]),
                    JmDB.IS.join([e.text for e in entry.iterfind('.//gloss')]),
                    JmDB.IS.join({strip(e[0].text) for e in entry.iterfind('.//pos')}),
                    JmDB.IS.join({strip(e[0].text) for e in entry.iterfind('.//misc')}),
                ])
                db.write(line+'\n')

    @classmethod
    def parse_entry(cls, entry_line: str) -> Dict[str, List[str]]:
        return dict(zip(
            cls.FIELDS,
            [l.split(JmDB.IS) for l in entry_line.rstrip('\n').split(cls.FS)]
        ))

    def search(self, regex: str, fields: set = set()) -> Generator[Dict[str, List[str]], None, None]:
        r = re.compile(regex)
        fields_set = set(JmDB.FIELDS)
        if not fields <= fields_set:
            raise JmDBError('Unknown search field(s) {}. Valid fields are {}.'.format(fields - fields_set, fields_set))
        fields = fields or fields_set
        try:
            with open(self.db_path) as db:
                for line in db.readlines():
                    e = self.parse_entry(line)
                    search_fields = sum([e.get(f) for f in fields], [])
                    for sf in search_fields:
                        if r.search(sf):
                            yield e
                            break
        except FileNotFoundError as ex:
            raise JmDBError('JMDict DB not found at {}. You may need to run prepare() first.'.format(self.db_path))
