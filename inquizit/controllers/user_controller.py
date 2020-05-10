from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):
    text = "Hello, World"
    return web.Response(text=text)


@routes.post('/users')
async def create(request):
    body = await request.json()

    username = body['username']
    email = body['email']
    return web.Response(text=username+""+email)
