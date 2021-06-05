from aiohttp.web import Application

import handlers


def setup_routes(app: Application) -> None:
    app.router.add_get('/', handlers.index_handler)
    app.router.add_static('/images', path='static/images', name='images')
