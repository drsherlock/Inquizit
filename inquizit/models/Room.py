async def find_user_in_room(query, db):
    user = await db.rooms.find_one(query)
    return user


async def insert_room(query, db):
    result = await db.rooms.insert_one(query)
    return result.inserted_id


async def find_room(query, db):
    room = await db.rooms.find_one(query)
    return room


async def add_user(filter, query, db):
    result = await db.rooms.update_one(filter, query)
    return result.modified_count > 0
