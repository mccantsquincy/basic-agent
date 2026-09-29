from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from tools.appointments import get_available_appointments, book_appointment, bookings
from tools.customers import customer_lookup
from tools.schemas import tool_schema
from agent.instructions import instructions

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# OPENAI API request with input
if __name__ == "__main__":
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=instructions,
        input="""
    My phone number is 555-123-4567.
    Can you book me for 3:00pm on 09/12/2026?
    """,
        tools = tool_schema
    )


    print(response.output)


    

