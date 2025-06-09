
import json
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner,function_tool
import os
from dotenv import load_dotenv


load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

@function_tool
def calculate_bill(unit:float) -> float:
    """ Calculate the bill based on the number of units consumed.
    Args:
         The number of units consumed.

    Returns:
            The total bill amount.
    """
    try:
        print(f"Calculating bill for {unit} units..." )
        rate_per_unit = 9.980
        total_bill = unit * rate_per_unit
        return total_bill
    except Exception as e:
        raise ValueError(f"Error calculating bill: {str(e)}")
    

agent = Agent(
    name="Bill Calculator Assistant",
    instructions="You are an expert of bills. You will be provided with the number of units consumed, and you will calculate the total bill amount.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[calculate_bill],
)

query = input("Enter the query: ")

result = Runner.run_sync(
    agent,
    query,
)

print(result.final_output)