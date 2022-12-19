import aiohttp
import discord
import random
import os

class Utils:
    async def gameToId(game):
        """Convert a game name to its ID"""
        # Start http session and get Steam game list
        session = aiohttp.ClientSession()
        async with session.get("http://api.steampowered.com/ISteamApps/GetAppList/v2") as r:
            response = await r.json()
        # Get list of apps from Steam game list
        response = response['applist']['apps']
        # Parse list of apps for specified game. If not found return
        try:
            gameid = next((item for item in response if item["name"].lower().replace(" ", "").replace(":", "").replace("!", "") == game.lower().replace(" ", "").replace(":", "").replace("!", "")))
        except StopIteration:
            await session.close()
            return False
        # Return game ID and close http session
        gameid = gameid['appid']
        await session.close()
        return gameid

    async def gameInfo(game):
        """Convert game ID to steam link"""
        # Search Steam for game ID
        appid = await Utils.gameToId(game)
        # Check if no games matched the search
        if not appid:
            return False
        # Message link to Steam game to channel if game was picked
        embed = discord.Embed(title="Steam Game Information", url="https://store.steampowered.com/app/" + str(appid),
                                description="Steam Link for " + game, color=0x42a6cc)
        embed.add_field(name="Steam Game ID", value=appid, inline=True)
        embed.add_field(name="Steam Game Name", value=game, inline=True)
        return embed

    async def pickHost(users):
        """Pick the host of winning game"""
        members = []
        for user in users:
            if user.bot != True:
                members.append(user)
        return random.choice(members)

    async def makeFile(file):
        """Make a new text file"""
        if not os.path.exists(file):
            f = open(file, "w+")
