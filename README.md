# e-hentai-tag-count

Because `ccloli` lost data for months, he hasn't dump his database for years.

This branch still inherites from e-hentai-db database architecture, but have even better performance, and much easier to reproduce.

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
