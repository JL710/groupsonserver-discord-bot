import discord


def load(tree):
    @tree.command(name="ping", description="Just a Ping")
    async def ping(interaction: discord.Interaction):
        embed = discord.Embed(title="Ping", description="I am Online!")
        await interaction.response.send_message(embed=embed)
        raise ValueError("Pong")
        