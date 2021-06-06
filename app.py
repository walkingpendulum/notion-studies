import logging
import os
from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp.web import Application

import render_state
from middleware import setup_middleware
from render_state import setup_render_state
from routes import setup_routes

here = Path(__file__).resolve().parent / "static"


def setup_logging(app: Application):
    logging.basicConfig()

    logging.getLogger("aiohttp").setLevel(logging.INFO)
    logging.getLogger("app").setLevel(logging.INFO)


def make_app() -> Application:
    app = Application()

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(here)))

    initializers = [
        setup_logging,
        setup_middleware,
        setup_routes,
        setup_render_state,
    ]
    [setup(app) for setup in initializers]

    app.on_startup.append(render_state.on_startup)
    app.on_cleanup.append(render_state.on_cleanup)

    return app


if __name__ == '__main__':
    app = make_app()
    web.run_app(app, port=int(os.getenv("PORT", "8080")))
