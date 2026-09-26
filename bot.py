import os
import sys
import asyncio
import logging
from pathlib import Path

import edge_tts
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("voiceover_bot")

TELEGRAM_BOT_TOKEN = "8869199245:AAE-R5Ns726Wm8VIg19D-1Z1by3366QaFRo"

# YouTube Shorts ke liye sabse best energetic aur viral hindi voice
VOICE_NAME = "hi-IN-SwaraNeural"

async def generate_voiceover(text: str, out_path: str):
    communicate = edge_tts.Communicate(text, VOICE_NAME, rate="+5%", pitch="+0Hz")
    await communicate.save(out_path)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return

    msg = await update.message.reply_text("🎙️ Shorts ke liye shandaar voiceover taiyar ho raha hai...")
    
    output_audio = "voiceover.mp3"
    try:
        # Edge TTS ke zariye voiceover generate karein
        asyncio.run(generate_voiceover(user_text, output_audio))
        
        # Telegram par audio file bhejen
        await update.message.reply_audio(
            audio=open(output_audio, "rb"), 
            title="Shorts Voiceover", 
            caption="🔥 Yeh lijiye aapka viral style voiceover ready hai!"
        )
        await msg.delete()
        
    except Exception as e:
        log.exception("Voiceover generation failed")
        await msg.edit_text(f"Kuch gadbad ho gayi: {e}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    log.info("Voiceover Bot running - send text on Telegram.")
    app.run_polling()

if __name__ == "__main__":
    main()
      
