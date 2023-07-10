import discord
from config import Config
from discord import app_commands
from discord.ext import commands
from koth import Koth
from counting import Counting


class DawnBot(discord.Client):
    def __init__(self, config: Config):
        super().__init__(intents=discord.Intents.all())
        self.config = config
        self.counting = Counting(self.config)
        self.koth = Koth(self.config)
        self.tree = app_commands.CommandTree(self)
        self.synced = False
        self.register_events()
        self.register_commands()

    def run_bot(self):
        super().run(self.config.TOKEN)

    def register_events(self):
        @self.event
        async def on_ready():
            await self.wait_until_ready()
            if not self.synced:
                syncing = await self.tree.sync(guild=discord.Object(id=self.config.guild_id))
                self.synced = True
                print(f"Synced {len(syncing)}: commands")

            print("Bot is running")

        @self.event
        async def on_message(message):
            response = None
            if message.channel.id == self.config.koth_channel:
                response = self.koth.get_response_to_message(message)
            elif message.channel.id == self.config.counting_channel:
                response = self.counting.count_received(message)
            if response is not None:
                if isinstance(response, discord.Embed):
                    await message.channel.send(embed=response)
                else:
                    await message.channel.send(response)

    def register_commands(self):
        @self.tree.command(name="rules", description="Show the rules for the counting game.", guild=discord.Object(id=self.config.guild_id))
        async def rules(interaction: discord.Interaction):
            if interaction.channel_id != self.config.counting_channel:
                await interaction.response.send_message(
                    f"This command can only be used in {interaction.guild.get_channel(self.config.counting_channel).mention} !",
                    ephemeral=True)
            else:
                await interaction.response.send_message(self.counting.rules(), ephemeral=True)

        @self.tree.command(name="count", description="Start the counting game.", guild=discord.Object(id=self.config.guild_id))
        async def count(interaction: discord.Interaction, number: int = 0):
            if interaction.channel_id != self.config.counting_channel:
                await interaction.response.send_message(f"This command can only be used in {interaction.guild.get_channel(self.config.counting_channel).mention} !", ephemeral=True)
            else:
                await interaction.response.send_message(self.counting.count(number, interaction.user))

        @self.tree.command(name="record", description="Returns the current record.", guild=discord.Object(id=self.config.guild_id))
        async def record(interaction: discord.Interaction):
            if interaction.channel_id != self.config.counting_channel:
                await interaction.response.send_message(
                    f"This command can only be used in {interaction.guild.get_channel(self.config.counting_channel).mention} !",
                    ephemeral=True)
            else:
                await interaction.response.send_message(self.counting.records(), ephemeral=True)

