import google.generativeai as genai
from keys import GEMINI_KEY

try:
    genai.configure(api_key=GEMINI_KEY)
    print(f"Checking models for key: {GEMINI_KEY[:5]}...")
    
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            print(f"- {m.name}")
            
    if not available_models:
        print("No models found that support 'generateContent'. Check if the API is enabled in Google Cloud Console.")
except Exception as e:
    print(f"Error: {e}")
