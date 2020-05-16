from aiohttp import web

from helpers import room_helper

routes = web.RouteTableDef()


@routes.post('/rooms')
async def create(request):
    response = await room_helper.create_room(request)
    return web.json_response(response)
