"""
Simple test to check if CrewAI works with default configuration.
"""
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

def test_simple_crew():
    """Test CrewAI with minimal configuration."""
    load_dotenv()
    
    print("🧪 Testing CrewAI with default LLM configuration...")
    
    try:
        # Create a simple agent without custom LLM
        agent = Agent(
            role="Test Agent",
            goal="Answer simple questions",
            backstory="I am a test agent",
            verbose=True
        )
        print("✅ Agent created successfully")
        
        # Create a simple task
        task = Task(
            description="Say hello and explain what you do",
            expected_output="A greeting and brief explanation",
            agent=agent
        )
        print("✅ Task created successfully")
        
        # Create crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        print("✅ Crew created successfully")
        
        # Run crew
        print("🚀 Running crew...")
        result = crew.kickoff()
        print(f"✅ Success: {result}")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_crew() 