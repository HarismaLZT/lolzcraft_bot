import disnake
from disnake.ext import commands, tasks
from datetime import datetime
import pytz

class BotProfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_change.start()

    @tasks.loop(hours=1)
    async def status_change(self):
            await self.bot.change_presence(status=disnake.Status.dnd, activity=disnake.Activity(name="mc.lolzcraft.net", type=disnake.ActivityType.playing))

    @status_change.before_loop
    async def before_status_change(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(BotProfile(bot))