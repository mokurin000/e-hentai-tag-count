import asyncio
from pathlib import Path
from http.cookiejar import MozillaCookieJar

from aiohttp import ClientSession, CookieJar

src_dir = Path(__file__).parent.absolute()
cookie_path = src_dir.joinpath("repo.e-hentai.org_cookies.txt")

cookiejar = MozillaCookieJar(filename=cookie_path)
cookiejar.load()

cookies_map = {c.name: c.value for c in cookiejar}


async def main():
    cookies = CookieJar()
    cookies.update_cookies(cookies_map)

    async with ClientSession(
        cookie_jar=cookies,
    ) as session:
        async with session.get(
            "https://repo.e-hentai.org/tools/taggroup?show=2",
        ) as resp:
            print(await resp.text())


if __name__ == "__main__":
    asyncio.run(main())
