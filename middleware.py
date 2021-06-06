import os

from aiohttp.web import Application
from aiohttp_basicauth_middleware import basic_auth_middleware

BASIC_AUTH_URLS = ("/",)
BASIC_AUTH_USER = os.environ["BASIC_AUTH_USER"]
BASIC_AUTH_PASSWORD = os.environ["BASIC_AUTH_PASSWORD"]


def setup_middleware(app: Application) -> None:
    middleware = []

    basic_auth = basic_auth_middleware(BASIC_AUTH_URLS, {BASIC_AUTH_USER: BASIC_AUTH_PASSWORD})
    middleware.append(basic_auth)

    app.middlewares.extend(middleware)
