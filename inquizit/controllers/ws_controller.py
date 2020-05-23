from aiohttp import web, WSMsgType
from bson.objectid import ObjectId

from models import Game

routes = web.RouteTableDef()


@routes.get('/ws/{game_id}/{player_id}')
async def create(request):
    game_id = request.match_info['game_id']
    player_id = request.match_info['player_id']

    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    if not ws_ready.ok:
        msg = "Sorry, something went wrong!"
        return web.json_response({'error': msg})

    await ws_current.prepare(request)

    query = {'_id': ObjectId(game_id), 'active': True}
    game = await Game.find_game(query=query, db=request.app['mongodb'])

    if game is None:
        msg = "Game over, start a new game"
        await ws_current.send_json({'action': 'error', 'name': player_id, 'msg': game_id})
        await ws_current.close()
        return

    if not any(player_id == str(player['_id']) for player in game['players']):
        msg = "You have not joined the game"
        await ws_current.send_json({'action': 'error', 'name': player_id, 'msg': msg})
        await ws_current.close()
        return

    await ws_current.send_json({'action': 'connect', 'name': player_id})

    for player in game['players']:
        if str(player['_id']) in request.app['websockets']:
            player_ws = request.app['websockets'][str(player['_id'])]
            await player_ws.send_json({'action': 'join', 'name': player_id})

    request.app['websockets'][player_id] = ws_current

    async for msg in ws_current:
        if msg.type == WSMsgType.text:
            if msg.data == 'close':
                await ws_current.close()
            else:
                for player in game['players']:
                    if str(player['_id']) in request.app['websockets']:
                        player_ws = request.app['websockets'][str(
                            player['_id'])]
                        if player_ws is not ws_current:
                            await player_ws.send_json(
                                {'action': 'sent', 'name': player_id, 'text': msg.data})
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws_current.exception())
        else:
            break

    if player_id in request.app['websockets']:
        del request.app['websockets'][player_id]

    for player in game['players']:
        if str(player['_id']) in request.app['websockets']:
            player_ws = request.app['websockets'][str(player['_id'])]
            await player_ws.send_json({'action': 'disconnect', 'name': player_id})

    return ws_current
