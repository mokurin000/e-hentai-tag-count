import gzip
import asyncio
import pickle
from sys import argv
from io import BytesIO
from os import environ
from dataclasses import dataclass

import polars as pl
from dotenv import load_dotenv
from sqlalchemy import String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from manual_fix import TAG_GROUP_MAP

load_dotenv()

DB_USER = environ.get("DB_USER", "root")
DB_PASS = environ.get("DB_PASS", "root")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_NAME = environ.get("DB_NAME", "e-hentai-db")


class Base(DeclarativeBase):
    pass


@dataclass
class GidTid(Base):
    __tablename__ = "gid_tid"

    gid: Mapped[int] = mapped_column(primary_key=True)
    tid: Mapped[int] = mapped_column(primary_key=True)

    def __str__(self):
        return f"GidTid(gid={self.gid}, tid={self.tid})"


@dataclass
class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))

    def __str__(self):
        return f"Tag(id={self.id}, name='{self.name}')"


def save_gz(io: BytesIO, filename: str):
    io.seek(0)

    with gzip.open(filename, mode="wb") as f:
        f.write(io.read())


def process_pair(pair: tuple[str, str]) -> tuple[str, str]:
    tag, group = pair
    return (tag, f"{group}:{tag}")


async def main():
    uri = f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    gid_tid = pl.read_database_uri(
        str(select(GidTid.tid)),
        uri=uri,
        engine="connectorx",
    ).lazy()
    tags = pl.read_database_uri(
        str(select(Tag)),
        uri=uri,
        engine="connectorx",
    ).lazy()

    # slave-master mapping
    with open("smmap_get/smmap.pickle", "rb") as f:
        smmap: dict[str, str] = pickle.load(f)

    if "--first-run" not in argv:
        smmap.update(
            map(
                process_pair,
                TAG_GROUP_MAP.items(),
            )
        )

    result = (
        gid_tid.join(
            tags.rename(
                {
                    "id": "tid",
                    "name": "tag_name",
                }
            ),
            on="tid",
            how="left",
        )
        .drop(pl.col("tid"))
        .with_columns(
            pl.col("tag_name").map_elements(
                lambda tag: smmap[tag] if tag in smmap else tag,
                strategy="threading",
                return_dtype=pl.String,
            )
        )
        .group_by(pl.col("tag_name"))
        .len()
        .collect()
    )

    output = BytesIO()
    result.write_csv(
        file=output,
    )
    save_gz(
        io=output,
        filename="tagname_count.csv.gz",
    )

    output_legacy = BytesIO()
    result_legacy = result.with_columns(pl.lit(None).alias("tid"))
    result_legacy = result_legacy.select(["tid", "len", "tag_name"])
    result_legacy.write_csv(
        file=output_legacy,
        quote_char="'",
        quote_style="non_numeric",
        include_header=False,
    )
    save_gz(
        io=output_legacy,
        filename="tid_count_tag.csv.gz",
    )


if __name__ == "__main__":
    asyncio.run(main())
