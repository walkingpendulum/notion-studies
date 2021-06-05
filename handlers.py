import aiohttp_jinja2


@aiohttp_jinja2.template('hello.html')
async def index_handler(request):
    return {'name': 'Andrew'}
