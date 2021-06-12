import logging

import aiohttp_jinja2
from aiohttp import web

from render_state import get_render_state

logger = logging.getLogger("app")


@aiohttp_jinja2.template('index.html')
async def index_handler(request):
    return {}


async def render_graph(request: web.Request):
    await get_render_state(request.app).request_render()
    raise web.HTTPFound("/")
