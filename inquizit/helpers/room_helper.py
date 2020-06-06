from bson.objectid import ObjectId

from models import Room, User


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
        msg = "User with id: {} does not exist"
        return {'error': msg.format(user_id)}

    user_in_room = await check_user_in_room(user_id, request)
    if user_in_room:
        msg = "User with id: {} is already in a room"
        return {'error': msg.format(user_id)}

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
        msg = "Room with id: {} does not exist"
        return {'error': msg.format(room_id)}

    query = {'_id': ObjectId(user_id)}
    user = await User.find_user(
        query=query, db=request.app['mongodb'])
    if user is None:
        msg = "User with id: {} does not exist"
        return {'error': msg.format(user_id)}

    user_in_room = await check_user_in_room(user_id, request)
    if user_in_room:
        msg = "User with id: {} is already in a room"
        return {'error': msg.format(user_id)}

    filter = {'_id': ObjectId(room_id)}
    query = {'$push': {'users': user}}
    updated = await Room.add_user(filter=filter, query=query,
                                  db=request.app['mongodb'])

    return {'updated': updated}


async def check_user_in_room(user_id, request):
    query = {'users': {'$elemMatch': {
        '_id': ObjectId(user_id)}}, 'active': True}
    user = await Room.find_user_in_room(query=query,
                                        db=request.app['mongodb'])
    if user is None:
        return False
    return True
