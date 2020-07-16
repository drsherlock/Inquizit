from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/api/check')
async def create(request):
    return web.Response(text="OK")
