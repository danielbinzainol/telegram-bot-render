import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- 1. THE FAKE WEBSITE (Tricks Render into thinking we are a web app) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "I am alive! 🤖"

def run_web_server():
    # Render gives us a specific port in the environment variable 'PORT'
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def start_web_server():
    # Run Flask in a separate thread so it doesn't block the bot
    t = Thread(target=run_web_server)
    t.daemon = True
    t.start()

# --- 2. THE REAL BOT CODE ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am running on the Render Cloud! ☁️")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Echo: {update.message.text}")

if __name__ == '__main__':
    # A. Start the fake website
    start_web_server()
    
    # B. Get Token from Render Environment (Secure)
    TOKEN = os.environ.get('TOKEN')
    
    if not TOKEN:
        print("Error: No TOKEN found. Set it in Render Dashboard!")
    else:
        print("Bot is starting...")
        application = ApplicationBuilder().token(TOKEN).build()
        
        # Add your handlers here
        application.add_handler(CommandHandler("start", start))
        # application.add_handler(...) 
        
        # Start Polling
        application.run_polling()