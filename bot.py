from pyrogram.types import InputMediaPhoto, InputMediaVideo
from pyrogram.enums import ChatType

import config
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.enums.message_entity_type import MessageEntityType
import db

db.start_db()
bot = Client("my_account",
             api_id=config.api_id,
             api_hash=config.api_hash)
print("Bot started")


# **********************************************************************************************************************
# **********************************************************************************************************************
# ОСНОВНАЯ ФУНКЦИЯ

async def text_formatter(message_text, entities, url, my_promo, promo):
    edit_t = message_text
    promo_size = len(promo)
    if entities is None:
        return message_text
    for i in entities:
        if i.type == MessageEntityType.TEXT_LINK:
            if i.length != promo_size:
                edit_t = edit_t.replace(message_text[i.offset: i.offset + i.length], '')
            if i.length == promo_size:
                edit_t = edit_t.replace(promo, my_promo)
                where = edit_t.find(f'{my_promo}')
                coord = edit_t[where: where + promo_size]
                edit_t = edit_t.replace(
                    coord,
                    f'<a href="{url}">{coord}</a>')





        # if i.type == MessageEntityType.BOLD:
        #     edit_t = edit_t.replace(
        #         message_text[i.offset: i.offset + i.length],
        #         f'<b>{message_text[i.offset: i.offset + i.length]}</b>')
        # if i.type == MessageEntityType.ITALIC:
        #     edit_t = edit_t.replace(
        #         message_text[i.offset: i.offset + i.length],
        #         f'<i>{message_text[i.offset: i.offset + i.length]}</i>')
        # if i.type == MessageEntityType.MENTION:
        #     edit_t = edit_t.replace(
        #         message_text[i.offset: i.offset + i.length],
        #         f'{username}')
    return edit_t


# **********************************************************************************************************************
# **********************************************************************************************************************
# КОМАНДЫ

@bot.on_message(filters.regex('^add new pattern'))  # add new pattern *name* *channel id* *link* *promo-code*
async def new_pattern(_, message: Message):
    text = message.text
    text = text.split()
    db.add_pattern(text)
    await bot.send_message(message.from_user.id, 'Паттерн добавлен')


@bot.on_message(filters.regex('^add my channel'))  # add my channel *name* *channel id*
async def add_channel(_, message: Message):
    text = message.text
    text = text.split()
    db.add_my_channel(text[3], int(text[4]))
    await bot.send_message(message.from_user.id, f'Добавлен канал: {int(text[4])}')


@bot.on_message(filters.regex('^add_promocode'))  # add_promocode_*name*_*promocode*
async def add_channel(_, message: Message):
    text = message.text
    text = text.split('_')
    db.add_promocode(text[2], text[3])
    await bot.send_message(message.from_user.id, f'Добавлен промокод: {text[3]}')


@bot.on_message(filters.regex('^delete pattern'))  # delete pattern *name*
async def chat_list_downloader(_, message: Message):
    text = message.text
    text = text.split()
    db.delete_pattern(text[2])
    await bot.send_message(message.from_user.id, 'Паттерн удалён')


@bot.on_message(filters.regex('^delete channel'))  # delete channel *channel id*
async def chat_list_downloader(_, message: Message):
    text = message.text
    text = text.split()
    db.delete_channel(text[2])
    await bot.send_message(message.from_user.id, 'Канал удалён')


@bot.on_message(filters.regex('^delete_promocode'))  # delete_promocode_*promocode*
async def chat_list_downloader(_, message: Message):
    text = message.text
    text = text.split('_')
    db.delete_promocode(text[2])
    await bot.send_message(message.from_user.id, 'Промокод удалён')


@bot.on_message(filters.regex('^view channels'))  # view channels *name*
async def chat_list_downloader(_, message: Message):
    text = message.text
    text = text.split()
    my_chnl = db.get_my_channel(text[2:])
    for i in my_chnl:
        await bot.send_message(message.from_user.id, f'Мои каналы паттерна {i[1]}:\n'
                                                     f'{i[2]}\n')


@bot.on_message(filters.regex('^view promocode'))  # view promocode *name*
async def chat_list_downloader(_, message: Message):
    text = message.text
    text = text.split()
    my_chnl = db.get_promocode(text[2:])
    for i in my_chnl:
        await bot.send_message(message.from_user.id, f'Промокод на который меняем:\n'
                                                     f'{i[2]}\n')


@bot.on_message(filters.regex('^reload$'))
async def chat_list_downloader(_, message: Message):
    await bot.send_message(message.from_user.id, f'Перезагрузка...')
    raise SystemExit(1)


@bot.on_message(filters.regex('^update donor channel'))  # update donor channel *name* *channel id*
async def chat_list_downloader(_, message: Message):
    text = message.text
    text = text.split()
    db.update_donor_channel(text[3], text[4])
    await bot.send_message(message.from_user.id, 'Канал донор изменён')


@bot.on_message(filters.regex('^update link'))  # update link *name* *link*
async def chat_list_downloader(_, message: Message):
    text = message.text
    text = text.split()
    db.update_link(text[2], text[3])
    await bot.send_message(message.from_user.id, 'Ссылка изменена')


@bot.on_message(filters.regex('^update promocode'))  # update promocode *name* *promocode*
async def chat_list_downloader(_, message: Message):
    text = message.text
    text = text.split()
    db.update_promocode(text[2], text[3])
    await bot.send_message(message.from_user.id, 'Промокод изменен')


