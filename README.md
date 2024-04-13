# Сервис расчёта TF/IDF
Реализация асинхронного сервиса загрузки текстового файла с расчётом индексов TF-IDF (от англ. TF — term frequency, IDF — inverse document frequency)
## Автор:
Алексей Наумов ( algena75@yandex.ru )
## Используемые технолологии:
* FastAPI
* PostgreSQL
* Asyncio
* SQLAlchemy
* Bootstrap

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:


```
git clone git@github.com:Algena75/tfidf_asyncio.git
```

```
cd tfidf_asyncio
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
## Как запустить проект локально:
Выполнить миграции
```
alembic upgrade head
```
запустить проект
```
uvicorn app.main:app --reload
```
открыть в браузере http://127.0.0.1:8000/
## Подготовка:
Загрузить текстовые файлы.  В корне проекта помещены для тестирования файлы `test.txt`, `onemoretest.txt` и `new_doc.txt`.
