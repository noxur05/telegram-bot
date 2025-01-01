from typing import Final
import google.generativeai as genai
import asyncio
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

TOKEN: Final = '7922646695:AAGcsORIi8ZkIowQLFE04xOwYuvswwWfOt4'
BOT_USERNAME: Final = '@multi_job_bot'

GENAI_API_KEY: Final = 'AIzaSyCUbceNtN2jWIVzYWJN4MA0Cd2A1xeRiSg'
genai.configure(api_key=GENAI_API_KEY)
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
MODEL_NAME: Final = genai.GenerativeModel('gemini-pro', generation_config=generation_config)

from apps.users.models import User
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

@sync_to_async
def get_or_create_user(user_id):
    return User.objects.get_or_create(user_id=user_id)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    obj, created = await get_or_create_user(user_id)

    first_name = obj.first_name if obj.first_name else "Unknown"
    last_name = obj.last_name if obj.last_name else "User"

    await update.message.reply_text(f"Hi {first_name} {last_name}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("HELP!!!")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("CUstom!!!")

def generate_reply(prompt: str) -> str:
    try:
        formatted_prompt = f"System: You are friendly AI ChatBot.\nUser: {prompt}"
        response = MODEL_NAME.generate_content([formatted_prompt])
        candidate = response._result.candidates[0] if response._result.candidates else None
        if candidate and candidate.content.parts:
            return candidate.content.parts[0].text
        return "I couldn't generate a reply."
    except Exception as e:
        print(f"Error generating response for '{prompt}': {e}")
        return "An error occurred while generating a response."

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        await update.message.reply_text(f"{contact.first_name} {contact.last_name} {contact.user_id} {contact._bot} {contact.vcard} {contact.phone_number}")
    else:
        await update.message.reply_text("Something went wrong. Please try again.")
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User {update.message.chat.id} in {message_type}: '{text}'")

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip
            response: str = generate_reply(new_text)
        else:
            return
    else:
        response: str = generate_reply(text)
    print("Bot", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"{update} caused fucking error {context.error}")

async def main():
    print("Starting bot")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    app.add_error_handler(error)
    print("Polling Interval")
    app.run_polling(poll_interval=3)

if __name__ == "__main__": 
    asyncio.run(main())