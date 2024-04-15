from .gamepool import GamePool


async def setup(bot):
    n = GamePool(bot)
    await bot.add_cog(n)