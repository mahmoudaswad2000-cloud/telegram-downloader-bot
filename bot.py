import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
import os

TOKEN = '8823255880:AAF93L25L5u5EX69Z8vF0xETIQMGV7vZedA'
bot = telebot.TeleBot(TOKEN)
MONETAG_LINK = 'https://uplcm.com/4/11970492'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    ad_button = InlineKeyboardButton(text="📢 اضغط هنا لدعمنا (مهم)", url=MONETAG_LINK)
    markup.add(ad_button)
    
    welcome_text = (
        "مرحباً بك في بوت تحميل الفيديوهات الشامل!\n\n"
        "1️⃣ أولاً: يرجى الضغط على الزر أدناه لمرة واحدة لدعم البوت.\n"
        "2️⃣ ثانياً: أرسل لي أي رابط فيديو من (تيك توك أو إنستغرام) وسأقوم بتحميله لك فوراً!"
    )
    bot.reply_to(message, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    
    if not url.startswith('http'):
        bot.reply_to(message, "الرجاء إرسال رابط صحيح يبدأ بـ http أو https")
        return

    msg = bot.reply_to(message, "⏳ جاري معالجة الفيديو وتحميله، يرجى الانتظار...")

    try:
        # إعدادات التحميل عبر yt-dlp
        ydl_opts = {
            'outtmpl': 'video.mp4',
            'format': 'mp4/best',
            'max_filesize': 50 * 1024 * 1024, # حد أقصى 50 ميجابايت لتناسب تليغرام
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # إرسال الفيديو للمستخدم
        with open('video.mp4', 'rb') as vid:
            markup = InlineKeyboardMarkup()
            ad_button = InlineKeyboardButton(text="🔗 رابط إضافي / دعم المطور", url=MONETAG_LINK)
            markup.add(ad_button)
            
            bot.send_video(message.chat.id, vid, caption="✅ تم التحميل بنجاح بواسطة البوت", reply_markup=markup)
        
        # حذف الملف المؤقت من التخزين بعد الإرسال
        if os.path.exists('video.mp4'):
            os.remove('video.mp4')
            
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء التحميل. تأكد أن الرابط عام وليس لحساب خاص.\nالخطأ: {str(e)}", message.chat.id, msg.message_id)

if __name__ == '__main__':
    print("Bot with downloader is running...")
    bot.infinity_polling()

