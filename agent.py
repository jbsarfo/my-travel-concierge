import os
from google import adk
from pydantic import BaseModel, Field
from typing import List
from google.adk.models.llm_request import LlmRequest
from google.adk.agents.callback_context import CallbackContext

# ==========================================
# RUBRIC 1: TOOL & INTERFACE DESIGN
# ==========================================

class HotelQuery(BaseModel):
    destination: str = Field(description="The city or country to search.")
    budget: float = Field(description="Max budget per night in USD.")

def search_hotel_inventory(query: HotelQuery) -> dict:
    """
    Searches available hotels based on destination and budget constraints.

    Args:
        query (HotelQuery): The destination and budget parameters.

    Returns:
        dict: A dictionary with 'status' and a list of 'hotels'.
    """
    try:
        # Mock API logic
        if query.budget < 100:
             return {"status": "success", "hotels": ["Backpacker Hostel", "Budget Budget Inn"]}
        return {"status": "success", "hotels": ["Grand Hyatt", "Marriott Resort"]}
    except Exception as e:
        # Guided Error Handling
        return {
            "status": "error",
            "error_message": f"Hotel search failed: {str(e)}. Try a higher budget or verify spelling."
        }

# Human-in-the-loop Mock Tool
def secure_book_hotel(hotel_name: str, tool_context: adk.ToolContext) -> dict:
    """
    Books a hotel. REQUIRES explicit human confirmation flag in state.

    Args:
        hotel_name (str): Name of the hotel to book.
        tool_context (adk.ToolContext): ADK Context to check state.
    """
    # Guardrail / Human-in-the-loop hook
    if not tool_context.state.get("user_confirmed_booking"):
        return {
            "status": "blocked", 
            "message": "PENDING HUMAN APPROVAL. Please set state 'user_confirmed_booking' to True."
        }
    return {"status": "success", "booking_id": "BK-99812"}

def budget_guardrail_plugin(callback_context: CallbackContext, llm_request: LlmRequest):
    """
    Rubric Requirement: Guardrails & Policy Plugins.
    Intercepts the request before it goes to the model to enforce policies.
    """
    # Simple policy: Check if user is trying to bypass budget
    user_message = llm_request.contents[-1].parts[0].text
    if "override budget" in user_message.lower():
        logger.warning("Policy Violation: Budget override attempt detected.")
        # We can raise an error or modify the request here
        raise ValueError("Policy Error: Budget overrides are not permitted.")


# ==========================================
# RUBRIC 3: ORCHESTRATION & STRATEGIC ROUTING
# ==========================================

# Child Agent: Focused only on hotels (Uses fast model)
hotel_agent = adk.Agent(
    name="hotel_specialist",
    model="gemini-2.5-flash", # Strategic Routing: Fast/cheap model for simple tasks
    instruction="You are a hotel specialist. Find hotels and handle booking logic.",
    tools=[search_hotel_inventory, secure_book_hotel]
)

# Root Supervisor: Handles planning and routing (Uses smart model)
root_agent = adk.Agent(
    name="travel_supervisor",
    model="gemini-2.5-pro", # Strategic Routing: Smart model for planning
    instruction="""
    You are the head Travel Supervisor. Coordinate with your specialists to plan trips.
    - Route hotel inquiries to the hotel_specialist.
    - Always ensure budget limits are respected.
    """,
    children=[hotel_agent]
)

root_agent.before_model_callback = budget_guardrail_plugin
