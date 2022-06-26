import discord
from discord import ui, app_commands
import default, log, sys


class client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)
        self.synced = False  # we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # check if slash commands have been synced
            await tree.sync()  # sync commands
            self.synced = True
        print(f"We have logged in as {self.user}.")

    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            if not message.guild:
                print("dm")
                embed = discord.Embed(title=f"Direct Message")
                embed.set_thumbnail(url=message.author.avatar.url)
                embed.add_field(name="Username", value=message.author, inline=False)
                embed.add_field(name="User Id", value=message.author.id, inline=False) 
                embed.add_field(name="Message", value=message.content, inline=False)
                for user_id in settings["dm_endpoint_users"]:
                    user = await self.fetch_user(user_id)
                    await user.send(embed=embed)

    async def on_interaction(self, interaction: discord.Interaction):
        print(f"[guild={interaction.guild_id}][user={interaction.user}][user_id={interaction.user.id}][channel={interaction.channel}][channel_id={interaction.channel.id}]{interaction.command.name}")
        log.Log.log(f"[guild={interaction.guild_id}][user={interaction.user}][user_id={interaction.user.id}][channel={interaction.channel}][channel_id={interaction.channel.id}]{interaction.command.name}")


class CommandTree(app_commands.CommandTree):
    def __init__(self, client):
        super().__init__(client)

    async def on_error(self, interaction, error):
        print(f"[guild={interaction.guild_id}][user={interaction.user}][user_id={interaction.user.id}][channel={interaction.channel}][channel_id={interaction.channel.id}]{interaction.command.name}")
        log.Log.log(f"[guild={interaction.guild_id}][user={interaction.user}][user_id={interaction.user.id}][channel={interaction.channel}][channel_id={interaction.channel.id}]{interaction.command.name}")

        if isinstance(error, discord.app_commands.CommandOnCooldown):
            print("cooldown")
            await interaction.response.send_message(ephemeral=True, embed=default.error_embed("Error", "You are on cooldown!"))


if __name__ == "__main__":
    settings = default.Settings("settings/settings.json")

    # check dirs
    default.create_dir(settings["log-dir"])
    default.create_dir(settings["data-dir"])

    log.Log(settings["log-dir"])

    aclient = client()
    tree = CommandTree(aclient)

    import default_commands, group_commands
    default_commands.load(tree)
    group_commands.load(tree)

    log.Log.log("Loaded Commands")

    aclient.run(default.load_token("settings/token"))

