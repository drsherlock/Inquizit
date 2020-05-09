import motor.motor_asyncio

from config.development import config

async def init(app):
    client = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb+srv://{config['MONGODB_USERNAME']}:{config['MONGODB_PASSWORD']}@cluster0-tmg75.mongodb.net/test?retryWrites=true&w=majority")

    app['mongodb'] = client

async def close(app):
    app['mongodb'].close()
