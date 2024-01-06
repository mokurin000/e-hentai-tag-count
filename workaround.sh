#!/usr/bin/env sh

if [ $# != 1 ]:
then
    echo "Usage: $0 [gid-tid.sql]"
    exit 1
fi

sed -i \
  's/, 10395)/, 138085)/' \
  "$1"
