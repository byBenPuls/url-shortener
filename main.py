from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from pydantic import BaseModel

import os
import string
import random

app = FastAPI()

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

templates = Jinja2Templates(directory='static')


class Item(BaseModel):
    original_url: str


@app.get('/')
async def main_page(request: Request):
    return templates.TemplateResponse('hello.html', {'request': request})


@app.post('/')
async def url_handler(item: Item, request: Request):
    return {
        'endpoint': f'http://{request.url.hostname}/{''.join(random.choices(string.ascii_letters, k=20))}/'
        }


@app.get('/{endpoint}')
async def redirect_url(endpoint: str):
    return RedirectResponse('https://example.com')


if __name__ == "__main__":
    uvicorn.run('main:app')
