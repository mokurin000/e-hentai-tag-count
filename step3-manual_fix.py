from sys import stderr
import polars as pl

import gzip


def main():
    with gzip.open("tagname_count.csv.gz", mode="rb") as csv_file:
        csv = csv_file.read()
    tags: set[str] = set(pl.read_csv(csv, encoding="utf-8")["tag_name"])
    result: dict[str, list[str]] = {}

    for tag in tags:
        if ":" not in tag:
            result[tag] = []

    for tag in tags:
        if ":" not in tag:
            continue

        group, orphan_part = tag.split(":")
        if orphan_part in result:
            result[orphan_part].append(group)

    with open("manual_fix.py", "w", encoding="utf-8") as f:
        print("# Generated for v\n", file=f)
        print("TAG_GROUP_MAP = {", file=f)
        for orphan, groups in sorted(result.items()):
            match len(groups):
                case 1:
                    print(f"    {orphan.__repr__()}: {groups[0].__repr__()},",
                          file=f)
                case 0:
                    # real orphan, don't touch
                    pass
                case _:
                    print(f"[ignored] multi group: {orphan} -> {groups}",
                          file=stderr)

        print("}", file=f)


if __name__ == "__main__":
    main()
