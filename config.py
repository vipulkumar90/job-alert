from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")