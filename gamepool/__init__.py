from .gamepool import GamePool


def setup(bot):
    n = GamePool(bot)
    bot.add_cog(n)