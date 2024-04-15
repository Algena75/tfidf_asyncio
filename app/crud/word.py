from math import log10

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.models import File, Word, WordFile


class CRUDWord(CRUDBase):

    async def get_or_create(
            self,
            word: str,
            session: AsyncSession,
    ) -> Word:
        word_list = await session.execute(select(Word).where(
            Word.word == word
        ))
        word_obj = word_list.scalars().first()
        if not word_obj:
            word_obj = await self.create(Word(word=word), session)
        return word_obj

    async def set_idf(
            self,
            word,
            session: AsyncSession
    ):
        docs_qty = await session.scalar(func.count(File.id))
        query = select(func.count()).where(WordFile.right_id == word.right_id)
        result = await session.execute(query)
        word_docs_qty = result.scalar()
        idf_value = log10(docs_qty / word_docs_qty)
        word.word.idf = idf_value
        session.add(word)
        await session.commit()


word_crud = CRUDWord(Word)
