from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import List

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class Quiz(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

agent = Agent(
    name="Quiz Agent",
    instructions="You are a helpful assistant that can answer questions and help with tasks.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client, ),
    output_type=Quiz 
)

query = input("Enter a query: ")

result = Runner.run_sync(agent, query)

print(result.final_output)
