from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

TOKEN: Final = '7826958531:AAGW_oUAL1-pubEAgaY821XUXUol96fc1Z0'
BOT_USERNAME: Final = '@EasyPeasyCrazyBot'
GENAI_API_KEY: Final = 'AIzaSyCUbceNtN2jWIVzYWJN4MA0Cd2A1xeRiSg'
genai.configure(api_key=GENAI_API_KEY)
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
MODEL_NAME: Final = genai.GenerativeModel('gemini-pro', generation_config=generation_config)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
    <b>Welcome to the EasyPeasyChat!</b><br>
    <a href="https://github.com/noxur05">Github Profile</a> of author.<br>
    <u>Enjoy using the bot!</u>
    """
    await update.message.reply_text("Hello!!!")

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

if __name__ == "__main__": 
    print("Starting bot")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)
    print("Polling Interval")
    app.run_polling(poll_interval=3)