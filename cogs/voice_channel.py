import disnake
from disnake.ext import commands

class VoicePrivate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        category_id = 1075621925302317097 # ID категории для создания нового канала
        target_channel_id = 1079823500912627812 # ID канала, на который реагирует бот
        if before.channel is None and after.channel is not None and after.channel.id == target_channel_id:
            guild = member.guild
            overwrites = {
                guild.default_role: disnake.PermissionOverwrite(connect=False),
                member: disnake.PermissionOverwrite(connect=True, manage_channels=True, manage_roles=True),
            }
            category = self.bot.get_channel(category_id)
            new_channel = await guild.create_voice_channel(f"{member.display_name} room", overwrites=overwrites, category=category)
            await member.move_to(new_channel)

            def check(a, b, c):
                return len(new_channel.members) == 0
            await self.bot.wait_for('voice_state_update', check=check)
            await new_channel.delete()

def setup(bot):
    bot.add_cog(VoicePrivate(bot))