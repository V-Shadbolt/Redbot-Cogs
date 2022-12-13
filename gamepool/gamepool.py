from redbot.core import commands
from .utils import Utils

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
        # Get the game info from steam
        await Utils.addToPool(ctx, game)
    
    @gamepool.command()
    async def remove(self, ctx, *, game):
        """Remove a game from the channel's Game Pool"""
        # Delete game from pool
        await Utils.removeFromPool(ctx, game)
    
    @gamepool.command()
    async def list(self, ctx):
        """List the channel's current Game Pool"""
        # Delete game from pool
        await Utils.readPool(ctx)
    
    @gamepool.command()
    async def pick(self, ctx):
        """Pick a game from the channel's Game Pool"""
        # Get the game info from steam
        await Utils.pickFromPool(ctx)
    
    @gamepool.command()
    async def winners(self, ctx):
        """List the channel's previous Game Pool winners"""
        # Delete game from pool
        await Utils.readPool(ctx, True)
    
    @gamepool.command()
    async def host(self, ctx, *, game):
        """Pick a new host for the winning game"""
        # Delete game from pool
        await Utils.pickNewHost(ctx, game, True)
