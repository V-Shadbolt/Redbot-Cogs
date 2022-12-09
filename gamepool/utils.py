import aiohttp
import discord

class Utils:
    async def gameToId(gamename):
        """Convert a game name to its ID"""
        # Start http session and get Steam game list
        session = aiohttp.ClientSession()
        async with session.get("http://api.steampowered.com/ISteamApps/GetAppList/v2") as r:
            response = await r.json()
        # Get list of apps from Steam game list
        response = response['applist']['apps']
        # Parse list of apps for specified game. If not found return
        try:
            gameid = next((item for item in response if item["name"].lower() == gamename.lower()))
        except StopIteration:
            await session.close()
            return False
        # Return game ID and close http session
        gameid = gameid['appid']
        await session.close()
        return gameid

    async def gameInfo(ctx, gamename, pick):
        """Convert game ID to steam link"""
        # Search Steam for game ID
        appid = await Utils.gameToId(gamename)
        # Check if no games matched the search
        if not appid:
            await ctx.send("There was an issue finding your game on Steam. Ensure the name is spelled correctly.")
            return
        # Message sucessful tag to channel if game was added
        if not pick:
            await ctx.send("Added \"" + gamename + "\" to the pool")
        else:
            # Message link to Steam game to channel if game was picked
            embed = discord.Embed(title="Steam Game Information", url="https://store.steampowered.com/app/" + str(appid),
                                description="Steam Link for " + gamename, color=0x42a6cc)
            embed.add_field(name="Steam Game ID", value=appid, inline=True)
            embed.add_field(name="Steam Game Name", value=gamename, inline=True)
            await ctx.send(embed=embed)
    
    async def removeGame(ctx, game, pick):
        """Convert message to its ID"""
        messages = await ctx.channel.history(limit=None).flatten()
        id_list = []
        # Get Bot message IDs with success tag for specified game
        for mess in messages:
            if mess.author.bot:
                if "Added" in mess.content :
                    if game in mess.content :
                         if mess.id not in id_list:
                                id_list.append(mess.id)
        # Check if no messages were found for specified game
        if not id_list:
            await ctx.send("Game was not found in the pool.")
        else:
            if not pick:
                await ctx.send("Removed \"" + game + "\" from the pool")
            else:
                await ctx.send("I've also removed it from the pool so it doesn't get picked again.")
        # Delete all message IDs for specified game
        for id in id_list:
            msg = await ctx.channel.fetch_message(id)
            await msg.delete()
