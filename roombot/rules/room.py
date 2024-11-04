from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule
from vkbottle.dispatch.rules.abc import T_contra

from roombot.validator.digits import is_valid_digit


class ValidateRoomDataRule(ABCRule[Message]):
    async def check(self, message: Message) -> bool:
        message_text = message.text.split()
        if not await is_valid_digit(message_text[1]):
            await message.reply("Ты ввёл не число.")
            return False
        if not (100 <= int(message_text[1]) < 1000):
            await message.reply("Странный номер комнаты.")
            return False
        if 5 > len(message_text[2]):
            await message.reply("Слишком короткое ФИО.")
            return False
        if 20 < len(message_text[2]):
            await message.reply("Слишком большое ФИО.")
            return False
        if 3 > len(message_text[3]):
            await message.reply("Слишком короткий способ связи.")
            return False
        if 20 < len(message_text[3]):
            await message.reply("Слишком большой способ связи.")
            return False
        return True


class ReplyToMessageRule(ABCRule[Message]):
    async def check(self, message: Message) -> bool:
        reply_to_message_id = message.reply_message
        if not reply_to_message_id:
            return False

        reply_text = message.text
        return "!комната" in reply_text
