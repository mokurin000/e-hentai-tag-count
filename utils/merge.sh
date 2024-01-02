#!/usr/bin/env sh

grep : tid_count_tag.csv > _tid_count_tag.csv
mv _tid_count_tag.csv tid_count_tag.csv

join -t , -1 3 -2 1 tid_count_tag.csv tag_name_intro.csv > merged.csv
