import toml


class Config:
    def __init__(self, config_toml):
        self.TOKEN = config_toml['bot']['TOKEN']
        self.koth_channel = config_toml['bot']['koth_channel']
        self.counting_channel = config_toml['bot']['counting_channel']
        self.guild_id = config_toml['bot']['guild_id']
        self.top_level = config_toml['koth']['levels']
