import asyncio
import pickle

from os import listdir
from pathlib import Path
from asyncio import Semaphore
from functools import reduce
from multiprocessing import Pool
from urllib.parse import urlparse, ParseResult

from aiofile import async_open
from bs4 import BeautifulSoup, Tag

groups_dir = Path(__file__).parent.joinpath("groups").absolute()
dump_output = Path(__file__).parent.joinpath("smmap.pickle").absolute()

READFILE_SEM = Semaphore(1024)


async def read_file(file_path: Path) -> str:
    async with READFILE_SEM:
        async with async_open(file_path, mode="r", encoding="utf-8") as f:
            content = await f.read()
    return content


def tag_real_name(tag: Tag) -> str:
    url: ParseResult = urlparse(tag["href"])
    return url.path.replace("+", " ").split("/")[-1]


def extract_tags(document: str) -> dict[str, str]:
    soup = BeautifulSoup(
        document,
        features="html.parser",
    )

    attrs = soup.select("tr > td:nth-child(1)")
    tags = list(map(tag_real_name, soup.select("tr > td:nth-child(3) > a")))
    for attr, tagname in zip(attrs, tags):
        if attr.text != "M":
            continue
        master = tagname
        tags.remove(master)
    slaves = tags

    return {slave: master for slave in slaves}


async def main():
    tag_groups = [groups_dir.joinpath(f) for f in listdir(groups_dir)]
    tag_group_read = await asyncio.gather(*map(read_file, tag_groups))

    with Pool() as pool:
        maps = pool.map(extract_tags, tag_group_read)

    result = reduce(lambda a, b: a | b, maps)
    with open(dump_output, "wb") as f:
        pickle.dump(result, f)
    print(f"exported {len(result)} relationships")


if __name__ == "__main__":
    asyncio.run(main())
