import discord


def load(tree, guild_id):
    @tree.command(guild = discord.Object(id=guild_id), name="ping", description="Just a Ping")
    async def ping(interaction: discord.Interaction):
        print(interaction.guild.members)
        embed = discord.Embed(title="Ping", description="I am Online!")
        await interaction.response.send_message(embed=embed)
        