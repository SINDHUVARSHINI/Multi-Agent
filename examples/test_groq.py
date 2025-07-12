import os
from groq import Groq # type: ignore [reportMissingImports]
from dotenv import load_dotenv # type: ignore [reportMissingImports]

# Load environment variables
load_dotenv()

def test_groq_connection():
    """Test Groq API connection and basic functionality"""
    try:
        # Initialize Groq client
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        # Test API with a simple completion
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Updated to available model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello World!'"}
            ],
            max_tokens=10
        )
        
        print("API Connection Successful!")
        print("Response:", response.choices[0].message.content)
        return True
        
    except Exception as e:
        print("Error connecting to Groq API:")
        print(e)
        return False

if __name__ == "__main__":
    test_groq_connection() 