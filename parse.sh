#!/usr/bin/env sh

if [ $# != 2 ]
then exit 1
fi

output_file=gid_tid.csv

echo processing gid-tid...
zcat "$1" |
  grep -E '^\(.*\)[,;]$' |
  tr -cd '[0-9] \n' |
  grep -v '^$' |
  awk -F" " '{ print $2 }' |
  sort -n -r |
  uniq -c |
  sed 's/^\s*//g;s/ /,/' |
  awk -F, '{ print $2 "," $1 }' |
  sort -n > tid_count.csv

echo processing tag...
zcat "$2" |
  grep -E '^\(.*\)[,;]$' |
  tr -d "();" |
  sed 's![,;]$!!;s!, !,!' |
  sort -n > tid_tag.csv

echo compressing tid-count in background...
gzip tid_count.csv &
echo compressing tid-tag in background...
gzip tid_tag.csv &

echo merging tid-count-tag...
join -t , tid_count.csv tid_tag.csv > tid_count_tag.csv

echo compressing tid-count in background...
gzip tid_count_tag.csv &
