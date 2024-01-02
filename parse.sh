if ! [[ -z $1 ]]
then exit 1
fi

gzip -d -c "$1" |
  rg '^\(.*\)[,;]$' |
  tr -cd '[0-9] \n' |
  grep -v '^$' |
  awk -F" " '{ print $2 }' |
  sort -n -r |
  uniq -c |
  sed 's/^\s*//g;s/ /,/' |
  sort -n -r > ${1%.sql.gz}.csv
