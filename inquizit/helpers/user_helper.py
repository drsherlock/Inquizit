from bson.objectid import ObjectId

from models import User, Room


async def find_user(request):
    body = await request.json()

    email = body['email']

    query = {'email': email}
    user = await User.find_user(
        query=query, db=request.app['mongodb'])

    return user


async def create_user(request):
    body = await request.json()

    email = body['email']
    username = body['username']

    user = await find_user(request)
    if user is None:
        query = {'email': email, 'username': username}
        user_id = await User.insert_user(query=query,
                                         db=request.app['mongodb'])
    else:
        user_id = user['_id']

    return {'user_id': str(user_id)}


async def verify_user(request):
    user_id = request.user_id
    if user_id == "":
        msg = "Token is invalid"
        return {'error': msg}

    room_id = request.match_info['room_id']

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

    room = await check_user_in_room(user_id, request)
    if room_id != str(room['_id']):
        return {'roomId': str(room['_id']), 'inRoom': True}

    return {'userId': str(user['_id']), 'username': user['username']}


async def check_user_in_room(user_id, request):
    query = {'users': {'$elemMatch': {
        '_id': ObjectId(user_id)}}, 'active': True}
    room = await Room.find_user_in_room(query=query,
                                        db=request.app['mongodb'])
    if room is None:
        return False
    return room
