"""
Debug script to test the exact LLM error.
"""
import os
from dotenv import load_dotenv

def test_simple_llm():
    """Test basic LLM functionality to see actual error."""
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"API Key present: {'Yes' if api_key else 'No'}")
    
    if api_key:
        print(f"API Key starts with: {api_key[:10]}...")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ langchain_google_genai imported successfully")
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=api_key,
            temperature=0.1
        )
        print("✅ LLM initialized successfully")
        
        response = llm.invoke("Say 'Hello World'")
        print(f"✅ LLM response: {response.content}")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_llm() 