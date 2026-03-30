import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# YOUR BOT TOKEN ✅
TELEGRAM_TOKEN = "8741854135:AAH5yUePFLgNcg5P6LvbHOzXa75uITlLRME"

logging.basicConfig(level=logging.INFO)
client = OpenAI()
user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🤖 **AI TEACHER BOT READY!** 🎓

**Main sikhaunga:**
- Maths 📊
- Coding 💻  
- Science 🔬
- English ✍️
- History 📜

**Try karo:**
"Python functions samjhao"
"Algebra solve karo"
"HTML basics sikhao"

Shuru! 🚀
    """, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    query = update.message.text
    
    # Session start
    if user_id not in user_sessions:
        user_sessions[user_id] = []
    
    user_sessions[user_id].append({"role": "user", "content": query})
    if len(user_sessions[user_id]) > 12:
        user_sessions[user_id] = user_sessions[user_id][-12:]
    
    # Typing...
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        messages = user_sessions[user_id].copy()
        messages.insert(0, {
            "role": "system",
            "content": """Tu dost-teacher hai. Hindi+English mix. 

**Style:**
✅ Simple language
✅ Step-by-step 
✅ Examples de
✅ Galti politely bata
✅ Practice question puchh
✅ Motivate kar 😊

**Format:**
1. Samjhaya ✅
2. Example 📝  
3. Practice ❓"""
        })
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=900,
            temperature=0.7
        )
        
        reply = response.choices[0].message.content
        user_sessions[user_id].append({"role": "assistant", "content": reply})
        
        await update.message.reply_text(reply, parse_mode='Markdown')
        
    except Exception:
        await update.message.reply_text("🔄 Dobara try kar!")

# START BOT
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🎓 AI Teacher Bot Started!")
    app.run_polling()

if __name__ == '__main__':
    main()
