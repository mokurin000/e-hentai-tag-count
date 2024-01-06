#!/usr/bin/env sh

if [ $# != 1 ]
then
    echo "Usage: $0 [gid-tid.sql]"
    exit 1
fi

replace='s/, 10395)/, 138085)/;'

# generated part start
source ./slave-master-replace.sh
# generated part end

sed -i \
  "$replace" \
  "$1"
