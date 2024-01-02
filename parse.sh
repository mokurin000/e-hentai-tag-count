#!/usr/bin/env sh

if [ $# != 2 ]
then exit 1
fi

output_file=gid_tid.csv

gzip -d -c "$1" |
  grep -E '^\(.*\)[,;]$' |
  tr -cd '[0-9] \n' |
  grep -v '^$' |
  awk -F" " '{ print $2 }' |
  sort -n -r |
  uniq -c |
  sed 's/^\s*//g;s/ /,/' |
  sort -n -r |
  awk -F, '{ print $2 "," $1 }' > tid_count.csv

gzip -d -c "$2" |
  grep -E '^\(.*\)[,;]$' |
  tr -d "(); " |
  sed 's![,;]$!!' |
  sort -n > tid_tag.csv

gzip tid_count.csv &
gzip tid_tag.csv &
