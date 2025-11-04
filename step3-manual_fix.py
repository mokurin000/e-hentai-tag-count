from sys import stderr
import polars as pl


def main():
    tags: set[str] = set(pl.read_csv("tagname_count.csv")["tag_name"])
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

    print("TAG_GROUP_MAP = {")
    for orphan, groups in sorted(result.items()):
        match len(groups):
            case 1:
                print(f"    {orphan.__repr__()}: {groups[0].__repr__()},")
            case 0:
                # real orphan, don't touch
                pass
            case _:
                print(f"[ignored] multi group: {orphan} -> {groups}", file=stderr)

    print("}")


if __name__ == "__main__":
    main()
