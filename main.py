import os
import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
from flask import Flask
from threading import Thread

# -------------------------
# 🌐 Flask (keep alive)
# -------------------------
app = Flask("")

@app.route("/")
def home():
    return "Bot is alive"

def run_web():
    app.run(host="0.0.0.0", port=8010)

Thread(target=run_web).start()

# -------------------------
# 🤖 Discord Bot
# -------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------------
# 🗄 SQLite DB
# -------------------------
db = sqlite3.connect("swearword.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS swearword (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    content TEXT
)
""")
db.commit()

# -------------------------
# ⚙️ 설정
# -------------------------
filter_on = False

swear_list = [
    "ㅅㅂ","시바","ㅆ","ㅁㅊ놈","미친놈","ㄸㄱ리",
    "따가리","ㄱㅅㄲ","개새끼","좆","ㅈㄱ","Ugliness"
]

# -------------------------
# 🚀 ready
# -------------------------
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("봇 실행됨")

# -------------------------
# /setup
# -------------------------
@bot.tree.command(name="setup")
async def setup(interaction: discord.Interaction):
    global filter_on
    filter_on = True
    await interaction.response.send_message("채팅 감시 ON")

# -------------------------
# /secustart
# -------------------------
@bot.tree.command(name="secustart")
async def secustart(interaction: discord.Interaction):
    global filter_on
    filter_on = True
    await interaction.response.send_message("욕설 감지 ON")

# -------------------------
# 💬 message detect
# -------------------------
@bot.event
async def on_message(message):
    global filter_on

    if message.author.bot:
        return

    if filter_on:
        for word in swear_list:
            if word in message.content:
                cursor.execute(
                    "INSERT INTO swearword (username, content) VALUES (?, ?)",
                    (str(message.author), message.content)
                )
                db.commit()
                break

    await bot.process_commands(message)

# -------------------------
# ▶ RUN (ENV TOKEN)
# -------------------------
bot.run(os.getenv("TOKEN"))
