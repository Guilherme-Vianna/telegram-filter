import os
import logging
from telethon import TelegramClient, events
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dotenv import load_dotenv

# =====================
# Logging (Docker friendly)
# =====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("telegram-bot")

# =====================
# Env
# =====================
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME", "sessao")
mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")

logger.info("Starting bot...")

# =====================
# Telegram
# =====================
client = TelegramClient(session_name, api_id, api_hash)

# =====================
# Mongo
# =====================
mongo_client = AsyncIOMotorClient(mongo_url)
db = mongo_client["telegram"]
collection = db["mensagens"]

logger.info("Connected to MongoDB")

# =====================
# Handler
# =====================
@client.on(events.NewMessage)
async def handler(event):
    if event.out:
        return

    if event.text:
        doc = {
            "mensagem": event.text,
            "data_recebida": datetime.utcnow()
        }

        try:
            await collection.insert_one(doc)
            logger.info(f"Message saved: {event.text[:80]}")
        except Exception as e:
            logger.error(f"Error saving message: {e}", exc_info=True)

# =====================
# Run
# =====================
client.start()
logger.info("Bot running. Waiting for messages...")
client.run_until_disconnected()
