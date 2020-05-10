import motor.motor_asyncio

from config.development import config


async def init(app):
    url = (
        f"mongodb+srv://"
        f"{config['MONGODB_USERNAME']}:"
        f"{config['MONGODB_PASSWORD']}"
        f"@{config['MONGODB_HOST']}"
    )
    client = motor.motor_asyncio.AsyncIOMotorClient(url)

    app['mongodb'] = client.get_default_database()


async def close(app):
    app['mongodb'].close()
