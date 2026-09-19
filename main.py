from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# model instructions
instructions = """
You are a customer service assistant for a fictional appointment booking system.

Use the provided tools to help customers look up their customer
records and appointment availability.

Customer records returned by customer_lookup are fictional test
data provided by this application.

When a tool returns customer information, use the returned
information to answer the user's request.
"""

# customer data
customers = {
    "555-123-4567": {
        "customer_id": "cust_001",
        "name": "John Doe"
    },
    "555-987-6543": {
        "customer_id": "cust_002",
        "name": "Jane Smith"
    }
}

# Mock slots data
appointments = {
        "09/11/2026": ["10:00am","12:00pm","01:00pm"],
        "09/12/2026": ["10:00am","12:00pm","01:00pm"],
        "09/13/2026": ["10:00am","12:00pm","01:00pm"],
    }

# tools
## get availability
def get_available_appointments(date):
    return {
        "date": date,
        "available_appointments": appointments.get(date, [])
    }

## search customer
def customer_lookup(phone):
    return customers.get(phone, [])

## Creating bookings and manage booking list
bookings = []

def book_appointment(customer_id, date, time):
    

    available_times = appointments.get(date, [])

    if time in available_times:
        booking = {
            "customer_id": customer_id,
            "date": date,
            "time": time
        }

        bookings.append(booking)

        return booking

    else:
        return { "error": "Requested appointment time is not available." }

    

    


# tool dictionary
tools_library = {
    "get_available_appointments": get_available_appointments,
    "customer_lookup": customer_lookup,
    "book_appointment": book_appointment
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
    },
    {
        "name": "customer_lookup",
        "type": "function",
        "description": "Look up a customer record in the local customer database using their phone number.",
        "parameters": {
            "type": "object",
            "properties": {
                "phone": {
                    "type": "string",
                    "description": "Customer phone number used to search the local customer database."
                }
            },
        "required": ["phone"]
        }
    },
    {
        "name": "book_appointment",
        "type": "function",
        "description": "Create an appointment booking for a customer using their customer ID, date, and time.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Customer id to reference for booking creation."
                },
                "date": {
                    "type": "string",
                    "description": "Customer desired date for their appointment booking."
                },
                "time": {
                    "type": "string",
                    "description": "Customer desired time for their appointment booking."
                }
            },
        "required": ["customer_id","date", "time"]
        }
    }
]


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
                instructions= instructions,
                input = tool_call_outputs,
                tools=tool_schema
            )

            print(response.output)
            
        else:
            break

        

    print(response.output_text)

    print(
        book_appointment(
            customer_id="cust_001",
            date="09/12/2026",
            time="3:00pm"
        )
    )

    print(bookings)

