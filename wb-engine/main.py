import asyncio
import io
from flask import Flask, request, jsonify, send_file
from telethon import TelegramClient
from telethon.sessions import StringSession
from keys import Keys
from format import Formatter
from token_maker import TokenMaker

app = Flask(__name__)
client = TelegramClient(StringSession(Keys.get_session()), Keys.API_ID, Keys.API_HASH)

@app.route('/api/v1/get', methods=['GET'])
async def handle_get():
    p_name = request.args.get("project")
    p_token = request.args.get("token")
    mode = request.args.get("mode")
    target = request.args.get("target")

    async with client:
        search_query = f"project: {p_name}"
        async for msg in client.iter_messages(Keys.BOX_ID, search=search_query):
            if f"token: {p_token}" not in msg.message:
                continue
            
            if mode == 'gv' and f"{target}:" in msg.message:
                value = msg.message.split(f"{target}:")[1].split('\n')[0].strip()
                return jsonify({"status": "found", "value": value})
            
            elif mode == 'file' and f"file: {target}" in msg.message:
                data = await client.download_media(msg, file=io.BytesIO())
                data.seek(0)
                return send_file(data, download_name=target, as_attachment=True)
                
    return jsonify({"status": "error", "msg": "NOT_FOUND"}), 404

@app.route('/api/v1/put', methods=['POST'])
async def handle_put():
    p_name = request.form.get("project")
    p_token = request.form.get("token")
    mode = request.form.get("mode")

    async with client:
        if mode == 'gv':
            v_name = request.form.get("name")
            v_val = request.form.get("value")
            caption = Formatter.global_var_style(p_name, p_token, v_name, v_val)
            await client.send_message(Keys.BOX_ID, caption)
        
        elif mode == 'file':
            file = request.files.get("file")
            caption = Formatter.file_style(p_name, p_token, file.filename)
            await client.send_file(Keys.BOX_ID, file, caption=caption)

    return jsonify({"status": "success", "project": p_name})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
