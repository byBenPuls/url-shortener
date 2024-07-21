import os
import string
import random
import logging
import uvicorn

import database.caching as caching

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from database.caching import redis
from database.postgres import Database

postgres = Database(dsn=os.getenv('DB_CONNECTION_STRING'))

logger = logging.getLogger("uvicorn.access")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Creating connection to databases at startup and their closing at turning off
    :param app:
    """
    await redis.create_connection()
    await postgres.connect()
    yield
    await redis.close_connection()
    await postgres.disconnect()


app = FastAPI(lifespan=lifespan)

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

templates = Jinja2Templates(directory='static')


class Item(BaseModel):
    original_url: str


async def create_endpoint():
    while True:
        endpoint = ''.join(random.choices(string.ascii_letters, k=20))
        pool = await postgres.get_connection()
        async with pool.acquire() as connection:
            response = await connection.fetchrow('SELECT * FROM links WHERE modified = $1', endpoint)
        if response is None:
            return endpoint


@app.get('/')
async def main_page(request: Request):
    return templates.TemplateResponse('hello.html', {'request': request})


@app.post('/')
async def url_handler(item: Item, request: Request):
    endpoint = await create_endpoint()
    pool = await postgres.get_connection()
    async with pool.acquire() as connection:
        search_original_url = await connection.fetchrow('SELECT * FROM links WHERE original = $1',
                                                        item.original_url)
        if search_original_url is not None:
            return {'endpoint': f'http://{request.url.hostname}/{dict(search_original_url)["modified"]}'}
        await connection.execute('INSERT INTO links (original, modified) VALUES ($1, $2)',
                                 item.original_url, endpoint)
    await caching.record_in_cache(endpoint, item.original_url)
    return {
        'endpoint': f'http://{request.url.hostname}/{endpoint}/'
    }


@app.get('/{endpoint}')
async def redirect_url(endpoint: str):
    if await caching.in_cache(endpoint):
        original_url = await caching.get_from_cache(endpoint)
        return RedirectResponse(original_url + '/' if original_url[-1] != '/' else original_url)
    pool = await postgres.get_connection()
    async with pool.acquire() as connection:
        response = await connection.fetchrow('SELECT * FROM links WHERE modified = $1', endpoint)
    original_url = dict(response)['original']
    await caching.record_in_cache(endpoint, original_url)
    return RedirectResponse(original_url + '/' if original_url[-1] != '/' else original_url)


if __name__ == "__main__":
    uvicorn.run('main:app')
