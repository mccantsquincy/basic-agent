from openai import OpenAI
from dotenv import load_dotenv
from agent.runner import run_agent
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# OPENAI API request with input
if __name__ == "__main__":
    user_input="""
    My phone number is 555-123-4567.
    Can you book me for 3:00pm on 09/12/2026?
    """
    result = run_agent(client, user_input)
    print(result)


    

