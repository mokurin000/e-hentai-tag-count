import asyncio
import hashlib
from os import listdir
from pathlib import Path
from http.cookiejar import MozillaCookieJar

from loguru import logger
from bs4 import BeautifulSoup
from aiohttp import ClientSession, CookieJar

src_dir = Path(__file__).parent.absolute()
cookie_path = src_dir.joinpath("repo.e-hentai.org_cookies.txt")
groups_txt = src_dir.joinpath("groups.txt")
group_dir = src_dir.joinpath("groups")

cookiejar = MozillaCookieJar(filename=cookie_path)
cookiejar.load()

cookies_map = {c.name: c.value for c in cookiejar}


def parse_document(document: str) -> list[str]:
    soup = BeautifulSoup(document, features="html.parser")
    return [tag["href"] for tag in soup.select("td > a")]


async def tag_groups(session: ClientSession) -> list[str]:
    documents = []

    for category in range(2, 11 + 1):
        logger.info(f"scraping category {category}")
        async with session.get(
            f"https://repo.e-hentai.org/tools/taggroup?show={category}",
        ) as resp:
            document = await resp.text()
            documents.append(document)
    results = []
    for tag_group_lst in map(parse_document, documents):
        results.extend(tag_group_lst)
    return results


async def main():
    cookies = CookieJar()
    cookies.update_cookies(cookies_map)

    async with ClientSession(
        cookie_jar=cookies,
    ) as session:
        groups = await tag_groups(session=session)

    current_files = set(listdir(group_dir))
    with open(groups_txt, "w", encoding="utf-8") as f:
        for group_url in groups:
            filename = f"taggroup-{hashlib.md5(group_url.encode('utf-8')).hexdigest()[:8]}.html"
            if filename in current_files:
                continue
            print(
                f"""{group_url}
    out={filename}
    continue=true""",
                file=f,
            )


if __name__ == "__main__":
    asyncio.run(main())
