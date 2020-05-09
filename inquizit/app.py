from aiohttp import web

from config.development import config
from utils import mongodb
from routes import setup_routes

async def init_app(argv=None):
    app = web.Application()

    app.on_startup.append(mongodb.init)
    app.on_cleanup.append(mongodb.close)

    setup_routes(app)

    return app


def main(argv):
    app = init_app(argv)
    web.run_app(app,
                host=config['SERVER_HOST'],
                port=config['SERVER_PORT'])
