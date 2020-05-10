
async def find_user(query, db):
    user = await db.users.find_one(query)
    return user


async def insert_user(query, db):
    result = await db.users.insert_one(query)
    return result.inserted_id
