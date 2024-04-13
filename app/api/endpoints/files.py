from fastapi import APIRouter, Depends
from fastapi import File as F
from fastapi import Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from typing import Mapping

from app.api.validators import is_text_file
from app.core.config import templates, UPLOAD_TO
from app.core.db import get_async_session
from app.crud.file import file_crud
from app.crud.word import word_crud
from app.schemas.files import FileCreate
from app.models.models import File, Word, WordFile

router = APIRouter()


@router.get(
    '/',
    response_class=HTMLResponse,
)
async def get_all_files(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    headers: Mapping[str, str] = None
):
    all_files = await file_crud.get_multi(session)
    context={'page_obj': all_files, 'is_index': True, 'form': Form()}
    if headers:
        context['flash'] = headers.get('flash')
    return templates.TemplateResponse(
        request=request, name="index.html", context=context
    )

@router.post('/add_file')
async def upload_file(
    request: Request,
    file: UploadFile,
    session: AsyncSession = Depends(get_async_session)
):
    if await is_text_file(file.filename, session):
        file.filename = await file_crud.get_file_name(file.filename, session)
        contents = await file.read()
        with open(f'{UPLOAD_TO}{file.filename}', 'wb') as f:
            f.write(contents)
        new_file: File = await file_crud.create(File(name=file.filename), session)
        words_qty = await file_crud.handle_file(new_file, session)
        new_file.words_qty = words_qty
        session.add(new_file)
        await session.commit()

        return RedirectResponse(request.url_for('get_file_details', file_id=new_file.id), status_code=302)
    elif not file:
        flash_message = 'Выберите файл'
    else:
        flash_message = f"{file.filename} is not text file"
    return RedirectResponse(request.url_for('get_all_files'), status_code=302)
    
@router.get('/files/{file_id}')
async def get_file_details(
    file_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    file_obj = await session.execute(
        select(File).where(File.id == file_id).options(selectinload(File.words).selectinload(WordFile.word))
    )
    file_obj = file_obj.scalars().first()
    words = file_obj.words
    for word in words:
        await word_crud.set_idf(word, session)
    words_sorted = sorted(words, key=lambda word: -word.word.idf)[:50]
    return templates.TemplateResponse(
        request=request, name="index.html", context={'page_obj': words_sorted, 'is_index': False, 'form': Form()}
    )
