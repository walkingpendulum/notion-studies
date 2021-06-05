import os
from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp import web

here = Path(__file__).resolve().parent / "templates"


@aiohttp_jinja2.template('hello.html')
async def index_handler(request):
    return {'name': 'Andrew'}


if __name__ == '__main__':
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(here)))
    app.router.add_get('/', index_handler)

    web.run_app(app, port=int(os.getenv("PORT", "8080")))
