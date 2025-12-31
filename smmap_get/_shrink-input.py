from pathlib import Path

src_dir = Path(__file__).parent.absolute()
groups_txt = src_dir.joinpath("groups.txt")
groups_dir = src_dir.joinpath("groups")

with open(groups_txt, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")
    lines = [line for line in lines if line]

download_files: list[tuple[str, list[str]]] = []

prev_line: list[str] = None
for line in lines:
    if line.startswith("    ") and prev_line is not None:
        prev_line.append(line)
    else:
        prev_line = []
        download_files.append((line, prev_line))

filtered: list[tuple[str, list[str]]] = []
for line, attrs in download_files:
    retain = True

    for attr in attrs:
        if "out=" not in attr:
            continue
        filename = attr.split("out=")[1]
        if (groups_dir / filename).exists():
            retain = False

    if retain:
        filtered.append((line, attrs))


with open(groups_txt, "w", encoding="utf-8") as f:
    for url, attrs in filtered:
        print(url, file=f)
        for attr in attrs:
            print(attr, file=f)
