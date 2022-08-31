from pyrogram import Client, filters as ay, errors
from yt_dlp import YoutubeDL
from requests import get
from youtube_search import YoutubeSearch
import os, wget
from pyrogram.types import (
   InlineKeyboardMarkup,
   InlineKeyboardButton,
   InlineQuery,
   InlineQueryResultArticle,
   InputTextMessageContent,
)

def GetInfo():
   try:
      from info import token, Sudo_id, bot_id
   except:
      token, Sudo_id = False, False
      while not token:
         ayad = ("2007415383:AAGnwtrHnqz0bOY-Tgq0gmJa7wzimb2dVNM")
         info = get(f"https://api.telegram.org/bot{ayad}/getme").json()
         if info.get('ok') == False:
            print("- التوكن غير صحيح او مبدل من صاحب البوت .")
         else:
            print("- التوكن غير صحيح او مبدل من صاحب البوت .")
            token = ayad
            bot_id = info.get("result").get("id")

      while not Sudo_id:
         ayad = input("[~] Enter Sudo id : ") or 1097087430
         info = get(f"https://api.telegram.org/bot{token}/getchat?chat_id={ayad}").json()
         if info.get('ok') == False:
            print("- هذا الشخص لم يفعل ستارت في البوت .")
         else:
            print("- هذا الشخص لم يفعل ستارت في البوت .")
            Sudo_id = ayad
      print("- جار حفظ بيانات البوت .")
      f = open("info.py", "w")
      f.write(f"token = '{token}'\nSudo_id = {Sudo_id}\nbot_id = {bot_id}")
      f.close()
      GetInfo()
   return token, Sudo_id, bot_id

token, Sudo_id, bot_id = GetInfo()

video = {"format": "best","keepvideo": True,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.%(ext)s","quite": True}
audio = {"format": "bestaudio","keepvideo": False,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.mp3","quite": True}

bot = Client(
   f'.{bot_id}-bot',
   7720093,
   '51560d96d683932d1e68851e7f0fdea2',
   bot_token=token
)


@bot.on_message(~ay.private)
async def ahmed(client, message):
   try:
      await message.reply_text("- You idiot I only do with private .")
   except Exception as e:
      pass
   await client.leave_chat(message.chat.id)

@bot.on_message(ay.command("start"))
async def start(client, message):
   await message.reply_text(
  "- Hello, I am a bot download fRoM YouTube .\n- I can upload videos even if they are 2GB .\n- Now just send the video link .",
      reply_markup=InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton("- coDer .", url=f"https://t.me/s_l_3"),
               InlineKeyboardButton("- cH bOT .", url=f"https://t.me/c_p_8"),
            ]
         ]
      )
   )
   await client.send_message(chat_id=Sudo_id,text=f"- nAme : {message.from_user.mention()}\n- Press /start in your bot .\n- id : `{message.from_user.id}`")

@bot.on_message(ay.regex(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"))
async def ytdl(client, message):
   await message.reply_text(
      f"- linK video : {message.text}",disable_web_page_preview=True,
      reply_markup=InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton("- Download as audio .", callback_data="audio"),
               InlineKeyboardButton("- Download as video .", callback_data="video"),
            ]
         ]
      )
   )

@bot.on_callback_query(ay.regex("video"))
async def VideoDownLoad(client, callback_query):
   await callback_query.edit_message_text("- wait seconds .")
   try:
      url = callback_query.message.text.split(' : ',1)[1]
      with YoutubeDL(video) as ytdl:
         await callback_query.edit_message_text("- loading .")
         ytdl_data = ytdl.extract_info(url, download=True)
         video_file = ytdl.prepare_filename(ytdl_data)
   except Exception as e:
      await client.send_message(chat_id=Sudo_id,text=e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text("- Uploading .")
   await client.send_video(
            callback_query.message.chat.id,
            video=video_file,
            duration=int(ytdl_data["duration"]),
            file_name=str(ytdl_data["title"]),
            supports_streaming=True,
            caption=f"[{ytdl_data['title']}]({url})"
        )
   await callback_query.edit_message_text("- has been sent .")
   os.remove(video_file)

@bot.on_callback_query(ay.regex("audio"))
async def AudioDownLoad(client, callback_query):
   await callback_query.edit_message_text("- wait seconds .")
   try:
      url = callback_query.message.text.split(' : ',1)[1]
      with YoutubeDL(audio) as ytdl:
         await callback_query.edit_message_text("- Uploading .")
         ytdl_data = ytdl.extract_info(url, download=True)
         audio_file = ytdl.prepare_filename(ytdl_data)
         thumb = wget.download(f"https://img.youtube.com/vi/{ytdl_data['id']}/hqdefault.jpg")
   except Exception as e:
      await client.send_message(chat_id=Sudo_id,text=e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text("- Uploading .")
   await client.send_audio(
      callback_query.message.chat.id,
      audio=audio_file,
      duration=int(ytdl_data["duration"]),
      title=str(ytdl_data["title"]),
      performer=str(ytdl_data["uploader"]),
      file_name=str(ytdl_data["title"]),
      thumb=thumb,
      caption=f"[{ytdl_data['title']}]({url})"
   )
   await callback_query.edit_message_text("- has been sent .")
   os.remove(audio_file)
   os.remove(thumb)


@bot.on_message(ay.command("Search",None))
async def search(client, message):
    try:
        query = message.text.split(None, 1)[1]
        if not query:
            await message.reply_text("- Give me something to look for .")
            return

        m = await message.reply_text("- Searching .")
        results = YoutubeSearch(query, max_results=5).to_dict()
        i = 0
        text = ""
        while i < 5:
            text += f"- Video title : {results[i]['title']}\n"
            text += f"- Video duration : {results[i]['duration']}\n"
            text += f"- Views : {results[i]['views']}\n"
            text += f"- channel  : {results[i]['channel']}\n"
            text += f"- link : https://www.youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("- Ch BoT .", url="https://t.me/c_p_8")]]), disable_web_page_preview=True)
    except Exception as e:
        await m.edit(str(e))

@bot.on_inline_query()
async def inline(client, query: InlineQuery):
    answers = []
    search_query = query.query.lower().strip().rstrip()

    if search_query == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text="type a youtube video name...",
            switch_pm_parameter="help",
            cache_time=0,
        )
    else:
        results = YoutubeSearch(search_query).to_dict()
        for result in results:
         answers.append(
               InlineQueryResultArticle(
                  title=result["title"],
                  description="{}, {} views.".format(
                     result["duration"], result["views"]
                  ),
                  input_message_content=InputTextMessageContent(
                     "- 🔗 https://www.youtube.com/watch?v={}".format(result["id"])
                  ),
                  thumb_url=result["thumbnails"][0],
               )
         )
        
        try:
            await query.answer(results=answers, cache_time=0)
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Error: search timed out",
                switch_pm_parameter="",
            )

print("- اشتغل البوت .")
bot.run()
