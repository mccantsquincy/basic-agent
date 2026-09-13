from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# tools
def get_available_appointments(date):
    appointments = {
        "09/11/2026": ["10:00am","12:00pm","01:00pm"],
        "09/12/2026": ["10:00am","12:00pm","01:00pm"],
        "09/13/2026": ["10:00am","12:00pm","01:00pm"],
    }

    return {
        "date": date,
        "available_appointments": appointments.get(date, [])
    }

# tool dictionary
tools_library = {
    "get_available_appointments": get_available_appointments
}

# tool schema
tool_schema = [
    {
        "name": "get_available_appointments",
        "type": "function",
        "description": "Get available appointment slots for a given date.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date in MM/DD/YYYY format"
                }
            },
        "required": ["date"]
        }
    }
]


response = client.responses.create(
    model="gpt-4o-mini",
    input="What appointments are available on 09/12/2026?",
    tools = tool_schema
)

tool_call = response.output[0]
args = json.loads(tool_call.arguments)
function = tools_library.get(tool_call.name)
result = function(**args)


print(result)

