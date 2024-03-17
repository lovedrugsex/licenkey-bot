import discord
from discord.ext import commands
 
def is_owner():
    async def predicate(ctx):
        return ctx.author.id == #your author id
    return commands.check(predicate)

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

        @bot.hybrid_command()
        @is_owner()
        async def sync(ctx): 
            await bot.tree.sync()
            if bot.tree.sync():
                print("synced")
                await ctx.send("synced", ephemeral=True)
            else:
                print("error syncing")
                await ctx.send("synced", ephemeral=True)

        @bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                em = discord.Embed(title=f"sit down",description=f"Try again in {error.retry_after:.2f} seconds.", color=0xEFCF88)
                await ctx.send(embed=em)

