from utils import jwt


def auth_middleware(controller):
    async def middleware(request):
        jwt_token = request.cookies.get('Authorization', None)
        if jwt_token:
            user = jwt.decode(jwt_token)
            request.user_id = user['user_id']
        else:
            request.user_id = ''
        return await controller(request)
    return middleware