@bot.on_message(filters.regex('^view all pattern'))
async def chat_list_downloader(_, message: Message):
    for i in db.view_all_pattern():
        await bot.send_message(message.from_user.id, f'{i[0]} паттерн:\n\n'
                                                     f'Имя: {i[1]}\n'
                                                     f'Канал донор: {i[2]}\n'
                                                     f'Ссылка: {i[3]}\n'
                                                     f'Промокод: {i[4]}\n')


@bot.on_message(filters.regex('^help$'))
async def chat_list_downloader(_, message: Message):
    await bot.send_message(message.from_user.id, f'**Добавить паттерн:**\n'
                                                 f'add new pattern (name) '
                                                 f'(donor_channel_id) '
                                                 f'(link) '
                                                 f'(promocode)\n\n'

                                                 f'**Добавить мой канал:**\n'
                                                 f'add my channel (name) (channel_id)\n\n'

                                                 f'**Добавить промокод:**\n'
                                                 f'add_promocode_name_promocode\n\n'

                                                 f'**Удалить паттерн:**\n'
                                                 f'delete pattern (name)\n\n'

                                                 f'**Удалить мой канал:**\n'
                                                 f'delete channel (channel_id)\n\n'

                                                 f'**Удалить промокод:**\n'
                                                 f'delete_promocode_(promocode)\n\n'

                                                 f'**Мои каналы:**\n'
                                                 f'view channels (name)\n\n'

                                                 f'**Посмотреть промокод:**\n'
                                                 f'view promocode (name)\n\n'

                                                 f'**Посмотреть все паттерны:**\n'
                                                 f'view all pattern\n\n'

                                                 f'**Перезагрузка бота:**\n'
                                                 f'reload\n\n'

                                                 f'**Изменить канал донор в паттернне:**\n'
                                                 f'update donor channel (name) (channel_id)\n\n'

                                                 f'**Изменить ссылку в паттернне:**\n'
                                                 f'update link (name) (link)\n\n'

                                                 f'**Изменить промокод в паттернне:**\n'
                                                 f'update promocode (name) (promocode)\n\n'

                                                 f'<**Важно соблюдать регистр команд и пробелы**>\n')


@bot.on_message(filters.regex('chats'))
async def chat_list_downloader(_, message: Message):
    message_text = 'Список моих чатов:\n'
    data = bot.get_dialogs()
    async for dialogs in data:
        if dialogs.chat.type == ChatType.CHANNEL:
            message_text += f"\n{dialogs.chat.title} @{dialogs.chat.username}\n"
            message_text += f"{dialogs.chat.id}\n"
    await bot.send_message(message.from_user.id, message_text)


# **********************************************************************************************************************
# **********************************************************************************************************************
# ОСНОВА

@bot.on_message(filters.text)
async def echo_channel(_, message: Message):
    data_list = db.get_channels_data()
    for donor_id, target_id, lnk, my_promo, promo in data_list:
        if donor_id == message.chat.id:
            new_message = await text_formatter(message.text, message.entities, lnk, my_promo, promo)
            await bot.send_message(target_id,
                                   f"{new_message}",
                                   parse_mode=enums.ParseMode.HTML,
                                   disable_web_page_preview=True)


send_media_groups = []


@bot.on_message(filters.media_group)
async def another_one(_, message: Message):
    if message.media_group_id not in send_media_groups:
        send_media_groups.append(message.media_group_id)
        data_list = db.get_channels_data()
        for donor_id, target_id, lnk, my_promo, promo in data_list:
            if donor_id == message.chat.id:
                media_messages_income = await bot.get_media_group(message.chat.id, message.id)

                data = await text_formatter(media_messages_income[0].caption, media_messages_income[0].caption.entities,
                                            lnk, my_promo, promo)
                photo_list = [InputMediaPhoto(media_message.photo.file_id, caption=data,
                                              parse_mode=enums.ParseMode.HTML)
                              if media_message.photo is not None else InputMediaVideo(media_message.video.file_id,
                                                                                      caption=data,
                                                                                      parse_mode=enums.ParseMode.HTML)
                              for media_message in media_messages_income[:1]]

                photo_list += [InputMediaPhoto(media_message.photo.file_id)
                               if media_message.photo is not None else InputMediaVideo(media_message.video.file_id)
                               for media_message in media_messages_income[1:]]

                await bot.send_media_group(chat_id=target_id, media=photo_list)


@bot.on_message(~ filters.caption & ~ filters.text)  # no TEXT and no caption content
async def resend_media(_, message: Message):
    data_list = db.get_channels_data()
    for donor_id, target_id in data_list:
        if donor_id == message.chat.id:
            await bot.copy_message(chat_id=target_id,
                                   from_chat_id=message.chat.id,
                                   message_id=message.id)


# PHOTO
@bot.on_message(filters.photo)
async def get_photo(_, message: Message):
    data_list = db.get_channels_data()
    for donor_id, target_id, lnk, my_promo, promo in data_list:
        if donor_id == message.chat.id:
            caption = await text_formatter(message.caption, message.caption_entities, lnk, my_promo, promo)
            await bot.send_photo(target_id,
                                 photo=message.photo.file_id,
                                 caption=caption)


# VIDEO
@bot.on_message(filters.video)
async def get_photo(_, message: Message):
    data_list = db.get_channels_data()
    for donor_id, target_id, lnk, my_promo, promo in data_list:
        if donor_id == message.chat.id:
            caption = await text_formatter(message.caption, message.caption_entities, lnk, my_promo, promo)
            await bot.send_video(target_id,
                                 video=message.video.file_id,
                                 caption=caption)


# **********************************************************************************************************************


if __name__ == '__main__':
    bot.run()
