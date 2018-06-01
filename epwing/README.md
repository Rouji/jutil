```bash
#./epw.py -h
usage: epw [-h] [-s SEARCH_REGEX] [-d DICT_REGEX] [-b BASE_DIR] [-p PREPARE]
           [-l] [--limit LIMIT] [-f FORMAT] [--debug]
Search EPWING dictionaries.
optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH_REGEX, --search-regex SEARCH_REGEX
                        Regex to use for searching entry headings.
  -d DICT_REGEX, --dict-regex DICT_REGEX
                        Regex to match against dictionary names.
  -b BASE_DIR, --base-dir BASE_DIR
                        Base dir for looking for the epwing_dicts folder and
                        storing prepared dicts in.
  -p PREPARE, --prepare PREPARE
                        Prepare an EPWING dictionary for use.
  -l, --list-dicts      List currently usable dictionaries.
  --limit LIMIT         Limit number of results output.
  -f FORMAT, --format FORMAT
                        Output format for search results. Uses Python's
                        str.format(), passes variables dict,heading,text. Ex.:
                        '[{dict}] {heading}:\n{text}\n'
  --debug               set logging level to DEBUG

# ./download_zero-epwing.sh
# ./epw.py --prepare /path/to/your/epwings/大辞泉
# ./epw.py --list-dicts
大辞泉

# ./epw.py --s '行商' --d '泉$'
[大辞泉] ぎょう‐しょう【行商】ギヤウシヤウ:
ぎょう‐しょう【行商】ギヤウシヤウ
［名］スル店を構えず、商品を持って売り歩くこと。また、その人。「野菜を―する」{{w_46116}}座商。

[大辞泉] ぎょうしょう‐にん【行商人】ギヤウシヤウ‐:
ぎょうしょう‐にん【行商人】ギヤウシヤウ‐
行商してまわる商人。
```
