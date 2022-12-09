from redbot.core import commands
from .utils import Utils
import random

class GamePool(commands.Cog):
    """Allows users to add games they'd like to play to a channel pool and then chooses a random game to play"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def gamepool(self, ctx):
        """Main command for the GamePool Cog"""
        return

    @gamepool.command()
    async def pick(self, ctx):
        """Pick a game from the channel's Game Pool"""
        messages = await ctx.channel.history(limit=None).flatten()
        game_pool = []
        # Get Bot messages with success tag
        for mess in messages:
            if mess.author.bot:
                if "Added" in mess.content :
                    if mess not in game_pool:
                        game_pool.append(mess)
        # Check if no messages meet conditions
        if not game_pool:
            await ctx.send("No games in the pool! Use the [p]gamepool add <game> syntax to add one")
            return
        # List possible choices in the pool
        await ctx.send("Here's the current pool: ")
        for game in game_pool:
            await ctx.send("    " + game.content.split("\"")[1])
        # Pick random game from the pool and sent result to channel
        random_message = random.choice(game_pool)
        chosen_game = random_message.content.split("\"")[1]
        await ctx.send("I pick \"" + chosen_game + "\", here's the link:")
        # Get the game info from steam
        await Utils.gameInfo(ctx, chosen_game, True)
        # Remove it from the pool
        await Utils.removeGame(ctx, chosen_game, True)
    
    @gamepool.command()
    async def add(self, ctx, *, game):
        """Add a game to the channel's Game Pool"""
        # Check if no game specififed
        if not game:
            await ctx.send("No game specified.")
            return
        # Get the game info from steam
        await Utils.gameInfo(ctx, game, False)
    
    @gamepool.command()
    async def remove(self, ctx, *, game):
        """Remove a game from the channel's Game Pool"""
        # Check if no game specififed
        if not game:
            await ctx.send("No game specified.")
            return
        # Delete game from pool
        await Utils.removeGame(ctx, game, False)
