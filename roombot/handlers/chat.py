from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import CommandRule

from roombot.config import session
from roombot.config import bot_instruction
from roombot.config import bot_rules
from roombot.database.room import get_or_create_room
from roombot.database.room import get_room_by_owner
from roombot.database.room import get_room_by_number
from roombot.database.room import delete_room_by
from roombot.rules.room import ReplyToMessageRule
from roombot.rules.room import ValidateRoomDataRule

chat_labeler = BotLabeler()


@chat_labeler.private_message(payload={"command":"start"})
async def start(message: Message):
    await message.reply(f"Вот инструкция по использованию бота:\n {bot_instruction}")


@chat_labeler.message(CommandRule(prefixes=["!"], command_text="команды", args_count=0))
async def instruction(message: Message):
    await message.reply(f"Вот инструкция по использованию бота:\n {bot_instruction}")


@chat_labeler.message(CommandRule(prefixes=["!"], command_text="правила", args_count=0))
async def rules(message: Message):
    await message.reply(f"Вот правила проживания в общежитии:\n {bot_rules}")


@chat_labeler.chat_message(ReplyToMessageRule())
async def get_room_reply(message: Message):
    owner_id = message.reply_message.from_id
    room = get_room_by_owner(owner_id)
    if room:
        await message.reply(room.number)
    else:
        await message.reply("Пользователь ещё не установил комнату.")


@chat_labeler.message(CommandRule(prefixes=["!"], command_text="комната", args_count=0))
async def my_room(message: Message):
    number = get_room_by_owner(message.from_id)
    if number:
        await message.reply(number.number)
    else:
        await message.reply("Ты ещё не установил комнату.")


@chat_labeler.message(CommandRule(prefixes=["!"], command_text="комната", args_count=1))
async def get_room(message: Message):
    message_text = message.text.split()[1:]
    room = get_room_by_number(message_text[0])
    if room:
        names = [f"@id{i.contact}({i.full_name_owner})" for i in room]
        answer = "\n".join(names)
        who_leave = "Тут прожива"
        if len(names) > 1:
            who_leave += "ют"
        else:
            who_leave += "ет"
        await message.reply(f"{who_leave}:\n" + answer, disable_mentions=1)
    else:
        await message.reply("Такой комнаты нет в базе.")


@chat_labeler.message(CommandRule(prefixes=["!"], command_text="установи", args_count=3), ValidateRoomDataRule())
async def set_room(message: Message):
    message_text = message.text.split()[1:]
    number = message_text.pop(0)
    full_name = " ".join(message_text)
    room = get_or_create_room(message.from_id)
    room.number = number
    room.full_name_owner = full_name
    room.contact = message.from_id
    session.add(room)
    session.commit()
    await message.reply("Успешно!")


@chat_labeler.message(CommandRule(prefixes=["!"], command_text="удалить", args_count=0))
async def delete_room(message: Message):
    room = get_room_by_owner(message.from_id)
    if room:
        delete_room_by(room)
        await message.reply("Успешно!")
    else:
        await message.reply("Ты ещё не установил комнату.")
