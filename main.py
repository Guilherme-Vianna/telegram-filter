import os
from telethon import TelegramClient, events
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dotenv import load_dotenv

# Carrega .env
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME", "sessao")
mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")

# Telegram
client = TelegramClient(session_name, api_id, api_hash)

# MongoDB
mongo_client = AsyncIOMotorClient(mongo_url)
db = mongo_client["telegram"]
collection = db["mensagens"]

@client.on(events.NewMessage)
async def handler(event):
    if event.out:
        return

    if event.text:
        doc = {
            "mensagem": event.text,
            "data_recebida": datetime.utcnow()
        }

        await collection.insert_one(doc)
        print("Salvo:", event.text)

client.start()
print("Bot rodando...")
client.run_until_disconnected()
