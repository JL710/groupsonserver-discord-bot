import discord


def load(tree):
    @tree.command(name="ping", description="Just a Ping!")
    @discord.app_commands.checks.cooldown(60, 60)
    async def ping(interaction: discord.Interaction):
        embed = discord.Embed(title="Ping", description="I am Online!")
        await interaction.response.send_message(embed=embed)
        raise ValueError("Pong")
        