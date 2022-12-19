from redbot.core import commands
from .utils import Utils
from datetime import datetime
import random

class GamePool(commands.Cog):
    """Allows users to add games they'd like to play to a channel pool and then chooses a random game to play"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def gamepool(self, ctx):
        """Create a pool of games that a channel is interested in playing together and pick a winner from the pool"""
        return
    
    @gamepool.command()
    async def add(self, ctx, *, game):
        """Add a game to the channel's Game Pool"""
        # Check if wanted game can be found on steam and write to pool
        embed = await Utils.gameInfo(game)
        if embed:
            # Report success to channel and add to file
            await ctx.send("Added \"" + game + "\" to the pool")
            with open("GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + ".txt","a+") as f:
                f.write(game + "\n")
        else:
            # Report failure to channel
            await ctx.send("There was an issue finding your game on Steam. Ensure the name is spelled correctly.")
    
    @gamepool.command()
    async def remove(self, ctx, *, game):
        """Remove a game from the channel's Game Pool"""
        # Create pool file if not exists
        file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + ".txt"
        await Utils.makeFile(file)
        # Read pool to memory
        found_game = False
        with open(file, "r+") as f:
            lines = f.readlines()
        # Rewrite pool to file excluding specified game
        with open(file, "w+") as f:
            for line in lines:
                if line.strip("\n").lower() != game.lower():
                    f.write(line)
                else:
                    found_game = True
        # Check if game wasn't found in the pool
        if not found_game:
            await ctx.send("Game was not found in the pool.")
        else:
            await ctx.send("Removed \"" + game + "\" from the pool")
    
    @gamepool.command()
    async def list(self, ctx, list = True):
        """List the channel's current Game Pool"""
        game_pool = []
        # Create pool file if not exists
        file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + ".txt"
        await Utils.makeFile(file)
        # Read pool into memory and deduplicate games
        with open(file,"r+") as f:
            for line in f:
                if line not in game_pool:
                    game_pool.append(line.strip("\n"))
        # Check if there's nothing in memory
        if not game_pool:
            await ctx.send("No games in the pool!")
            return False
        else: 
            if list:
                # Send pool to channel and return list
                message_string = "Here's the current pool: \n"
                for game in game_pool:
                    message_string += str("\t- " + game + "\n")
                await ctx.send(message_string)
            return game_pool
    
    @gamepool.command()
    async def pick(self, ctx):
        """Pick a game from the channel's Game Pool"""
        # Get possible choices in the pool
        game_pool = await self.list(ctx, False)
        if game_pool:
            # Pick random game from the pool
            game = random.choice(game_pool)
            # Pick a random host from the channel
            users = ctx.channel.members
            host = await Utils.pickHost(users)
            # Get the game info from steam
            embed = await Utils.gameInfo(game)
            # Send result to channel
            await ctx.send("I pick \"" + game + f"\" and I think {host.mention} should host! I've also removed it from the pool so it doesn't get picked again. \nHere's the link:", embed=embed)
            # Remove game from the pool by rewriting file excluding chosen game
            file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + ".txt"
            with open(file, "r+") as f:
                lines = f.readlines()
            with open(file, "w+") as f:
                for line in lines:
                    if line.strip("\n").lower() != game.lower():
                        f.write(line)
            # Add game and host to the winners file
            with open("GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Winners.txt","a+") as f:
                f.write("\"" + game + "\" on " + datetime.today().strftime('%Y-%m-%d') + " | Hosted by: " + str(host) +"\n")
    
    @gamepool.command()
    async def winners(self, ctx):
        """List the channel's previous Game Pool winners"""
        winner_pool = []
        # Create pool file if not exists
        file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Winners.txt"
        await Utils.makeFile(file)
        # Read from pool into memory
        with open(file,"r+") as f:
            for line in f:
                winner_pool.append(line.strip("\n"))
        # Check if there's nothing in the pool
        if not winner_pool:
            await ctx.send("No past winners.")
        else:
            # Send pool to channel
            message_string = "Here are the past winners: \n"
            for winner in winner_pool:
                message_string += str("\t- " + winner + "\n")
            await ctx.send(message_string)
    
    @gamepool.command()
    async def host(self, ctx, *, game):
        """Pick a new host for the winning game"""
        filtered_members = []
        # Create pool file if not exists
        file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Winners.txt"
        await Utils.makeFile(file)
        # Get possible users in the channel
        users = ctx.channel.members
        # Read from pool into memory
        with open(file, "r+") as f:
            lines = f.readlines()
        # Rewrite pool and attempt to change game host
        found_game = False
        with open(file, "w+") as f:
            for line in lines:
                if game.lower() in line.lower():
                    found_game = True
                    # Split line to pull the name of the previous host
                    current_line = line.split("Hosted by: ")
                    old_host = ctx.guild.get_member_named(current_line[1].strip("\n"))
                    # Create list of possible hosts excluding bot(s) and previous host
                    for user in users:
                        if user != old_host and user.bot != True:
                            filtered_members.append(user)
                    try:
                        # Pick new host and write back to file
                        new_host = random.choice(filtered_members)
                        f.write(current_line[0] + "Hosted by: " + str(new_host) + "\n")
                    except: 
                        # Use old host and write back to file
                        new_host = ""
                        f.write(current_line[0] + "Hosted by: " + str(old_host) + "\n")
                    
                else:
                    f.write(line)
            # Report to channel
            if not found_game:
                await ctx.send("Game was not found in the pool.")
            elif new_host != "":
                # Found new host
                try:
                    await ctx.send(f"{old_host.mention} couldn't cut it huh? Let's make your new host {new_host.mention}")
                except:
                    await ctx.send(str(old_host) + " couldn't cut it huh? Let's make your new host " + str(new_host))
            else:
                # No other host possible
                try:
                    await ctx.send(f"There's no other hosts to choose from! You're all we got {old_host.mention}")
                except:
                    await ctx.send("There's no other hosts to choose from! You're all we got " + str(old_host))
