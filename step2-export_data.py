import asyncio
from dataclasses import dataclass
from os import environ


from dotenv import load_dotenv
from sqlalchemy import String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

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


async def main():
    engine = create_async_engine(
        f"mysql+asyncmy://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}",
        echo=True,
    )
    engine.execution_options(stream_results=True)

    async with AsyncSession(engine) as session:
        result = await session.execute(select(GidTid).limit(1000))

        print("query end")

        for item in result.scalars():
            print(item)

        result = await session.execute(select(Tag))
        for item in result.scalars():
            print(item)


if __name__ == "__main__":
    asyncio.run(main())
