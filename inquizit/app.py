import re

from aiohttp import web
from aiohttp_middlewares import cors_middleware

from config.development import config
from utils import mongodb
from routes import setup_routes


async def init_app(argv=None):
    app = web.Application(middlewares=(
        cors_middleware(origins=["http://localhost:3000"],
                        urls=[re.compile(r"^\/api")],
                        allow_credentials=True,),
    ))

    app['websockets'] = {}

    app.on_startup.append(mongodb.init)
    app.on_shutdown.append(shutdown)
    app.on_cleanup.append(mongodb.close)

    setup_routes(app)

    return app


async def shutdown(app):
    for ws in app['websockets'].values():
        await ws.close()
    app['websockets'].clear()


def main(argv):
    app = init_app(argv)
    web.run_app(app,
                host=config['SERVER_HOST'],
                port=config['SERVER_PORT'])
