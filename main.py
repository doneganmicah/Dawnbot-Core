import toml
from config import Config
from bot import DawnBot


g_CONFIG_FILE = "./config.toml"


# loads the config file into a json object and returns it
# throws FileNotFound error if g_CONFIG_FILE doesn't exist
def load_config():
    with open(g_CONFIG_FILE) as f:
        return Config(toml.loads(f.read()))


if __name__ == "__main__":
    # run the bot
    config = load_config()
    dawn_bot = DawnBot(config)
    dawn_bot.run_bot()
