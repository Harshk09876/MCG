import instaloader
import os
import json
import time
import random

# Bot configuration
BOT_TOKEN = '8088308793:AAHvoY0FSpFghfxE_0v06NKVEj1dNWuWv2k'
OWNER_ID = 7086729173  # Replace with your Telegram ID
ADMIN_IDS = [OWNER_ID]
bot = telebot.TeleBot(BOT_TOKEN)

# /start
@bot.message_handler(commands=['start'])
def start_cmd(msg):
    bot.reply_to(msg, "🔥 *Welcome to the @DARKMODOFFICAL Bot!*\n💻

# ✅ Color Codes
colors = [
    '\033[91m',  # Red
    '\033[92m',  # Green
    '\033[93m',  # Yellow
    '\033[94m',  # Blue
    '\033[95m',  # Magenta
    '\033[96m',  # Cyan
]
RESET = '\033[0m'

# ✅ Banner
def banner():
    os.system("clear")
    red = '\033[91m'
    green = '\033[92m'
    print(red + "="*60 + RESET)
    print(red + "="*60 + RESET)
    print(green + "                🔥 CYBER ANISH 🔥".center(60).upper() + RESET)
    print(green + "         POWERED BY: @CYB3RS0LDIER".center(60).upper() + RESET)
    print(green + "     TELEGRAM: T.ME/CYBERANISH_OFFICIAL".center(60).upper() + RESET)
    print(red + "="*60 + RESET)
    print(red + "="*60 + RESET)
    time.sleep(1)

# ✅ Fetch Info
def get_instagram_info(username):
    try:
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, username)

        info = {
            "USERNAME (CYBER ANISH)": profile.username,
            "FULL NAME (CYBER ANISH)": profile.full_name,
            "BIO (CYBER ANISH)": profile.biography,
            "FOLLOWERS (CYBER ANISH)": profile.followers,
            "FOLLOWING (CYBER ANISH)": profile.followees,
            "TOTAL POSTS (CYBER ANISH)": profile.mediacount,
            "PROFILE PIC URL (CYBER ANISH)": str(profile.profile_pic_url)
        }

        return info

    except Exception as e:
        print(f"\n\033[91m❌ ERROR: {e}{RESET}")
        return None

# ✅ Save to file
def save_to_file(data, username):
    file_name = f"{username}_info_by_CYBER_ANISH.json"
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)
    print(f"\n\033[92m✅ DATA SAVED TO: {file_name} (CYBER ANISH){RESET}")

# ✅ Main Program
if __name__ == "__main__":
    banner()
    username = input("\033[96m👤 ENTER INSTAGRAM USERNAME (WITHOUT @): \033[0m").strip()
    info = get_instagram_info(username)

    if info:
        print("\n\033[95m📄 EXTRACTED INFO:\033[0m\n")
        for i, (key, value) in enumerate(info.items()):
            color = colors[i % len(colors)]
            print(f"{color}{key}: {value} (CYBER ANISH){RESET}")
        save_to_file(info, username)
        print(f"\n\033[92m👑 SCRIPT BY: CYBER ANISH | TELEGRAM: @CYB3RS0LDIER{RESET}")