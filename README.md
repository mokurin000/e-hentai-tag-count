# e-hentai-tag-count

First you should export your cookies of e-hentai.org (with `Get Cookies.txt LOCALLY`) to `smmap_get/repo.e-hentai.org_cookies.txt`. Netescape format is needed.

Second, you need to fetch tag groups by `smmap_get`, and it might take hours.

Then you could export smmap.pickle, and import the [e-hentai-db sql backup](https://github.com/URenko/e-hentai-db/releases/tag/nightly).

Finally you get to `step2-export_data.py`, and you should use the `step3-manual_fix.py` to re-export the manual fix of missing group prefix, then run step 2 again.

## Data clean

`smmap` introduced slave-master tag fix, by replacing every slave tag to the master tag.

`manual_fix.py` finds the case a tag has only one prefix existing, for example `otaku` and `male:otaku` makes `otaku` a subtag of `male:otaku` if `female:otaku` does not exists.

## Format

- `tagname_count.csv`:
  - not quoted
  - seperator: `,`
  - with header line
- `tid_count_tag.csv`:
  - partially backward compatible
  - `tid` is always empty after `2025-01-08` release.
  - quoted using `'`
  - without header line
