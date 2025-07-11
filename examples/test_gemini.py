import os
from dotenv import load_dotenv # type: ignore [import-untyped]
import google.generativeai as genai # type: ignore [import-untyped]

# Load environment variables
load_dotenv()

# Configure the library
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Test a simple generation
model = genai.GenerativeModel('gemini-2.5-pro')
response = model.generate_content('Write a hello world message')
print("\nTest Response:")
print(response.text) 