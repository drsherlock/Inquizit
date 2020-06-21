async def insert_game(query, db):
    result = await db.games.insert_one(query)
    return result.inserted_id


async def find_game(query, db):
    game = await db.games.find_one(query)
    return game


async def remove_player(filter, query, db):
    result = await db.games.update_one(filter, query)
    return result.modified_count > 0


async def remove_game(filter, query, db):
    result = await db.games.update_one(filter, query)
    return result.modified_count > 0
