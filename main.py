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
            for guild_id in settings["guilds"]:
                await tree.sync(guild = discord.Object(id=guild_id))  # guild specific: leave blank if global (global registration can take 1-24 hours) -> the id of the server
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
        print("interaction")
        log.Log.log(f"[{interaction.user}][{interaction.user.id}][{interaction.channel}][{interaction.channel.id}]{interaction.message}")


class CommandTree(app_commands.CommandTree):
    def __init__(self, client):
        super().__init__(client)

    async def on_error(self, interaction, error):
        print(error)
        log.Log.log(f"[{interaction.user}][{interaction.user.id}][{interaction.channel}][{interaction.channel.id}]{interaction.message}:{error}")


if __name__ == "__main__":
    settings = default.Settings("settings.json")

    # check dirs
    default.create_dir(settings["log-dir"])
    default.create_dir(settings["data-dir"])

    log.Log(settings["log-dir"])

    aclient = client()
    tree = CommandTree(aclient)

    import default_commands, group_commands
    for guild_id in settings["guilds"]:
        default_commands.load(tree, guild_id)
        group_commands.load(tree, guild_id)

    log.Log.log("Loaded Commands")

    aclient.run(default.load_token("token"))

