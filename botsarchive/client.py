from typing import List, Dict, Optional, Union

import httpx

from . import types, enums, exceptions

__all__ = ["API_BASE_URL", "PHOTO_BASE_URL", "Client"]

API_BASE_URL = "https://api.botsarchive.com"
PHOTO_BASE_URL = "https://www.botsarchive.com/img"

class Client:
    def __init__(self: "botsarchive.client.Client", api_base_url: str = API_BASE_URL, photo_base_url: str = PHOTO_BASE_URL, proxies: Union[str, dict, httpx.Proxy] = None, timeout: int = 60) -> None:
        """
        Represents a botsarchive.Client class.
        
        Parameters:
            - api_base_url: base API url of botsarchive.com
            - photo_base_url: base photo url for bot's photo.
            - proxies: proxies for httpx.AsyncClient.
            - timeout: timeout for httpx.AsyncClient.
        
        Example:
            >>> from botsarchive import Client
            >>> client = Client()
        """
        self.api_base_url = api_base_url
        self.photo_base_url = photo_base_url
        self.proxies = proxies
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            proxies=self.proxies,
            timeout=self.timeout
            )
    
    async def get_bot_id(self: "botsarchive.client.Client", username: str) -> types.Bot:
        """
        Get the ID of a bot based on its username.
        
        Parameters:
            - username (str): Username of the bot.
        
        Raises:
            - BotNotFound: When the bot's username is not found.
            - httpx.HTTPError: If an HTTP error occurs during the request.
        
        Returns:
            - types.Bot: An instance of the Bot class representing the bot.
        
        Example:
            >>> client = Client()
            >>> await client.get_bot_id("vote")
            Bot(
                id=1,
                name='Votebot',
                username='@vote',
                description='Votebot creates anonymous and public polls, you can send them everywhere using inline. This is an official Telegram bot.',
                warn=None,
                msg='http://t.me/BotsArchive/79',
                category=['poll'],
                groups=False,
                inline=True,
                developer_id=0,
                stars=770,
                votes=189,
                vote=4.1,
                tags=['vote', 'poll', 'like', 'polls', 'anonymous', 'private', 'public', 'inline', 'official'],
                languages=['English'],
                offline=False,
                photo=True,
                photo_url='https://www.botsarchive.com/img/1.jpg'
            )
        """
        url = f"{self.api_base_url}/getBotID.php"
        params = {
            "username": username
        }
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "message" in data and data["message"] == "bot not found":
            raise exceptions.BotNotFound(data["message"])
        result = types.Bot(
            id=data["result"]["id"],
            name=data["result"]["name"],
            username=data["result"]["username"],
            description=data["result"]["description"],
            warn=data["result"]["warn"],
            msg=data["result"]["msg"],
            category=data["result"]["category"],
            groups=bool(data["result"]["groups"]),
            inline=bool(data["result"]["inline"]),
            developer_id=int(data["result"]["developer_id"]),
            stars=data["result"]["stars"],
            votes=data["result"]["votes"],
            vote=data["result"]["vote"],
            tags=[word.lstrip("#") for word in data["result"]["tags"].split()],
            languages=data["result"]["languages"].split(),
            offline=bool(int(data["result"]["offline"])),
            photo=data["result"]["photo"],
            photo_url=f"{self.photo_base_url}/{data['result']['id']}.jpg" if data["result"]["photo"] else None
            )
        return result
    
    async def get_user_vote(self: "botsarchive.client.Client", bot_id: int, user_id: int) -> Optional[Union[int, bool]]:
        """
        Get the user vote on a bot by bot id and user id.
        
        Parameters:
            - bot_id (int): bot id of the bot.
            - user_id (int): user id of the user.
        
        Raises:
            - BotNotFound: When the bot's username is not found.
            - httpx.HTTPError: If an HTTP error occurs during the request.
        
        Returns:
            - int: An integer of the votes by user.
            - bool: False is returned, if the user was not found or did not voted yet.
        
        Example:
            >>> client = Client()
            >>> await client.get_user_vote(1, 141691961)
            5
        """
        url = f"{self.api_base_url}/getUserVote.php"
        params = {
            "bot_id": bot_id,
            "user_id": user_id
        }
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "message" in data and data["message"] == "bot not found":
            raise exceptions.BotNotFound(data["message"])
        if "result" in data:
            result = int(data["result"])
        elif "vote" in data:
            result = False
        else:
            result = None
        return result
    
    async def search(self: "botsarchive.client.Client", query: str) -> Optional[Union[List[types.Bot]]]:
        """
        Search bots avaiable in database.
        
        Parameters:
            - query (str): name or username of the bot.
        
        Raises:
            - httpx.HTTPError: If an HTTP error occurs during the request.
        
        Returns:
            - list: List of Bot instance based on query matched bots.
            - None: None is returned, if no no bots matched query.
        
        Example:
            >>> client = Client()
            >>> await client.search("vote")
            [Bot(...), Bot(...), Bot(...), ...]
        """
        url = f"{self.api_base_url}/search.php"
        params = {
            "q": query
        }
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if not data["result"]:
            return None
        result = []
        for info in data["result"]:
            bot = types.Bot(
                id=info["id"],
                name=info["name"],
                username=info["username"],
                description=info["description"],
                warn=info["warn"],
                msg=info["msg"],
                category=info["category"],
                groups=bool(info["groups"]),
                inline=bool(info["inline"]),
                developer_id=int(info["developer_id"]),
                stars=info["stars"],
                votes=info["votes"],
                vote=info["vote"],
                tags=[word.lstrip("#") for word in info["tags"].split()],
                languages=info["languages"].split(),
                offline=bool(int(info["offline"])),
                photo=info["photo"],
                photo_url=f"{self.photo_base_url}/{info['id']}.jpg" if info["photo"] else None
                )
            result.append(bot)
        return result
    
    async def category_search(self: "botsarchive.client.Client", category: Union[enums.Category, str]) -> Optional[Union[List[types.Bot]]]:
        """
        Search bots by category.
        
        Parameters:
            - category (enums.Category | str): an enum member from enums.Category or a string.
        
        Raises:
            - httpx.HTTPError: If an HTTP error occurs during the request.
        
        Returns:
            - list: List of Bot instance based on query matched bots.
            - None: None is returned, if no bot was found in the category.
        
        Example:
            >>> from botsarchive import enums
            >>> client = Client()
            >>> await client.category_search(enums.Category.MUSIC)
            [Bot(...), Bot(...), Bot(...), ...]
        """
        url = f"{self.api_base_url}/getCategory.php"
        params = {
            "category": category.value if isinstance(category, enums.Category) else category
        }
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if not data["result"]:
            return None
        result = []
        for info in data["result"]:
            bot = types.Bot(
                id=info["id"],
                name=info["name"],
                username=info["username"],
                description=info["description"],
                warn=info["warn"],
                msg=info["msg"],
                category=info["category"],
                groups=bool(info["groups"]),
                inline=bool(info["inline"]),
                developer_id=int(info["developer_id"]),
                stars=info["stars"],
                votes=info["votes"],
                vote=info["vote"],
                tags=[word.lstrip("#") for word in info["tags"].split()],
                languages=info["languages"].split(),
                offline=bool(int(info["offline"])),
                photo=info["photo"]
                )
            result.append(bot)
        return result

    async def close(self: "botsarchive.client.Client") -> None:
        await self.client.close()