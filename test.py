from botsarchive import Client, enums, exceptions
import asyncio

# Initialize a botsarchive Client.
client = Client()

async def main() -> None:
    # Get bot id by bot's username.
    result = await client.get_bot_id("vote")
    print("Bot ID:", result) # Bot(...)
    
    # Get the user vote on the bot.
    result = await client.get_user_vote(1, 141691961)
    print("User vote:", result) # 5
    
    # Search bot in database.
    result = await client.search("vote")
    print("Result:", result) # [Bot(...), Bot(...), Bot(...)]
    
    # Category search.
    result = await client.category_search(enums.Category.MUSIC)
    print("Result:", result) # [Bot(...), Bot(...), Bot(...)]
    
    # Excepting raised exceptions.
    
    # Excepting exceptions.BotNotFound:
    try:
        await client.get_bot_id(0)
    except exceptions.BotNotFound:
        pass

# Run the asynchronous function.
asyncio.run(main())