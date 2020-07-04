from aiohttp import web

from helpers import user_helper
from middlewares import auth_middleware
from utils import jwt

routes = web.RouteTableDef()


@routes.post('/api/users')
async def create(request):
    user = await user_helper.create_user(request)
    response = jwt.encode(user)
    return web.json_response(response)


@routes.get('/api/users/verify')
@auth_middleware
async def verify(request):
    response = await user_helper.verify_user(request)
    return web.json_response(response)
