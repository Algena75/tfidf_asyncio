from typing import Optional

from fastapi import APIRouter, Depends, Form, Request, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.validators import is_text_file
from app.core.config import UPLOAD_TO, templates
from app.core.db import get_async_session
from app.crud.file import file_crud
from app.crud.word import word_crud
from app.models.models import File, WordFile

router = APIRouter()


@router.get(
    '/',
    response_class=HTMLResponse,
)
async def get_all_files(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    msg: Optional[str] = None
):
    all_files = await file_crud.get_multi(session)
    context = {'page_obj': all_files, 'is_index': True, 'form': Form()}
    if msg:
        context['messages'] = [msg,]
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
        new_file: File = await file_crud.create(File(name=file.filename),
                                                session)
        words_qty = await file_crud.handle_file(new_file, session)
        new_file.words_qty = words_qty
        session.add(new_file)
        await session.commit()

        return RedirectResponse(
            request.url_for('get_file_details', file_id=new_file.id),
            status_code=302
        )
    elif not file.filename:
        message = 'Выберите файл'
    else:
        message = f"{file.filename} is not text file"
    return RedirectResponse(request.url_for('get_all_files'), status_code=302)


@router.get('/files/{file_id}')
async def get_file_details(
    file_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    file_obj = await session.execute(
        select(File).where(File.id == file_id).options(
            selectinload(File.words).selectinload(WordFile.word)
        )
    )
    file_obj = file_obj.scalars().first()
    words = file_obj.words
    for word in words:
        await word_crud.set_idf(word, session)
    words_sorted = sorted(words, key=lambda word: -word.word.idf)[:50]
    return templates.TemplateResponse(
        request=request, name="index.html",
        context={'page_obj': words_sorted, 'is_index': False, 'form': Form()}
    )


async def not_found_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse('404.html', {'request': request},
                                      status_code=404)


async def internal_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse('500.html', {'request': request},
                                      status_code=500)


async def csrf_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse('403.html', {'request': request},
                                      status_code=403)


async def not_allowed_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse('405.html', {'request': request},
                                      status_code=405)
