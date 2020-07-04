from aiohttp import web

from helpers import room_helper
from middlewares import auth_middleware

routes = web.RouteTableDef()


@routes.post('/api/rooms')
@auth_middleware
async def create(request):
    response = await room_helper.create_room(request)
    return web.json_response(response)


@routes.post('/api/rooms/addUser')
@auth_middleware
async def join(request):
    response = await room_helper.add_user(request)
    return web.json_response(response)


@routes.post('/api/rooms/removeUser')
@auth_middleware
async def remove(request):
    response = await room_helper.remove_user(request)
    return web.json_response(response)


@routes.get('/api/rooms')
@auth_middleware
async def find(request):
    response = await room_helper.find_room(request)
    return web.json_response(response)
