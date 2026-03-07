import os
from pathlib import Path
from dotenv import load_dotenv

# Explicitly load .env from the project root regardless of where the script is run from
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

class Settings:
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USER = os.getenv("NEO4J_USERNAME")  # Fixed: was "NEO4J_USER", .env uses "NEO4J_USERNAME"
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

settings = Settings()