#!/usr/bin/env python3
# coding = utf-8

from jmdb import JmDB
from random import shuffle

if __name__ == '__main__':
    entries = list(JmDB().search('.', fields={'kanji'}))
    shuffle(entries)
    while True:
        prompt = entries.pop()
        answer_str = '{} ({}): {}'.format(','.join(prompt['kanji']), ','.join(prompt['reading']), ','.join(prompt['meaning']))
        while True:
            answer = input('\033[34m{}\033[0m: '.format(prompt['kanji'][0]))
            if answer in prompt['reading']:
                print('\033[32m正解！\033[0m ' + answer_str)
                break
            elif not answer.strip():
                print('\033[31m正解は:\033[0m ' + answer_str)
                break
            else:
                print('\033[31mブブー\033[0m')
