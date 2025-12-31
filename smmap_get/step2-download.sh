#!/usr/bin/env bash

cd $(dirname $0)

grep -lR "This IP address has been temporarily banned due to an excessive request rate" \
    ./groups |
    xargs rm 2> /dev/null
find ./groups -maxdepth 1 -type f \
    -size 0 -delete

python3 _shrink-input.py

aria2c -s 1 -j 3 \
    --load-cookies=repo.e-hentai.org_cookies.txt \
    --save-session=aria2.session \
    --auto-file-renaming=false \
    --allow-overwrite=false \
    --dir=groups -i groups.txt
