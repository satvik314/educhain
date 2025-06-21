from educhain import Educhain, LLMConfig
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import dotenv
dotenv.load_dotenv()

def client_model():
    GOOGLE_API_KEY = os.getenv("GEMINI_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_flash = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GOOGLE_API_KEY
    )
    flash_config = LLMConfig(custom_model=gemini_flash)
    return Educhain(flash_config)