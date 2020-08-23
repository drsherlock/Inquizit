from aiohttp import web, WSMsgType
from bson.objectid import ObjectId

from helpers import room_helper
from models import Room

routes = web.RouteTableDef()


@routes.get('/ws/{room_id}/{user_id}')
async def create(request):
    room_id = request.match_info['room_id']
    user_id = request.match_info['user_id']

    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    if not ws_ready.ok:
        msg = "Sorry, something went wrong!"
        return web.json_response({'error': msg})

    await ws_current.prepare(request)

    query = {'_id': ObjectId(room_id), 'active': True}
    room = await Room.find_room(query=query, db=request.app['mongodb'])

    # room does not exist
    if room is None:
        msg = "Room is closed, create a new room"
        await ws_current.send_json({'action': 'error', 'userId': user_id, 'msg': room_id})
        await ws_current.close()
        return

    if not any(user_id == str(user['_id']) for user in room['users']):
        msg = "You have not joined the room"
        await ws_current.send_json({'action': 'error', 'userId': user_id, 'msg': msg})
        await ws_current.close()
        return

    users = [{'email': user['email'], 'username': user['username'], 'userId': str(
        user['_id'])} for user in room['users']]
    await ws_current.send_json({'action': 'connect', 'userId': user_id, 'users': users})

    current_user = next({'email': user['email'], 'username': user['username'], 'userId': str(
        user['_id'])} for user in room['users'] if user_id == str(user['_id']))

    # notify current users of new user
    for user in room['users']:
        if str(user['_id']) in request.app['websockets']:
            user_ws = request.app['websockets'][str(user['_id'])]
            await user_ws.send_json({'action': 'join', 'user': current_user})

    request.app['websockets'][user_id] = ws_current

    async for msg in ws_current:
        if msg.type == WSMsgType.text:
            if msg.data == 'close':
                await ws_current.close()
            else:
                for user in room['users']:
                    if str(user['_id']) in request.app['websockets']:
                        user_ws = request.app['websockets'][str(user['_id'])]
                        # forward message to all users except the sender
                        if user_ws is not ws_current:
                            await user_ws.send_json(
                                {'action': 'sent', 'userId': user_id, 'text': msg.data})
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws_current.exception())
        else:
            break

    if user_id in request.app['websockets']:
        del request.app['websockets'][user_id]

        room_filter = {'_id': ObjectId(room_id), 'active': True}
        game_filter = {'room_id': ObjectId(room_id), 'active': True}

        room_helper.remove_user_from_room_and_game(
            room_filter, game_filter, user_id, request)

    for user in room['users']:
        if str(user['_id']) in request.app['websockets']:
            user_ws = request.app['websockets'][str(user['_id'])]
            await user_ws.send_json({'action': 'disconnect', 'userId': user_id})

    return ws_current
