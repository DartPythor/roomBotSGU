from vkbottle import Bot

from config import api, labeler
from handlers import chat_labeler, admin_labeler

labeler.load(chat_labeler)
labeler.load(admin_labeler)


bot = Bot(
    api=api,
    labeler=labeler,
)

bot.run_forever()
