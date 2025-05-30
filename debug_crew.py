"""
Debug script to test CrewAI components step by step.
"""
import os
from dotenv import load_dotenv

def test_crew_components():
    """Test each CrewAI component to find the issue."""
    load_dotenv()
    
    print("🔍 Testing CrewAI components step by step...")
    
    try:
        # Test 1: Import CrewAI
        from crewai import Agent, Task, Crew
        print("✅ CrewAI imports successful")
        
        # Test 2: Import LLM
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.1
        )
        print("✅ LLM configuration successful")
        
        # Test 3: Import tools
        from tools.solar_tools import read_current_ac_measurements
        print("✅ Solar tools import successful")
        
        # Test 4: Create a simple agent
        test_agent = Agent(
            role="Test Agent",
            goal="Test basic functionality",
            backstory="I am a test agent",
            tools=[read_current_ac_measurements],
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        print("✅ Agent creation successful")
        
        # Test 5: Create a simple task
        test_task = Task(
            description="Test task: call the read_current_ac_measurements tool",
            expected_output="A string with AC measurements",
            agent=test_agent
        )
        print("✅ Task creation successful")
        
        # Test 6: Create a simple crew
        test_crew = Crew(
            agents=[test_agent],
            tasks=[test_task],
            verbose=True
        )
        print("✅ Crew creation successful")
        
        # Test 7: Run the crew
        print("🚀 Testing crew execution...")
        result = test_crew.kickoff()
        print(f"✅ Crew execution successful: {result}")
        
    except Exception as e:
        print(f"❌ Error at step: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_crew_components() 