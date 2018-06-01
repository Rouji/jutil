```bash
# ./sentences.py -h
usage: sentences.py [-h] [-s SENTENCE] [-t TAG] [-a] [-r] [-d] [-l]
                    [--limit LIMIT] [--db-path DB_PATH] [-u] [-p] [--debug]
Manage/search a DB of example sentences.
optional arguments:
  -h, --help            show this help message and exit
  -s SENTENCE, --sentence SENTENCE
                        Sentence search regex or input sentence for
                        append/replace operations.
  -t TAG, --tag TAG     Tag search regex or tag for append/replace operations.
  -a, --append          Add sentences to a tag. Either use --sentence to
                        specify a single sentence or pipe lines into stdin.
  -r, --replace         Like --append, but clears the tag before inserting.
  -d, --delete          Delete tag.
  -l, --list-tags       List all tags.
  --limit LIMIT         Limit number of search results shown.
  --db-path DB_PATH     Alternate path (directory) for tags storage.
  -u, --unique          Ignore duplicate lines in input.
  -p, --print-tag       Print the tag name in front of every result.'
  --debug               set logging level to DEBUG

# echo "this is\na very useful example" | ./sentences.py --append --tag ex
# ./sentences.py --print-tag
ex: a thing I put in earlier
ex: this is
ex: a very useful example

# ./sentences.py -s '^a\b'
a thing I put in earlier
a very useful example
```

```bash
./scripts/aozora.py < 狼と香辛料.txt | ./sentences.py --replace -tag ranobe.狼と香辛料1
./sentences.py -s わっち --limit 10 -p
anime.gon: うわっち あぁ～。
anime.summer_wars: 昼休みが終わっちまう！
anime.ressha_sentai_tokkyuuger: 関わっちゃいけないんだ。
ranobe.狼と香辛料1: 「わっちは神と呼ばれていたがよ。わっちゃあホロ以外の何者でもない」
ranobe.狼と香辛料1: 「あはははは、わっちが悪魔か」
ranobe.狼と香辛料1: 「そりゃあおかしいさね。わっちゃあそんなこと言われるの初めてじゃ」
ranobe.狼と香辛料1: 「わっち？」
ranobe.狼と香辛料1: 「わっちに剣を向けるとは礼儀知らずじゃな」
ranobe.狼と香辛料1: 「わっちの名前はホロ。しばらくぶりにこの形を取ったがな、うん、なかなか上手くいっとるの」
```
