#!/usr/bin/env sh

if ! [[ -z $1 ]]
then exit 1
fi

output_file=gid_tid.csv

gzip -d -c "$1" |
  rg '^\(.*\)[,;]$' |
  tr -cd '[0-9] \n' |
  grep -v '^$' |
  awk -F" " '{ print $2 }' |
  sort -n -r |
  uniq -c |
  sed 's/^\s*//g;s/ /,/' |
  sort -n -r |
  awk -F, '{ print $2 "," $1 }' > tid_count.csv

gzip tid_count.csv
