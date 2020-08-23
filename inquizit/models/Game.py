async def insert_game(query, db):
    try:
        result = await db.games.insert_one(query)
        return result.inserted_id
    except Exception as e:
        print(e)


async def find_game(query, db):
    try:
        game = await db.games.find_one(query)
        return game
    except Exception as e:
        print(e)


async def remove_player(filter, query, db):
    try:
        result = await db.games.update_one(filter, query)
        return result.modified_count > 0
    except Exception as e:
        print(e)


async def remove_game(filter, query, db):
    try:
        result = await db.games.update_one(filter, query)
        return result.modified_count > 0
    except Exception as e:
        print(e)
