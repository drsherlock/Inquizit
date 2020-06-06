from aiohttp import web

from helpers import room_helper
from middlewares import auth_middleware

routes = web.RouteTableDef()


@routes.post('/rooms')
@auth_middleware
async def create(request):
    response = await room_helper.create_room(request)
    return web.json_response(response)


@routes.post('/rooms/join')
async def join(request):
    response = await room_helper.join_room(request)
    return web.json_response(response)
