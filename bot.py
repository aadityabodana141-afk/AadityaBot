import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import edge_tts

# Logging setup taaki errors saaf dikhein
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Naya Telegram Bot Token
TOKEN = "8657911286:AAHlXIfLZOAc0YEYQ4cus77oXhLOjilc9g"

# Text ko audio (voice) me convert karne ka function
async def text_to_speech(text, output_file="voice.mp3"):
    voice = "en-US-AriaNeural"  # Aap apni pasand ki voice bhi rakh sakte hain
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

# Jab bhi user message bheje ga, ye function chalega
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("Aapka message mil gaya! Audio ban raha hai...")
    
    # Audio generate karein
    audio_path = "output.mp3"
    await text_to_speech(user_text, audio_path)
    
    # Telegram par audio file bhejein
    with open(audio_path, "rb") as audio:
        await update.message.reply_voice(voice=audio)

# ==========================================
# RENDER PORT BINDING SERVER (Port Error Hatane ke liye)
# ==========================================
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Server ko background thread me chalana
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()
# ==========================================

def main():
    # Bot Application Build karein
    application = ApplicationBuilder().token(TOKEN).build()

    # Message Handler jodein
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Bot ko start karein (Polling)
    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
        
