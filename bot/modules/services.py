from html import escape
from time import time
from uuid import uuid4

from aiofiles import open as aiopen

from bot import LOGGER, user_data
from bot.core.aeon_client import TgClient
from bot.core.config_manager import Config
from bot.helper.ext_utils.bot_utils import new_task
from bot.helper.ext_utils.db_handler import database
from bot.helper.ext_utils.status_utils import get_readable_time
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.button_build import ButtonMaker
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import (
    auto_delete_message,
    delete_message,
    edit_message,
    send_file,
    send_message,
)


@new_task
async def start(client, message):
    sbutton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📢 𝐔𝐩𝐝𝐚𝐭𝐞𝐬 📢", url=""),
                InlineKeyboardButton("❄️ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 ❄️", url="")
            ],
            [
                InlineKeyboardButton("📜  📜", url="")
            ]
        ]
    )    
    if len(message.command) > 1 and message.command[1] == "private":
        await delete_message(message)
    elif len(message.command) > 1 and len(message.command[1]) == 36:
        userid = message.from_user.id
        input_token = message.command[1]
        stored_token = await database.get_user_token(userid)
        if stored_token is None:
            return await send_message(
                message,
                "<b>Looks like the token was not generate for you 🌚</b>\n\nPlease generate your own. 😁✌️",
            )
        if input_token != stored_token:
            return await send_message(
                message,
                "Invalid token.\n\nPlease generate a new one.",
            )
        if userid not in user_data:
            return await send_message(
                message,
                "This token is not yours!\n\nKindly generate your own.",
            )
        data = user_data[userid]
        if "TOKEN" not in data or data["TOKEN"] != input_token:
            return await send_message(
                message,
                "<b>This token has already been used!</b>\n\nPlease get a new one.",
            )
        token = str(uuid4())
        token_time = time()
        data["TOKEN"] = token
        data["TIME"] = token_time
        user_data[userid].update(data)
        await database.update_user_tdata(userid, token, token_time)
        msg = "Your token has been successfully generated!\n\n"
        msg += f"It will be valid for {get_readable_time(int(Config.TOKEN_TIMEOUT), True)}"
        return await send_message(message, msg)
    elif await CustomFilters.authorized(client, message):
        help_command = f"/{BotCommands.HelpCommand}"
        start_string = f"𝘏𝘦𝘭𝘭𝘰 𝘵𝘩𝘦𝘳𝘦!! \n\n𝘐'𝘮 𝘢𝘯 𝘢𝘥𝘷𝘢𝘯𝘤𝘦 𝘭𝘦𝘦𝘤𝘩 𝘣𝘰𝘵 𝘤𝘳𝘦𝘢𝘵𝘦𝘥 𝘉𝘺 <a href='http://t.me/The_TGguy'>𝘛𝘦𝘭𝘦𝘨𝘳𝘢𝘮 𝘎𝘶𝘺!!</a> 𝘐 𝘤𝘢𝘯 𝘸𝘰𝘳𝘬 𝘪𝘯 𝘗𝘔 𝘢𝘯𝘥 𝘢𝘭𝘴𝘰 𝘪𝘯 𝘈𝘶𝘵𝘩𝘰𝘳𝘪𝘻𝘦𝘥 𝘨𝘳𝘰𝘶𝘱𝘴! 𝘐 𝘴𝘶𝘱𝘱𝘰𝘳𝘵 𝘠𝘵𝘥𝘭, 𝘵𝘰𝘳𝘳𝘦𝘯𝘵𝘴, 𝘮𝘢𝘨𝘯𝘦𝘵 𝘭𝘪𝘯𝘬𝘴, 𝘭𝘦𝘦𝘤𝘩𝘪𝘯𝘨, 𝘮𝘪𝘳𝘳𝘰𝘳 𝘢𝘯𝘥 𝘮𝘰𝘳𝘦....\n\n<i>𝘓𝘦𝘢𝘳𝘯 𝘮𝘰𝘳𝘦 𝘢𝘣𝘰𝘶𝘵 𝘮𝘦 𝘰𝘯 {help_command}</i> \n\n<blockquote>Dᴏᴡɴʟᴏᴀᴅɪɴɢ 18+ sᴜᴄʜ ᴀs Pᴏʀɴ, ᴜʟʟᴜ ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ (ɴᴏ R@ᴘᴇ ᴏʀ ᴄᴘ, ɪғ ғᴏᴜɴᴅ ᴘᴇʀᴍᴀɴᴇɴᴛ ʙᴀɴ 🚫)</blockquote>"
        await send_message(message, start_string, buttons=sbutton)
    else:
        help_command = f"/{BotCommands.HelpCommand}"
        unauth = f"𝘏𝘦𝘭𝘭𝘰 𝘵𝘩𝘦𝘳𝘦!! \n\n𝘐'𝘮 𝘢𝘯 𝘢𝘥𝘷𝘢𝘯𝘤𝘦 𝘭𝘦𝘦𝘤𝘩 𝘣𝘰𝘵 𝘤𝘳𝘦𝘢𝘵𝘦𝘥 𝘉𝘺 <a href='http://t.me/The_TGguy'>𝘛𝘦𝘭𝘦𝘨𝘳𝘢𝘮 𝘎𝘶𝘺!!</a> 𝘐 𝘤𝘢𝘯 𝘸𝘰𝘳𝘬 𝘪𝘯 𝘗𝘔 𝘢𝘯𝘥 𝘢𝘭𝘴𝘰 𝘪𝘯 𝘈𝘶𝘵𝘩𝘰𝘳𝘪𝘻𝘦𝘥 𝘨𝘳𝘰𝘶𝘱𝘴! 𝘐 𝘴𝘶𝘱𝘱𝘰𝘳𝘵 𝘠𝘵𝘥𝘭, 𝘵𝘰𝘳𝘳𝘦𝘯𝘵𝘴, 𝘮𝘢𝘨𝘯𝘦𝘵 𝘭𝘪𝘯𝘬𝘴, 𝘭𝘦𝘦𝘤𝘩𝘪𝘯𝘨, 𝘮𝘪𝘳𝘳𝘰𝘳 𝘢𝘯𝘥 𝘮𝘰𝘳𝘦....\n\n<i>𝘓𝘦𝘢𝘳𝘯 𝘮𝘰𝘳𝘦 𝘢𝘣𝘰𝘶𝘵 𝘮𝘦 𝘰𝘯 {help_command}</i> \n\n<blockquote>Dᴏᴡɴʟᴏᴀᴅɪɴɢ 18+ sᴜᴄʜ ᴀs Pᴏʀɴ, ᴜʟʟᴜ ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ (ɴᴏ R@ᴘᴇ ᴏʀ ᴄᴘ, ɪғ ғᴏᴜɴᴅ ᴘᴇʀᴍᴀɴᴇɴᴛ ʙᴀɴ 🚫)</blockquote>"
        await send_message(message, unauth, buttons=sbutton)
    await database.update_pm_users(message.from_user.id)
    return None


