import aiohttp
import discord
import random
import os
from datetime import datetime

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

    async def gameInfo(ctx, gamename, pickCommand):
        """Convert game ID to steam link"""
        # Search Steam for game ID
        appid = await Utils.gameToId(gamename)
        # Check if no games matched the search
        if not appid:
            await ctx.send("There was an issue finding your game on Steam. Ensure the name is spelled correctly.")
            return False
        # Message sucessful tag to channel if game was added
        if not pickCommand:
            await ctx.send("Added \"" + gamename + "\" to the pool")
        else:
            # Message link to Steam game to channel if game was picked
            embed = discord.Embed(title="Steam Game Information", url="https://store.steampowered.com/app/" + str(appid),
                                description="Steam Link for " + gamename, color=0x42a6cc)
            embed.add_field(name="Steam Game ID", value=appid, inline=True)
            embed.add_field(name="Steam Game Name", value=gamename, inline=True)
            await ctx.send(embed=embed)
        return True
     
    async def pickNewHost(ctx, game, reroll = False):
        """Edit the host of winning game"""
        # Ensure pool(s) file exists
        file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Winners.txt"
        await Utils.makeFile(file)
        # Get possible choices in the channel
        members = []
        users = ctx.channel.members
        if not reroll:
            for user in users:
                if user.bot != True:
                    members.append(user)
            return random.choice(members)
        else:
            # Check if no game specififed
            if not game:
                await ctx.send("No game specified.")
                return
            filtered_members = []
            # Rewrite pool and change host game
            found_game = False
            with open(file, "r+") as f:
                lines = f.readlines()
            with open(file, "w+") as f:
                for line in lines:
                    if game.lower() in line.lower():
                        new_line = line.split("Hosted by: ")
                        old_host = ctx.guild.get_member_named(new_line[1].strip("\n"))
                        for user in users:
                            if user != old_host and user.bot != True:
                                filtered_members.append(user)
                        new_host = random.choice(filtered_members)
                        f.write(new_line[0] + "Hosted by: " + str(new_host) + "\n")
                        found_game = True
                    else:
                        f.write(line)
                # Check if game wasn't found in pool
                if not found_game:
                    await ctx.send("Game was not found in the pool.")
                    return
                if old_host is not None and new_host is not None:
                    await ctx.send(f"{old_host.mention} couldn't cut it huh?")
                    await ctx.send(f"Let's make your new host {new_host.mention}")
                    return
                else:
                    await ctx.send("Old host couldn't cut it huh?")
                    await ctx.send("Let's make your new host @" + str(new_host))
    
    async def makeFile(file):
        if not os.path.exists(file):
            f = open(file, "w+")
    
    async def removeFromPool(ctx, game, pickCommand = False):
        """Get Game Info from Steam"""
        # Check if no game specififed
        if not game:
            await ctx.send("No game specified.")
            return
        # Ensure pool file exists
        file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + ".txt"
        await Utils.makeFile(file)
        # Rewrite pool excluding specified game
        found_game = False
        with open(file, "r+") as f:
            lines = f.readlines()
        with open(file, "w+") as f:
            for line in lines:
                if line.strip("\n").lower() != game.lower():
                    f.write(line)
                else:
                    found_game = True
        # Check if game wasn't found in pool
        if not found_game:
            await ctx.send("Game was not found in the pool.")
        else:
            if not pickCommand:
                await ctx.send("Removed \"" + game + "\" from the pool")
            else:
                await ctx.send("I've also removed it from the pool so it doesn't get picked again.")
    
    async def addToPool(ctx, game, pickCommand = False, host = ""):
        """Add a verified steam game to the pool"""
        # Check if no game specififed
        if not game:
            await ctx.send("No game specified.")
            return
        # Check if wanted game can be found on steam and write to pool
        if not pickCommand:
            valid = await Utils.gameInfo(ctx, game, False)
            if valid:
                with open("GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + ".txt","a+") as f:
                    f.write(game + "\n")
                # await Utils.readPool(ctx)
        else:
            with open("GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Winners.txt","a+") as f:
                    f.write("\"" + game + "\" on " + datetime.today().strftime('%Y-%m-%d') + " | Hosted by: " + str(host) +"\n")
    
    async def readPool(ctx, pickCommand = False, justList = False):
        """Read all games in the pool"""
        game_pool = []
        # Ensure pool(s) file exists
        file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + ".txt"
        if pickCommand:
            file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Winners.txt"
        await Utils.makeFile(file)
        # Read from pool and deduplicate games
        with open(file,"r+") as f:
            for line in f:
                if line not in game_pool:
                    game_pool.append(line.strip("\n"))
        # Check if there's nothing in the pool
        if not game_pool:
            await ctx.send("No games in the pool!")
            return False
        if not justList:
            # List off the pool and return
            if pickCommand:
                message_string = "Here are the past winners: \n"
            else:
                message_string = "Here's the current pool: \n"
            for game in game_pool:
                message_string += str("\t- " + game + "\n")
            await ctx.send(message_string)
        return game_pool
    
    async def pickFromPool(ctx, pickCommand = True):
        """Pick a random game form the pool"""
        # Get possible choices in the pool
        game_pool = await Utils.readPool(ctx, False, True)
        if game_pool:
            # Pick random game from the pool and send result to channel
            random_game = random.choice(game_pool)
            await ctx.send("I pick \"" + random_game + "\", here's the link:")
            # Get the game info from steam
            await Utils.gameInfo(ctx, random_game, pickCommand)
            # Remove it from the pool
            await Utils.removeFromPool(ctx, random_game, pickCommand)
            # Pick random host
            host = await Utils.pickNewHost(ctx, random_game)
            await ctx.send(f"Oh, and I think {host.mention} should host!")
            # Add it to the winners pool
            await Utils.addToPool(ctx, random_game, pickCommand, host)
   