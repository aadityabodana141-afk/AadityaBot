import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import edge_tts

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Aapka Naya Telegram Token
TOKEN = "8657911286:AAHlXIfLZOAc0YEYQ4cus77oXhLOjilc9g"

# Fast Voice Generation Function
async def text_to_speech(text, output_file="voice.mp3"):
    # Sabse fast aur natural voice
    voice = "en-US-AriaNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Turant message bhejein taaki user ko pata chale bot kaam kar raha hai
    status_msg = await update.message.reply_text("⏳ Generating voice quickly...")
    
    audio_path = "output.mp3"
    try:
        # Voice banayein
        await text_to_speech(user_text, audio_path)
        
        # Audio bhejein
        with open(audio_path, "rb") as audio:
            await update.message.reply_voice(voice=audio)
            
        # Status message hata dein
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text(f"Error: {e}")

# ==========================================
# RENDER PORT BINDING SERVER
# ==========================================
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()
# ==========================================

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Fast Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
    
        
