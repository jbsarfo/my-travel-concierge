import os
from google import adk
from pydantic import BaseModel, Field
from typing import List

# ==========================================
# RUBRIC 1: TOOL & INTERFACE DESIGN
# ==========================================

class TravelQuery(BaseModel):
    destination: str = Field(description="The city or country the user wants to visit.")
    budget: float = Field(description="Total budget for the trip in USD.")
    days: int = Field(description="Duration of the trip in days.")

def search_hotel_inventory(query: TravelQuery) -> dict:
    """
    Searches available hotels based on destination and budget constraints.

    Args:
        query (TravelQuery): The destination, budget, and duration.

    Returns:
        dict: A dictionary with 'status' and a list of 'hotels'.
    """
    try:
        # Mock logic (Replace this with real API calls later if desired)
        if query.budget < 500:
             return {"status": "success", "hotels": ["Backpacker Hostel", "Budget Inn"]}
        return {"status": "success", "hotels": ["Grand Hyatt", "Marriott Resort"]}
    
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Hotel search failed: {str(e)}. Please check destination spelling or increase budget."
        }

# ==========================================
# RUBRIC 2: CONTEXT & MEMORY
# ==========================================

SYSTEM_INSTRUCTION = """
You are a helpful, professional Personal Travel Concierge agent.
Your goal is to help users plan their dream vacations while staying within their budget.

Constraints:
- You MUST use the `search_hotel_inventory` tool to verify hotel availability before recommending them.
- Always ask for the budget if the user hasn't provided it.
- Maintain a friendly, enthusiastic, yet realistic tone about costs.
"""

root_agent = adk.Agent(
    model="gemini-2.5-flash", 
    name="travel_concierge_agent",
    instruction=SYSTEM_INSTRUCTION,
    tools=[search_hotel_inventory]
)
