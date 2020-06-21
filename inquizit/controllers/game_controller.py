from aiohttp import web

from helpers import game_helper

routes = web.RouteTableDef()


@routes.post('/api/games')
async def create(request):
    response = await game_helper.create_game(request)
    return web.json_response(response)
