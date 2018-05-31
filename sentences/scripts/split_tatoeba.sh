#!/bin/bash
IFS=$'\t'
wget -O- http://downloads.tatoeba.org/exports/sentences.tar.bz2 | tar xjOf - | \
while read id language sentence; do
    echo "$sentence" >> $language.txt
done
