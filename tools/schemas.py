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
