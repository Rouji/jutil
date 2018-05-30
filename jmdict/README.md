```bash
# ./jm.py -h
usage: jm.py [-h] [-f FIELDS] [-p] [-j JMDICT_URL] [-d DB_PATH]
             [--format FORMAT] [-l LIMIT] [-s SEPARATOR] [--debug]
             regex

Searches (English) JMDict.

positional arguments:
  regex                 Python regex to use for searching. Matches substrings,
                        use ^ and $ if you need whole matches.

optional arguments:
  -h, --help            show this help message and exit
  -f FIELDS, --fields FIELDS
                        Comma-separated list of fields to search. Valid fields
                        are: kanji, reading, meaning, pos, misc
  -p, --prepare         Download JMDict and prepare it for searching before
                        doing anything else. Must be done once before searches
                        are possible.
  -j JMDICT_URL, --jmdict-url JMDICT_URL
                        Alternate URL to download JMDict from.
  -d DB_PATH, --db-path DB_PATH
                        Alternate path for the prepared JMDict DB.
  --format FORMAT       Format string to use for search results. Uses Python's
                        str.format(), passes all search_fields. Ex.: '{kanji}
                        [{reading}] ({pos}) {{{misc}}}: {meaning}'
  -l LIMIT, --limit LIMIT
                        Limit number of results shown.
  -s SEPARATOR, --separator SEPARATOR
                        Separator to use for fields with multiple values.
  --debug               set logging level to DEBUG
```

```bash
# ./jm.py 会長
会長 [かいちょう] (n) {}: president (of a society),chairman
副会長 [ふくかいちょう] (n) {}: vice president (of a club or organization, organisation)
名誉会長 [めいよかいちょう] (n) {}: honorary president
取締役会長 [とりしまりやくかいちょう] (n) {}: chairman of board of directors
政調会長 [せいちょうかいちょう] (n) {}: chairman of (party) policy bureau,policy chief
総務会長 [そうむかいちょう] (n) {}: chairman of executive council (usu. of a party),chairman of the general affairs committee
生徒会長 [せいとかいちょう] (n) {}: head of the student council,president of the student council
```

```bash
# ./jm.py '^..会長$' --format '{kanji}: {reading}' --limit 3./jm.py '^..会長$' --format '{kanji}: {reading}' --limit 3
名誉会長: めいよかいちょう
政調会長: せいちょうかいちょう
総務会長: そうむかいちょう
```

```bash
# ./jm.py おねがい --format '{kanji}' -s '::'
お願いします::御願いします
お願いいたします::お願い致します::御願い致します::御願いいたします
お願いごと::お願い事
お願いを聞く
お願い申し上げる
お願い::御願い
よろしくお願いします::宜しくお願いします
よろしくお願いいたします::宜しくお願い致します
お願いできますか::お願い出来ますか
お願いだから
```
