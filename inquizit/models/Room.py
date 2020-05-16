async def find_user_in_room(query, db):
    user = await db.rooms.find_one({'user': {'$elemMatch': query}})
    return user


async def insert_room(query, db):
    result = await db.rooms.insert_one(query)
    return result.inserted_id
