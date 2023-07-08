import configparser


config = configparser.ConfigParser()
config.read("yestabak/configs/config.ini")

bot_config = config["BOT_CONFIG"]
BOT_TOKEN = bot_config.get("BOT_TOKEN")
CHAT_ID = -629210889
