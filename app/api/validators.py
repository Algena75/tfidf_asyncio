import os

from sqlalchemy.ext.asyncio import AsyncSession


async def is_text_file(filename: str, session: AsyncSession) -> bool:
    file, ext = os.path.splitext(filename)
    return ext == '.txt'
