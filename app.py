import os
from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp import web

from middleware import setup_middleware
from routes import setup_routes

here = Path(__file__).resolve().parent / "static"


def make_app() -> web.Application:
    app = web.Application()

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(here)))

    setup_middleware(app)
    setup_routes(app)

    return app


if __name__ == '__main__':
    app = make_app()
    web.run_app(app, port=int(os.getenv("PORT", "8080")))
