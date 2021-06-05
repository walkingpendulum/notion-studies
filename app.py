import os
from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp import web

here = Path(__file__).resolve().parent / "static"


@aiohttp_jinja2.template('hello.html')
async def index_handler(request):
    return {'name': 'Andrew'}


if __name__ == '__main__':
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(here)))

    app.router.add_get('/', index_handler)
    app.router.add_static('/images', path='static/images', name='images')

    web.run_app(app, port=int(os.getenv("PORT", "8080")))
