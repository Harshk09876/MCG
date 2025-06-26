import telebot
import datetime
import random
import logging
import subprocess
from flask import Flask, request, jsonify

# Initialize the bot with your bot's API token
bot = telebot.TeleBot('8088308793:AAHvoY0FSpFghfxE_0v06NKVEj1dNWuWv2k')

# Admin user IDs (replace with your own admin IDs as strings)
admin_ids = ["7086729173"]

app = Flask(__name__)

UC_PACKAGES = {
    "300 UC": 180,
    "600 UC": 400,
    "1500 UC": 1250,
    "3000 UC": 2800,
    "6000 UC": 5200
}

# Store session temporarily for demo (use a DB in production)
user_sessions = {}

@app.route('/start', methods=['GET'])
def start():
    return jsonify({
        "message": "🎮 Welcome to the UC Bot!",
        "instructions": "Choose a UC package from the list below.",
        "packages": UC_PACKAGES
    })

@app.route('/select_package', methods=['POST'])
def select_package():
    data = request.json
    user_id = data.get('user_id')  # User/session ID
    package = data.get('package')

    if package not in UC_PACKAGES:
        return jsonify({"status": "error", "message": "Invalid package."})

    user_sessions[user_id] = {"package": package}
    return jsonify({
        "status": "success",
        "message": f"You selected {package}. Please send your Game User ID next."
    })

@app.route('/submit_game_id', methods=['POST'])
def submit_game_id():
    data = request.json
    user_id = data.get('user_id')
    game_id = data.get('game_id')

    if user_id not in user_sessions:
        return jsonify({"status": "error", "message": "Please select a package first."})

    user_sessions[user_id]['game_id'] = game_id
    package = user_sessions[user_id]['package']
    amount = UC_PACKAGES[package]

    # Dummy QR code URL (use real UPI or payment gateway API for production)
    qr_code_url = "https://files.catbox.moe/r8u99g.jpg/?size=200x200&data=upi://pay?pa=example@upi&pn=UCStore&am=" + str(amount)

    return jsonify({
        "status": "success",
        "payment_details": {
            "UC Package": package,
            "Amount": f"₹{amount}",
            "Game ID": game_id,
            "QR Code URL": qr_code_url,
            "Instructions": "Scan this QR to pay. Then send a payment screenshot to verify."
        }
    })

if __name__ == '__main__':
    app.run(debug=True)