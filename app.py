import os

from aiohttp import web


async def hello(request):
    return web.Response(text="Hello, world")


if __name__ == '__main__':
    app = web.Application()
    app.router.add_get('/', hello)

    web.run_app(app, port=int(os.getenv("PORT", "8080")))
