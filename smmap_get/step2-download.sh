#!/usr/bin/env bash

cd $(dirname $0)

aria2c -s 1 -j 3 \
    --load-cookies=repo.e-hentai.org_cookies.txt \
    --save-session=aria2.session \
    --auto-file-renaming=false \
    --dir=groups -i groups.txt
