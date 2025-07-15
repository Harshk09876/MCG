import random
import os
from telegram.ext import Updater, CommandHandler

# Luhn & Generator
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

# Telegram command
def generate(update, context):
    if len(context.args) == 0:
        update.message.reply_text("Please provide a BIN, e.g.: /gen 411111")
        return
    bin_input = context.args[0]
    if not bin_input.isdigit() or len(bin_input) < 6:
        update.message.reply_text("Invalid BIN. Must be at least 6 digits.")
        return
    cards = generate_cc_from_bin(bin_input)
    reply = f"BIN: {bin_input}\n" + "\n".join(cards)
    update.message.reply_text(reply)

def start(update, context):
    update.message.reply_text("Send /gen <bin> to generate test cards.")

# Main entry
def main():
    token = os.getenv("7729772878:AAElbpzU7bw0xd0Bl1ANquHZtY6lZq-bMN0")
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN environment variable not set.")
        return

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("generate", generate))

    updater.start_polling()
    print("✅ Bot running...")
    updater.idle()

if __name__ == "__main__":
    main()