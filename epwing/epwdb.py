import gzip
import json
from typing import List, Dict
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
        self.base_dir = base_dir

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

        for b in json.loads(out)['subbooks']:
            for e in b['entries']:
                yield e

    def prepare(self):
        dirs = {d: join(self.base_dir, d) for d in ['epwing_dicts', 'json']}
        for d in dirs.values():
            if not exists(d):
                makedirs(d)

        def proc(epwdict):
            json_path = join(dirs['json'], epwdict)
            if not exists(json_path):
                with gzip.open(json_path, 'wt') as gz:
                    gz.write(json.dumps(list(self.parse_epwing(join(dirs['epwing_dicts'], epwdict)))))

        with ThreadPoolExecutor(4) as executor:
            futs = [executor.submit(proc,d) for d in listdir(dirs['epwing_dicts'])]
            wait(futs)

    def dicts(self):
        return listdir(join(self.base_dir, 'json'))
