#!/usr/bin/env python3
# coding = utf-8
from sys import stdin, stderr, exit
import re
import chardet

def detect_decode(data: bytes) -> str:
    det = chardet.detect(data[:2048])
    det = det.get('encoding', None) or 'shift-jis'
    return data.decode(det, 'ignore')

def strip_aozora(text: str) -> str:
    r = re.compile(r'(.《.*?》)|(［＃.*?］)|(<img.*?>)')
    lines = []
    for line in text.split('\n'):
        line = r.sub('', line).strip()
        if line:
            lines.append(line)
    return '\n'.join(lines)

if __name__ == '__main__':
    if stdin.isatty():
        print('Takes an ebook in aozora .txt format from stdin and spits out lines of text, with image tags, ruby, etc. stripped.', file=stderr)
        exit(1)
    print(strip_aozora(detect_decode(stdin.buffer.read())))
