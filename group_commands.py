import default, discord
from db import get_db
from default import Settings


def load(tree, guild_id):

    class CreateModal(discord.ui.Modal, title="Create Group"):
        def __init__(self, db_path):
            super().__init__()
            self.__db_path = db_path

        name = discord.ui.TextInput(
            label="Group Name:",
            style=discord.TextStyle.short,
            required=True,
            min_length=3,
            max_length=10,
        )

        async def on_submit(self, interaction: discord.Interaction) -> None:
            db = get_db(self.__db_path)
            if db.execute("SELECT * FROM groups WHERE name=? AND guild_id=?", (str(self.name).lower(), interaction.guild_id)).fetchone() == None and \
                not any([True if x.name.lower() == str(self.name).lower() else False for x in interaction.guild.channels]):
                settings = Settings("settings.json")
                # get category name
                category_name = settings["default-category"] if not interaction.guild_id in settings["custom-categorys"] else settings["custom-categorys"][interaction.guild_id]
                
                # check if category already exists
                if not any([True if x.name == category_name else False for x in interaction.guild.categories]):
                    await interaction.guild.create_category(category_name, position=0)

                # get category
                category = [x for x in interaction.guild.categories if x.name == category_name][0]
                
                # create text channel
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    interaction.user: discord.PermissionOverwrite(view_channel=True)
                }
                channel = await interaction.guild.create_text_channel(str(self.name), category=category, overwrites=overwrites)
                
                # add to database
                db.execute("INSERT INTO groups (name, discord_id, guild_id, owner_id) VALUES (?, ?, ?, ?)", (channel.name.lower(), channel.id, interaction.guild_id, interaction.user.id))
                db.commit()

                # respond to user
                await interaction.response.send_message(ephemeral=True, embed=discord.Embed(title="Succes", description=f"Succesfully created channel: {channel.name}!"))

            else:
                await interaction.response.send_message(embed=default.error_embed("Error", "Already exists!"), ephemeral=True)

            # close db
            db.close()

    @tree.command(guild=discord.Object(id=guild_id), name="group_create", description="Create a group chat on the Server.")
    async def create(interaction: discord.Interaction):
        settings = Settings("settings.json")
        await interaction.response.send_modal(CreateModal(settings["database"]))

    @tree.command(guild=discord.Object(id=guild_id), name="group_invite", description="Invite someone into Group")
    async def invite(interaction: discord.Interaction, user: discord.Member):
        settings = Settings("settings.json")
        db = get_db(settings["database"])
        if db.execute("SELECT * FROM groups WHERE discord_id=? AND guild_id=?", (interaction.channel_id, interaction.guild_id)).fetchone() == None:
            await interaction.response.send_message(ephemeral=True, embed=default.error_embed("Error", "This channel isnt a Group"))
        else:
            if user.id in [x.id for x in interaction.channel.overwrites]:
                await interaction.response.send_message(default.error_embed("Error", "Useris already added"))
            else:
                await interaction.channel.set_permissions(user, view_channel=True)
                await interaction.response.send_message(embed=discord.Embed(title="Succes", description=f"Succesfully added {user}!"))
        db.close()
    
    @tree.command(guild=discord.Object(id=guild_id), name="group_leave", description="Leaves Group")
    async def leave(interaction: discord.Interaction):
        settings = Settings("settings.json")
        db = get_db(settings["database"])
        if db.execute("SELECT * FROM groups WHERE discord_id=? AND guild_id=?", (interaction.channel_id, interaction.guild_id)).fetchone() == None:
            await interaction.response.send_message(ephemeral=True, embed=default.error_embed("Error", "This channel isnt a Group"))
        else:
            users = [x for x in interaction.channel.overwrites if type(x) == discord.member.Member]
            if len(users) == 1:
                # remove from db
                db.execute("DELETE FROM groups WHERE discord_id=? AND guild_id=?", (interaction.channel_id, interaction.guild_id))
                db.commit()

                # delete channel
                await interaction.channel.delete()

            else:
                # remove just the user
                await interaction.channel.set_permissions(interaction.user, overwrite=None)
        db.close()
            
    @tree.command(guild=discord.Object(id=guild_id), name="group_kick", description="Kicks out of a Group")
    async def kick(interaction: discord.Interaction, user: discord.Member):
        settings = Settings("settings.json")
        db = get_db(settings["database"])
        if db.execute("SELECT * FROM groups WHERE discord_id=? AND guild_id=?", (interaction.channel_id, interaction.guild_id)).fetchone() == None:
            await interaction.response.send_message(ephemeral=True, embed=default.error_embed("Error", "This channel isnt a Group"))
        else:
            if db.execute("SELECT * FROM groups WHERE discord_id=? AND guild_id=? AND owner_id=?", (interaction.channel_id, interaction.guild_id, interaction.user.id)).fetchone() == None or \
                interaction.user.guild_permissions.move_members:
                users = [x for x in interaction.channel.overwrites if type(x) == discord.member.Member]
                if len(users) == 1:
                    # remove from db
                    db.execute("DELETE FROM groups WHERE discord_id=? AND guild_id=?", (interaction.channel_id, interaction.guild_id))
                    db.commit()

                    # delete channel
                    await interaction.channel.delete()

                else:
                    # remove just the user
                    await interaction.channel.set_permissions(user, overwrite=None)

        db.close()