@new_task
async def ping(_, message):
    start_time = round(time() * 1000)
    reply = await send_message(message, "Starting Ping 😉")
    end_time = round(time() * 1000)
    await edit_message(reply, f"{end_time - start_time} ms")


@new_task
async def log(_, message):
    buttons = ButtonMaker()
    buttons.data_button("View log", f"aeon {message.from_user.id} view")
    reply_message = await send_file(
        message,
        "log.txt",
        buttons=buttons.build_menu(1),
    )
    await delete_message(message)
    await auto_delete_message(reply_message, time=300)


@new_task
async def aeon_callback(_, query):
    message = query.message
    user_id = query.from_user.id
    data = query.data.split()
    if user_id != int(data[1]):
        return await query.answer(text="This message not your's!", show_alert=True)
    if data[2] == "view":
        await query.answer()
        async with aiopen("log.txt") as f:
            log_file_lines = (await f.read()).splitlines()

        def parseline(line):
            try:
                return line.split("] ", 1)[1]
            except IndexError:
                return line

        ind, log_lines = 1, ""
        try:
            while len(log_lines) <= 3500:
                log_lines = parseline(log_file_lines[-ind]) + "\n" + log_lines
                if ind == len(log_file_lines):
                    break
                ind += 1
            start_line = "<pre language='python'>"
            end_line = "</pre>"
            btn = ButtonMaker()
            btn.data_button("Close", f"aeon {user_id} close")
            reply_message = await send_message(
                message,
                start_line + escape(log_lines) + end_line,
                btn.build_menu(1),
            )
            await query.edit_message_reply_markup(None)
            await delete_message(message)
            await auto_delete_message(reply_message, time=300)
        except Exception as err:
            LOGGER.error(f"TG Log Display : {err!s}")
    elif data[2] == "private":
        await query.answer(url=f"https://t.me/{TgClient.NAME}?start=private")
        return None
    else:
        await query.answer()
        await delete_message(message)
        return None
