from dotenv import load_dotenv
import os

load_dotenv()

model = os.getenv("GEMINI_API_MODEL_FLASH")
# model = os.getenv("GEMINI_API_MODEL_LITE")
temprature = 0.7
