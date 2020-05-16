from models import User


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

    return {'userId': str(user_id)}
