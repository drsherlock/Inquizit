
async def find_user(query, db):
    try:
        user = await db.users.find_one(query)
        return user
    except Exception as e:
        print(e)


async def insert_user(query, db):
    try:
        result = await db.users.insert_one(query)
        return result.inserted_id
    except Exception as e:
        print(e)
