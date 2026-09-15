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

# OPENAI API request with input
response = client.responses.create(
    model="gpt-4o-mini",
    input="What appointments are available on 09/12/2026?",
    tools = tool_schema
)

while True:

    tool_call_outputs = []

    for item in response.output:

        if item.type == "function_call":

            tool_call = item
            tool_name = tool_call.name
            args = json.loads(tool_call.arguments)

            function = tools_library.get(tool_name)

            if function:
                try:
                    result = function(**args)
                except Exception as error:
                    result = {
                        "error": str(error)
                    }
            else:
                result = {
                    "error": f"Tool {tool_name} not found"
                }

            # Tool outputs appending to tool call outputs list
            tool_call_outputs.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(result)
            })



    if tool_call_outputs:

        response = client.responses.create(
            model = "gpt-4o-mini",
            previous_response_id = response.id,
            input = tool_call_outputs
        )
        
    else:
        break

    

print(response.output_text)

