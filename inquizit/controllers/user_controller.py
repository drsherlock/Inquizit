from aiohttp import web

from helpers import user_helper

routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):
    text = "Hello, World"
    return web.Response(text=text)


@routes.post('/users')
async def create(request):
    user_id = await user_helper.create_user(request)
    return web.json_response({'userId': user_id})
