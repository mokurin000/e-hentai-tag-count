#!/usr/bin/env bash

cd $(dirname $0)

aria2c -s 4 -j 16 -x 16 \
    --load-cookies=repo.e-hentai.org_cookies.txt \
    --save-session=aria2.session \
    --auto-file-renaming=false \
    --dir=groups -i groups.txt
