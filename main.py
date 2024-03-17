from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == #your discord user id
    return commands.check(predicate)

@bot.event
async def on_ready():
    await setup(bot)

async def setup(bot: commands.Bot):
    for root, dirs, files in os.walk("./cogs"):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":  # Exclude __init__.py
                cog_path = os.path.join(root, file)
                module_name = os.path.splitext(cog_path.replace(os.sep, '.'))[0]
                try:
                    bot.load_extension(module_name)
                    print(f"Cog Loaded: {module_name}")
                except Exception as e:
                    print(f"Failed to load cog {module_name}: {e}")

    # Automatically add cogs to the bot
    for root, _, files in os.walk("./cogs"):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":  
                folder_name = os.path.basename(os.path.dirname(os.path.join(root, file)))
                cog_module = os.path.splitext(file)[0]
                cog_class_name = folder_name.capitalize()  # Capitalizing folder name for class name
                cog = getattr(__import__(f"cogs.{folder_name}.{cog_module}", fromlist=[""]), cog_class_name)
                await bot.add_cog(cog(bot))

bot.run(DISCORD_TOKEN)
