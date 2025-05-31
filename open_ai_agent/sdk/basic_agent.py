from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

agent = Agent(
    name="Gemini Agent",
    instructions="You are a helpful assistant that can answer questions and help with tasks.",
        model=OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=client,
        )
    )

query = input("Enter a query: ")

result = Runner.run_sync(agent, query)

print(result.final_output)

