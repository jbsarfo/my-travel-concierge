import asyncio
from google.adk import Runner
from google.genai import types
from agent import root_agent

async def main():
    # In-memory session for local testing
    runner = Runner(agent=root_agent, app_name="travel_concierge_app")
    
    # Send a test query
    query = "I want to visit Tokyo for 5 days. My budget is $1000."
    content = types.Content(role='user', parts=[types.Part(text=query)])
    
    print(f"User: {query}\n---")
    
    async for event in runner.run_async(
        user_id="test_user", 
        session_id="session_001", 
        new_message=content
    ):
        if event.is_final_response():
            print(f"Agent: {event.content.parts[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
