import random
from telegram.ext import Updater, CommandHandler
import os

# Load token securely from token.txt
def get_token():
    try:
        with open("7729772878:AAElbpzU7bw0xd0Bl1ANquHZtY6lZq-bMN0", "r") as f:
            return f.read().strip()
    except:
        print("❌ token.txt file missing")
        exit(1)

# Luhn algorithm for card validity
def luhn_checksum(card_number):
    def digits_of(n): return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    checksum = 0
    odd = digits[-1::-2]
    even = digits[-2::-2]
    checksum += sum(odd)
    for d in even:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0

# Generate cards from BIN
def generate_cc_from_bin(bin_str, count=5, bot_id="BOT-001"):
    cards = []
    id_counter = 1
    while len(cards) < count:
        num = bin_str + ''.join(str(random.randint(0, 9)) for _ in range(16 - len(bin_str) - 1))
        for i in range(10):
            trial = num + str(i)
            if is_luhn_valid(trial):
                bot_tag = f"{bot_id}-{str(id_counter).zfill(4)}"
                cards.append(f"{bot_tag}: {trial}")
                id_counter += 1
                break
    return cards

# Command handler
def generate(update, context):
    if len(context.args) == 0:
        update.message.reply_text("❗ Usage: /gen <BIN>\nExample: /gen 411111")
        return

    bin_input = context.args[0]
    if not bin_input.isdigit() or len(bin_input) < 6:
        update.message.reply_text("❌ Invalid BIN. Use at least 6 digits.")
        return

    cards = generate_cc_from_bin(bin_input)
    message = f"BIN: {bin_input}\n" + "\n".join(cards)
    update.message.reply_text(message)

# /start command
def start(update, context):
    update.message.reply_text("👋 Welcome to the CC Generator Bot.\nSend /gen <BIN> to generate cards.\nExample: /gen 411111")

# Main bot setup
def main():
    token = get_token()
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gen", generate))

    updater.start_polling()
    print("✅ Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()