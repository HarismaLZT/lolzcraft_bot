import disnake
from disnake.ext import commands

class Form(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1079877314109767700
        self.submission_channel_id = 1079833976883126382
        self.role_id = 1079817894684283001

    @commands.slash_command(
        name="submit",
        description="Отправить заявку",
        guild_ids=[1075621924643819551],  # ID вашего сервера
        options=[
            disnake.Option("text", "Текст заявки", disnake.OptionType.string, required=True),
        ]
    )
    async def submit_command(self, ctx: disnake.ApplicationCommandInteraction, text: str):
        # Создаем новое сообщение в канале с заявками
        submission_message = await self.bot.get_channel(self.submission_channel_id).send(f"Новая заявка от {ctx.author.mention}:\n{text}")
        # Добавляем реакции для администраторов
        await submission_message.add_reaction("✅")  # Возьму
        await submission_message.add_reaction("❌")  # Не возьму

@commands.Cog.listener()
async def on_raw_reaction_add(self, payload: disnake.RawReactionActionEvent):
    if payload.channel_id == self.submission_channel_id and not payload.member.bot:
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = disnake.utils.get(message.reactions, emoji=payload.emoji.name)
        if reaction and reaction.emoji == "✅":  # Если выбрана реакция "Возьму"
            user_id = int(message.content.split()[3][2:-1])  # Извлекаем ID пользователя из сообщения
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(self.role_id)
            user = await self.bot.fetch_user(user_id)  # Получаем пользователя по ID
            await user.add_roles(role)  # Выдаем пользователю роль
            await message.delete()  # Удаляем сообщение с заявкой и реакциями

def setup(bot):
    bot.add_cog(Form(bot))
