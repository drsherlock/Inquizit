from bson.objectid import ObjectId

from models import Room, User, Game


async def create_room(request):
    # body = await request.json()
    user_id = request.user_id
    if user_id == "":
        msg = "Token is invalid"
        return {'error': msg}

    query = {'_id': ObjectId(user_id)}
    user = await User.find_user(
        query=query, db=request.app['mongodb'])
    if user is None:
        msg = "User does not exist"
        return {'error': msg}

    room = await check_user_in_room(user_id, request)
    if room:
        return {'roomId': str(room['_id']), 'inRoom': True}

    query = {'admin_id': ObjectId(user_id), 'users': [user], 'active': True}
    room_id = await Room.insert_room(query=query,
                                     db=request.app['mongodb'])

    return {'roomId': str(room_id)}


async def join_room(request):
    body = await request.json()

    user_id = body['userId']
    room_id = body['roomId']

    query = {'_id': ObjectId(room_id), 'active': True}
    room = await Room.find_room(
        query=query, db=request.app['mongodb'])
    if room is None:
        msg = "Room does not exist"
        return {'error': msg}

    query = {'_id': ObjectId(user_id)}
    user = await User.find_user(query=query, db=request.app['mongodb'])
    if user is None:
        msg = "User does not exist"
        return {'error': msg}

    room = await check_user_in_room(user_id, request)
    if room:
        return {'roomId': str(room['_id']), 'inRoom': True}

    filter = {'_id': ObjectId(room_id)}
    query = {'$push': {'users': user}}
    updated = await Room.add_user(filter=filter, query=query,
                                  db=request.app['mongodb'])

    return {'updated': updated}


async def remove_user(request):
    user_id = request.user_id
    if user_id == "":
        msg = "Token is invalid"
        return {'error': msg}

    body = await request.json()

    room_id = body['roomId']

    query = {'_id': ObjectId(user_id)}
    user = await User.find_user(
        query=query, db=request.app['mongodb'])
    if user is None:
        msg = "User does not exist"
        return {'error': msg}

    query = {'_id': ObjectId(room_id), 'active': True}
    room = await Room.find_room(query=query, db=request.app['mongodb'])
    if room is None:
        msg = "Room does not exist"
        return {'error': msg}

    roomFilter = {'_id': ObjectId(room_id), 'active': True}
    gameFilter = {'room_id': ObjectId(room_id), 'active': True}
    if str(room['admin_id']) == user_id:
        query = {'$set': {'active': False}}
        updated = await Room.remove_room(filter=roomFilter, query=query,
                                         db=request.app['mongodb'])

        updated = await Game.remove_game(filter=gameFilter, query=query,
                                         db=request.app['mongodb'])
    else:
        query = {'$pull': {'users': {'_id': ObjectId(user_id)}}}
        updated = await Room.remove_user(filter=roomFilter, query=query,
                                         db=request.app['mongodb'])

        query = {'$pull': {'players': {'_id': ObjectId(user_id)}}}
        updated = await Game.remove_player(filter=gameFilter, query=query,
                                           db=request.app['mongodb'])

    return {'updated': updated}


async def find_room(request):
    user_id = request.user_id
    if user_id == "":
        msg = "Token is invalid"
        return {'error': msg}

    query = {'_id': ObjectId(user_id)}
    user = await User.find_user(
        query=query, db=request.app['mongodb'])
    if user is None:
        msg = "User does not exist"
        return {'error': msg}

    room = await check_user_in_room(user_id, request)
    if room:
        return {'roomId': str(room['_id']), 'inRoom': True}

    return {'inRoom': False}


async def check_user_in_room(user_id, request):
    query = {'users': {'$elemMatch': {
        '_id': ObjectId(user_id)}}, 'active': True}
    room = await Room.find_user_in_room(query=query,
                                        db=request.app['mongodb'])
    if room is None:
        return False
    return room
