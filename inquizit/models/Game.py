async def insert_game(query, db):
    result = await db.games.insert_one(query)
    return result.inserted_id


async def find_game(query, db):
    game = await db.games.find_one(query)
    return game
