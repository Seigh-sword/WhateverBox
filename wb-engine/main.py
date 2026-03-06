import asyncio
import io
import time
from flask import Flask, request, jsonify, send_file
from telethon import TelegramClient
from telethon.sessions import StringSession
from keys import Keys
from format import Formatter

app = Flask(__name__)
client = TelegramClient(StringSession(Keys.get_session()), Keys.API_ID, Keys.API_HASH)

usage_history = {}

def is_spaming(token):
    now = time.time()
    if token not in usage_history:
        usage_history[token] = []
    
    usage_history[token] = [t for t in usage_history[token] if now - t < 60]
    
    if len(usage_history[token]) > 10:
        return True
    
    usage_history[token].append(now)
    return False

@app.route('/api/v1/put', methods=['POST'])
async def handle_put():
    p_name = request.form.get("project")
    p_token = request.form.get("token")
    mode = request.form.get("mode")

    if is_spaming(p_token):
        return jsonify({"status": "error", "msg": "SLOW_DOWN_SPAMMER"}), 429

    async with client:
        if mode == 'gv':
            v_name = request.form.get("name")
            v_val = request.form.get("value")
            
            async for msg in client.iter_messages(Keys.BOX_ID, search=f"project: {p_name}"):
                if f"token: {p_token}" in msg.message and f"{v_name}:" in msg.message:
                    await msg.delete()
            
            caption = Formatter.global_var_style(p_name, p_token, v_name, v_val)
            await client.send_message(Keys.BOX_ID, caption)
        
        elif mode == 'file':
            file = request.files.get("file")
            f_name_clean = file.filename.rsplit('.', 1)[0]
            
            async for msg in client.iter_messages(Keys.BOX_ID, search=f"project: {p_name}"):
                if f"token: {p_token}" in msg.message and f"file: {f_name_clean}" in msg.message:
                    await msg.delete()

            caption = Formatter.file_style(p_name, p_token, file.filename)
            await client.send_file(Keys.BOX_ID, file, caption=caption)

    return jsonify({"status": "success", "project": p_name})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
