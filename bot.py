import logging
import json
import os
from telethon import TelegramClient, events, Button

# --- الإعدادات ---
API_ID = 32452150 
API_HASH = '30958ffad5c668399d03c26aa16fee03'
BOT_TOKEN = '8772686278:AAH0yh8erFNRcoYU37fu90_B4lzZh5ueImo'
DB_FILE = 'database.json'

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# دالة لتحميل البيانات من الملف
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {}

# دالة لحفظ البيانات في الملف
def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f)

users = load_db()

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    uid = str(event.sender_id) # تحويل لـ string للحفظ بـ JSON
    if len(event.message.text.split()) > 1:
        ref = event.message.text.split()[1]
        if ref != uid and uid not in users:
            users[ref] = users.get(ref, 0) + 10
            save_db(users)
            try:
                await client.send_message(int(ref), "✅ حصلت على 10 نقاط لدعوة شخص جديد!")
            except: pass

    if uid not in users: 
        users[uid] = 0
        save_db(users)
    
    btns = [[Button.inline("➕ تجميع نقاط", b"p"), Button.inline("🚀 طلب تمويل", b"o")],
            [Button.inline("👤 حسابي", b"m"), Button.inline("🔗 رابط الدعوة", b"l")],
            [Button.url("📢 القناة", "https://t.me/POVlLV")],
            [Button.url("🛠️ المطور", "https://t.me/tm_qe")]]
    
    await event.respond(f"**🚀 بوت تمويل سوران (دائمي)**\n💰 نقاطك: {users[uid]}", buttons=btns)

@client.on(events.CallbackQuery())
async def callback(event):
    u = str(event.sender_id)
    if event.data == b"l":
        me = await client.get_me()
        await event.edit(f"🔗 رابط دعوتك:\n`https://t.me/{me.username}?start={u}`")
    elif event.data == b"p":
        await event.edit("💡 شارك رابطك لجمع النقاط.")
    elif event.data == b"m":
        await event.edit(f"👤 رصيدك الحالي: {users.get(u, 0)} نقطة.")
    elif event.data == b"o":
        await event.edit("🚀 تواصل مع المطور لطلب التمويل: @tm_qe")

print("✅ البوت شغال بنظام الحفظ الدائم...")
client.run_until_disconnected()
