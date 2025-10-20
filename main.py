import telebot, os, uuid, psutil
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

os.makedirs("downloads", exist_ok=True)

def add_bouncing_text(input_path, output_path, text1="only tele", text2="@LOKALANN"):
    clip = VideoFileClip(input_path)
    txt1 = TextClip(text1, fontsize=clip.h//15, color='white',
                    stroke_color='black', stroke_width=2, font='Arial-Bold')
    txt2 = TextClip(text2, fontsize=clip.h//20, color='white',
                    stroke_color='black', stroke_width=2, font='Arial-Bold')

    # teks muncul lembut dan mantul halus
    txt1 = txt1.set_position(('center', clip.h//3)).fadein(0.5).fadeout(0.5).set_start(3)
    txt2 = txt2.set_position(('center', clip.h//2)).fadein(0.5).fadeout(0.5).set_start(5)

    final = CompositeVideoClip([clip, txt1, txt2])
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=4)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    chat_id = message.chat.id
    bot.reply_to(message, "🎬 Proses video... teks muncul detik ke-3 dan lembut mantul...")

    try:
        file_info = bot.get_file(message.video.file_id)
        downloaded = bot.download_file(file_info.file_path)
        uid = uuid.uuid4().hex[:6]
        inp = f"downloads/in_{uid}.mp4"
        out = f"downloads/out_{uid}.mp4"

        with open(inp, "wb") as f:
            f.write(downloaded)

        add_bouncing_text(inp, out)

        with open(out, "rb") as v:
            bot.send_video(chat_id, v, caption="✅ Selesai!")

    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Error: {e}")
    finally:
        for p in [inp, out]:
            if os.path.exists(p):
                os.remove(p)

bot.infinity_polling()
