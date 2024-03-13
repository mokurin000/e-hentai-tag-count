#!/usr/bin/env sh

# remove invalid tags
grep : tid_count_tag.csv > _tid_count_tag.csv
mv _tid_count_tag.csv tid_count_tag.csv

# sort by tag
sort -t , -k 3 -o tid_count_tag.csv tid_count_tag.csv
sort -t , -k 1 -o tag_name_intro.csv tag_name_intro.csv

# merge files
join -t , -1 3 -2 1 tid_count_tag.csv tag_name_intro.csv > merged.csv
