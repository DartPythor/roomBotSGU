from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vkbottle import API
from vkbottle.bot import BotLabeler


TOKEN = config("TOKEN", cast=str)
LOGER_LEVEL = config("LOGER_LEVEL", cast=str, default="INFO")

engine = create_engine(config("DATABASE_URL", cast=str))
Session = sessionmaker(bind=engine)
session = Session()

bot_instruction = """Не знаю, что сюда написать даже..."""
bot_rules = """https://vk.com/@-222733500-korotko-o-pravilah-prozhivaniya-v-obschezhitii-6"""

api = API(TOKEN)
labeler = BotLabeler()
