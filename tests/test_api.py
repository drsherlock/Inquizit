from inquizit import app


async def test_hello(aiohttp_client, loop):
    app_instance = await app.init_app()
    client = await aiohttp_client(app_instance)
    resp = await client.get('/api/check')
    assert resp.status == 200
    text = await resp.text()
    assert 'OK' in text
