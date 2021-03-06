from bson.objectid import ObjectId

from models import Game, Room


async def create_game(request):
    body = await request.json()

    room_id = body['roomId']

    room_available = await is_room_available(room_id, request)
    if not room_available:
        msg = "Game already running in this room"
        return {'error': msg}

    query = {'_id': ObjectId(room_id), 'active': True}
    room = await Room.find_room(query=query, db=request.app['mongodb'])
    if room is None:
        msg = "Room does not exist"
        return {'error': msg}

    query = {'room_id': ObjectId(
        room_id), 'players': room['users'], 'active': True}
    game_id = await Game.insert_game(query=query, db=request.app['mongodb'])

    return {'gameId': str(game_id)}


async def is_room_available(room_id, request):
    query = {'room_id': ObjectId(room_id), 'active': True}
    game = await Game.find_game(query=query, db=request.app['mongodb'])
    if game is not None:
        return False
    return True
