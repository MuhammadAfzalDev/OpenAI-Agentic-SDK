import os
import chainlit as cl
from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Set Provider 

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    
)

# Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client = provider,
    )

# Config : Config defined at Run level
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

agent1 = Agent(
    instructions= " you are a helpful assistant that answers questions and ",
    name="Faizi RAG Based Agent"
)

result = Runner.run_sync(
    agent1,
    input="what is the capital of Pakistan",
    run_config=config,
    
)

print(result.final_output)

# @cl.on_message
# async def handle_message(message: cl.Message):
   
#     await cl.Message(content=f"Hello: {message.content}" ).send()