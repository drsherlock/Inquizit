async def find_user_in_room(query, db):
    try:
        user = await db.rooms.find_one(query)
        return user
    except Exception as e:
        print(e)


async def insert_room(query, db):
    try:
        result = await db.rooms.insert_one(query)
        return result.inserted_id
    except Exception as e:
        print(e)


async def find_room(query, db):
    try:
        room = await db.rooms.find_one(query)
        return room
    except Exception as e:
        print(e)


async def add_user(filter, query, db):
    try:
        result = await db.rooms.update_one(filter, query)
        return result.modified_count > 0
    except Exception as e:
        print(e)


async def remove_user(filter, query, db):
    try:
        result = await db.rooms.update_one(filter, query)
        return result.modified_count > 0
    except Exception as e:
        print(e)


async def remove_room(filter, query, db):
    try:
        result = await db.rooms.update_one(filter, query)
        return result.modified_count > 0
    except Exception as e:
        print(e)
