import os
import json
import disnake
from disnake.ext import commands
from colorama import Fore, Style

os.system('color')

with open('settings.json') as f:
    settings = json.load(f)

bot = commands.Bot(command_prefix=(".",), intents=disnake.Intents.all())

for extension in settings["cogs"]:
    try:
        bot.load_extension(extension)
        print(f"{Fore.GREEN}[INFO] Loaded extension: {extension}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Failed to load extension: {extension}. Reason: {e}{Style.RESET_ALL}")

print(f"{Fore.GREEN}[INFO] Bot is now online{Style.RESET_ALL}")
bot.run(settings["token"])