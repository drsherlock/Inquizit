from aiohttp import web

from helpers import user_helper
from utils import jwt

routes = web.RouteTableDef()


@routes.post('/users')
async def create(request):
    user = await user_helper.create_user(request)
    response = jwt.encode(user)
    return web.json_response(response)
