import asyncio
from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.sessions import StringSession

from keys import Keys
from format import Formatter
from token_maker import TokenMaker

app = Flask(__name__)

client = TelegramClient(StringSession(Keys.get_session()), Keys.API_ID, Keys.API_HASH)

@app.route('/api/v1/create-project', methods=['POST'])
async def create_project():
    data = request.json
    p_name = data.get("project")
    is_private = data.get("private", True)

    if not p_name:
        return jsonify({"status": "error", "msg": "PROJECT_NAME_REQUIRED"}), 400

    token = TokenMaker.generate_private() if is_private else TokenMaker.generate_public()
    p_type = "Private" if is_private else "Public"

    registration_text = Formatter.token_registration_style(p_name, token, p_type)

    async with client:
        await client.send_message(Keys.BOX_ID, registration_text)

    return jsonify({
        "status": "created",
        "project": p_name,
        "token": token
    })

@app.route('/api/v1/push', methods=['POST'])
async def handle_push():
    p_name = request.form.get("project")
    p_token = request.form.get("token")
    mode = request.form.get("mode") # 'var' or 'file'

    if not p_name or not p_token:
        return jsonify({"status": "error", "msg": "AUTH_REQUIRED"}), 401

    async with client:
        if mode == 'var':
            v_name = request.form.get("name")
            v_val = request.form.get("value")
            caption = Formatter.global_var_style(p_name, p_token, v_name, v_val)
            await client.send_message(Keys.BOX_ID, caption)
        
        elif mode == 'file':
            file = request.files.get("file")
            if not file:
                return jsonify({"status": "error", "msg": "NO_FILE"}), 400
            
            caption = Formatter.file_style(p_name, p_token, file.filename)
            await client.send_file(Keys.BOX_ID, file, caption=caption)

    return jsonify({"status": "success", "project": p_name})

@app.route('/api/v1/nuke', methods=['DELETE'])
async def handle_nuke():
    data = request.json
    p_name = data.get("project")
    p_token = data.get("token")

    async with client:
        count = 0
        async for msg in client.iter_messages(Keys.BOX_ID, search=f"project: {p_name}"):
            if f"token: {p_token}" in msg.message:
                await msg.delete()
                count += 1
    
    return jsonify({"status": "nuked", "cleaned_messages": count})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
