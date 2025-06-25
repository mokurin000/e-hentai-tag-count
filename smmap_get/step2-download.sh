#!/usr/bin/env bash

rm -rf ./groups

aria2c -s 4 -j 16 -x 16 \
    --load-cookies=repo.e-hentai.org_cookies.txt \
    --continue \
    --dir=groups -i groups.txt
