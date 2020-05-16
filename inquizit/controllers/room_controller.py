from aiohttp import web

from helpers import room_helper

routes = web.RouteTableDef()


@routes.post('/rooms')
async def create(request):
    response = await room_helper.create_room(request)
    return web.json_response(response)


@routes.post('/rooms/join')
async def join(request):
    response = await room_helper.join_room(request)
    return web.json_response(response)
