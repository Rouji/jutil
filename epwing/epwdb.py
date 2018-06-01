import re
import gzip
import json
from typing import List, Dict, Union
from os.path import join, exists, dirname
from os import makedirs, listdir, environ, errno
from shutil import which
from subprocess import Popen, PIPE
from concurrent.futures import ThreadPoolExecutor, wait

_DEFAULT_BASE = join(dirname(__file__))

class EpwDBError(Exception):
    pass

class EpwDB(object):
    DEFAULT_BASE = _DEFAULT_BASE

    def __init__(self, base_dir: str = _DEFAULT_BASE):
        self.base_dir = base_dir or self.DEFAULT_BASE
        self.dirs = {d: join(self.base_dir, d) for d in ['epwing_dicts', 'json']}

    def parse_epwing(self, path: str) -> List[Dict]:
        env = environ.copy()
        env['PATH'] = env.get('PATH', '') + ':' + self.base_dir
        try:
            p = Popen(['zero-epwing', '--entries', path], env=env, stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            ret = p.returncode
            if ret != 0:
                raise EpwDBError('zero-epwing exited with non-zero exit code {}. stderr: {}'.format(ret, err))
        except OSError as ex:
            if ex.errno == errno.ENOENT:
                raise EpwDBError('Could not run zero-epwing. Make sure it is in your PATH.')
            else:
                raise

        required_keys = {'heading', 'text'}
        for b in json.loads(out)['subbooks']:
            for e in b['entries']:
                if set(e.keys()) >= required_keys:
                    yield e

    def prepare(self):
        for d in self.dirs.values():
            if not exists(d):
                makedirs(d)

        def proc(epwdict):
            json_path = join(self.dirs['json'], epwdict)
            if not exists(json_path):
                with gzip.open(json_path, 'wt') as gz:
                    json.dump(list(self.parse_epwing(join(self.dirs['epwing_dicts'], epwdict))), gz)

        with ThreadPoolExecutor(4) as executor:
            futs = [executor.submit(proc,d) for d in listdir(self.dirs['epwing_dicts'])]
            wait(futs)

    def search(self, dict_re: Union[str, None] = None, heading_re: Union[str, None] = None) -> List[dict]:
        dicts = self.dicts()
        if dict_re:
            dict_re = re.compile(dict_re)
            dicts = [d for d in dicts if dict_re.search(d)]
        if not dicts:
            return []
        if heading_re:
            heading_re = re.compile(heading_re)
        for d in dicts:
            with gzip.open(join(self.dirs['json'], d)) as gz:
                for entry in json.load(gz):
                    if heading_re and not heading_re.search(entry['heading']):
                        continue
                    entry['dict'] = d
                    yield entry


    def dicts(self):
        return listdir(self.dirs['json'])
