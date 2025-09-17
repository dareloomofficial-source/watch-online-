import requests
from telegram.ext import Updater, MessageHandler, Filters

# 🔑 Tumhara Streamtape account details
STREAMTAPE_LOGIN = "y7bhafra3bfxudz"   # (tumhara login ID yaha dalein)
STREAMTAPE_KEY = "02d86c050bb5ea3caec0"  # (tumhara API key)

# 🔑 Tumhara Telegram bot token
BOT_TOKEN = "8335001520:AAGcSSKSQQzw1e3_3whC7ZEr6Vtz1SW12O0"

# Jab user video/document bheje
def handle_video(update, context):
    file = update.message.video or update.message.document

    if not file:
        update.message.reply_text("⚠️ Sirf video/document send karo.")
        return

    # Telegram file link nikalna
    file_id = file.file_id
    new_file = context.bot.get_file(file_id)
    telegram_file_url = new_file.file_path

    update.message.reply_text("⏳ Uploading to Streamtape...")

    # Streamtape Remote Upload API
    api_url = f"https://api.streamtape.com/remotedl/add?login={STREAMTAPE_LOGIN}&key={STREAMTAPE_KEY}&url={telegram_file_url}"
    res = requests.get(api_url).json()

    if res.get("status") == 200:
        file_id = res["result"]["id"]
        watch_link = f"https://streamtape.com/v/{file_id}/"
        embed_link = f"https://streamtape.com/e/{file_id}/"
        update.message.reply_text(f"✅ Uploaded!\n\n🎬 Watch: {watch_link}\n📺 Embed: {embed_link}")
    else:
        update.message.reply_text(f"❌ Error: {res}")

# Bot start
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.video | Filters.document, handle_video))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
