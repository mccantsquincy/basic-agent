from tools.schemas import tool_schema
from agent.instructions import instructions
from tools.registry import tools_library

import json


def run_agent(client, user_input):
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=instructions,
        input=user_input,
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
                instructions= instructions,
                input = tool_call_outputs,
                tools=tool_schema
            )
            
        else:
            break

    return (response.output_text)
