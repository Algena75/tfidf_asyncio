import string
from random import choices
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import ARRAY, UPLOAD_TO
from app.crud.base import CRUDBase
from app.crud.word import word_crud
from app.models.models import File, WordFile


class CRUDFile(CRUDBase):

    async def get_file_name(
            self,
            file_name: str,
            session: AsyncSession,
    ) -> Optional[str]:
        db_file = await session.execute(select(File).where(
            File.name == file_name
        ))
        if db_file.scalars().first():
            name_suffix: str = ''.join(choices(ARRAY, k=8))
            new_name: str = f'{file_name[:-4]}_{name_suffix}.txt'
            file_name = await self.get_file_name(new_name, session)
        return file_name

    async def handle_file(
            self,
            file_obj: File,
            session: AsyncSession,
    ) -> int:
        with open(f'{UPLOAD_TO}{file_obj.name}', 'r') as myfile:
            rows = myfile.readlines()
            clear_rows = [row.strip().translate(str.maketrans(
                '', '', (string.punctuation + '—')
            )) for row in rows]
            freq = dict()
            word_counter = 0
            for row in clear_rows:
                for word in row.split():
                    word_counter += 1
                    word = word.lower()
                    if word in freq:
                        freq[word] += 1
                    else:
                        freq[word] = 1
            word_file_list = []
            for req in freq:
                word = await word_crud.get_or_create(word=req,
                                                     session=session)
                word_file = WordFile(left_id=file_obj.id, right_id=word.id,
                                     tf=float(freq.get(req) / word_counter))
                word_file_list.append(word_file)
            session.add_all(word_file_list)
            await session.commit()

            return word_counter


file_crud = CRUDFile(File)
