from aiohttp import web

async def handle(request):
	text = "Hello, World"
	return web.Response(text=text)
