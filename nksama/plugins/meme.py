from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from nksama import bot
from pyrogram import filters
from pyrogram.types import Message
import requests
from nksama import help_message 
from nksama.plugins.helpers import call_back_in_filter
from nksama.utils.errors import capture_err

@bot.on_callback_query(call_back_in_filter('meme'))
def callback_meme(_,query):
    if query.data.split(":")[1] == "next":
        query.message.delete()
        res = requests.get('https://nksamamemeapi.pythonanywhere.com').json()
        img = res['image']
        title = res['title']
        bot.send_photo(query.message.chat.id , img , caption=title , reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Next" , callback_data="meme:next")],
        ]))



@bot.on_message(filters.command('rmeme'))
def rmeme(_,message):
    res = requests.get('https://nksamamemeapi.pythonanywhere.com').json()
    img = res['image']
    title = res['title']
    bot.send_photo(message.chat.id , img , caption=title , reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Next" , callback_data="meme:next")]
    ]))

@bot.on_message(filters.command("webss"))
@capture_err
async def take_ss(_, message: Message):
    try:
        if len(message.command) != 2:
            return await message.reply_text("Give A Url To Fetch Screenshot.")
        url = message.text.split(None, 1)[1]
        m = await message.reply_text("**Taking Screenshot**")
        await m.edit("**Uploading**")
        try:
            await message.reply_photo(
                photo=f"https://webshot.amanoteam.com/print?q={url}",
                quote=False,
            )
        except TypeError:
            return await m.edit("No Such Website.")
        await m.delete()
    except Exception as e:

help_message.append(
    {
        "Module_Name": "meme",
        "Help": "/rmeme - to get random memes from reddit"
    }
)
