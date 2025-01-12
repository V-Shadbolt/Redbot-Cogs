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
            gameData = next((item for item in response if item["name"].lower().replace(" ", "").replace(":", "").replace("!", "").replace("™", "") == game.lower().replace(" ", "").replace(":", "").replace("!", "").replace("™", "")))
        except StopIteration:
            await session.close()
            return False
        # Return game ID and close http session
        gameid = gameData['appid']
        gamename = gameData['name']
        await session.close()
        return gameid, gamename

    async def gameInfo(game):
        """Convert game ID to steam link"""
        # Search Steam for game ID
        appData = await Utils.gameToId(game)
        # Check if no games matched the search
        if not appData:
            return False
        else:
            appid = appData[0]
            appName = appData[1]
            # Message link to Steam game to channel if game was picked
            embed = discord.Embed(title="Steam Game Information", url="https://store.steampowered.com/app/" + str(appid),
                                    description="Steam Link for " + appName, color=0x42a6cc)
            embed.add_field(name="Steam Game ID", value=appid, inline=True)
            embed.add_field(name="Steam Game Name", value=appName, inline=True)
            return embed, appName

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
    
    async def deleteFile(file):
        """Delete an existing text file"""
        if os.path.exists(file):
            os.remove(file)

    async def tally(opt_dict, tally, message):
        """Tally up reaction counts"""
        for reaction in message.reactions:
            if reaction.emoji in opt_dict.keys():
                reactors = await reaction.users().flatten()
                for reactor in reactors:
                    if reactor.bot != True:
                        tally[reaction.emoji] += 1
        return tally
    
    async def voteTally(opt_dict, tally, message):
        """Tally up reaction counts"""
        for reaction in message.reactions:
            if reaction.emoji in opt_dict.keys():
                tally[reaction.emoji] += 1
        return tally