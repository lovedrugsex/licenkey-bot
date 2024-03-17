import discord
import os
import uuid
from discord.ext import commands

def load_keys():
    keys = {}
    if os.path.exists("keys.txt"):
        with open("keys.txt", "r") as f:
            for line in f:
                parts = line.strip().split(" - ")
                if len(parts) >= 5:  # Check if there are at least 5 elements
                    key = parts[0]
                    user_id = int(parts[1])
                    link = parts[2]
                    limit = int(parts[3])
                    role_id = int(parts[4]) if parts[4] != "None" else None
                    keys[key] = {'user_id': user_id, 'link': link, 'limit': limit, 'role_id': role_id}
    return keys


def save_keys(keys):
    with open("keys.txt", "w") as f:
        for key, data in keys.items():
            f.write(f"{key} - {data['user_id']} - {data['link']} - {data['limit']} - {data['role_id']}\n")


class Keys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot        
         
        @bot.hybrid_command()
        @commands.cooldown(1, 3, commands.BucketType.user)
        async def redeem(ctx, key):
            keys = load_keys()
            if key in keys:
                if keys[key]['limit'] == -1 or keys[key]['limit'] > 0:
                    if keys[key]['limit'] != -1:
                        keys[key]['limit'] -= 1
                    save_keys(keys)
                    link = keys[key]['link']
                    role_id = keys[key]['role_id']
                    em = discord.Embed(title="Key Redeemed", color=0xed6035)
                    em.add_field(name="String", value=link)
                    if role_id:
                        role = ctx.guild.get_role(role_id)
                        if role:
                            await ctx.author.add_roles(role)
                            em.add_field(name="Role Added", value=role.name)
                    await ctx.send(embed=em, ephemeral=True)
                else:
                    embed = discord.Embed(title="Error", description="Inputted key is invalid!", color=0xFF0000)
                    await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="Error", description="Inputted key is invalid!", color=0xFF0000)
                await ctx.send(embed=embed, ephemeral=True)


        @bot.hybrid_command()
        @commands.cooldown(1, 3, commands.BucketType.user)
        async def gen(ctx, amount: int, link: str, role: discord.Role = None, usage_limit: int = -1):
            key_amt = range(amount)
            keys = load_keys()
            generated_keys = []
            for _ in key_amt:
                key = str(uuid.uuid4())
                keys[key] = {'user_id': ctx.author.id, 'link': link, 'limit': -1 if usage_limit == -1 else usage_limit, 'role_id': role.id if role else None}
                generated_keys.append(key)
            save_keys(keys)
            embed = discord.Embed(title="Success", description=f"{amount} key(s) generated successfully.", color=0x0BDA51)
            embed.add_field(name="Key(s)", value="\n".join(generated_keys), inline=False)
            embed.add_field(name="Link", value=link, inline=False)
            embed.add_field(name="Usage Limit", value=usage_limit if usage_limit != -1 else "Infinite", inline=False)
            if role:
                embed.add_field(name="Role ID", value=f"<@&{role.id}>", inline=False)
            await ctx.send(embed=embed, ephemeral=True)

        @bot.hybrid_command()
        @commands.cooldown(1, 3, commands.BucketType.user)
        async def update(ctx, key: str, link: str = None, role: discord.Role = None, usage_limit: int = None):
            if usage_limit is not None and usage_limit < -1:
                await ctx.send("Usage limit cannot be less than -1.", ephemeral=True)
                return

            keys = load_keys()
            if key in keys:
                if keys[key]['user_id'] == ctx.author.id:
                    if link:
                        keys[key]['link'] = link
                    if role:
                        keys[key]['role_id'] = role.id
                    if usage_limit is not None:
                        keys[key]['limit'] = -1 if usage_limit == -1 else usage_limit
                    save_keys(keys)
                    embed = discord.Embed(title="Success", description="Key updated successfully", color=0x0BDA51)
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title="Error", description="You are not the owner of this key.", color=0xFF0000)
                    await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="Error", description="Inputted key is invalid!", color=0xFF0000)
                await ctx.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Keys(bot))
