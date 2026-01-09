import os
import sys
from dotenv import load_dotenv

# Add project root to path for imports
sys.path.insert(0, os.path.abspath("."))

# Load environment variables
load_dotenv()

# Import settings and key loader
from app.config.settings import settings
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

# --- Test ---
try:
    from google import genai
    print("Attempting to initialize Gemini Client...")
    
    # This call will fail if the key is invalid
    client = genai.Client(api_key=GEMINI_KEY)
    
    # If initialization succeeds, try a simple, cheap model list check
    models = client.models.list()
    print("\n✅ SUCCESS! Your Gemini API Key is working.")
    print(f"   Key successfully initialized {len(models)} models.")
    
except Exception as e:
    print(f"\n❌ FAILURE: Gemini Key Test Failed.")
    print(f"   Error details: {e}")
    print("   Please verify the key in your .env file is correct and active.")
