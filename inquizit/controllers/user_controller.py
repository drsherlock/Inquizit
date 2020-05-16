from aiohttp import web

from helpers import user_helper

routes = web.RouteTableDef()


@routes.post('/users')
async def create(request):
    response = await user_helper.create_user(request)
    return web.json_response(response)
