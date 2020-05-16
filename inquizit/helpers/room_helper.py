from models import Room, User
from bson.objectid import ObjectId


async def create_room(request):
    body = await request.json()

    admin_id = body['adminId']

    query = {"_id": ObjectId(admin_id)}
    user = await User.find_user(
        query=query, db=request.app['mongodb'])
    if user is None:
        msg = "User with id: {} does not exist"
        return {'error': msg.format(admin_id)}

    user_in_room = await has_user(request)
    if user_in_room:
        msg = "User with id: {} is already in another room"
        return {'error': msg.format(admin_id)}

    query = {'admin_id': admin_id, 'user': [user]}
    room_id = await Room.insert_room(query=query,
                                     db=request.app['mongodb'])

    return {'roomId': str(room_id)}


async def has_user(request):
    body = await request.json()

    admin_id = body['adminId']

    query = {"_id": ObjectId(admin_id)}
    user = await Room.find_user_in_room(query=query,
                                        db=request.app['mongodb'])
    if user is None:
        return False
    return True
