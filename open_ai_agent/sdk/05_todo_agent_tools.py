import json
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

@function_tool
def list_todos():
    """ List all todo from todo.json file."""
    try:
        print("Listing all todos...")
        with open('todo.json', 'r') as file:
            todos = json.load(file)
        return todos
    except Exception as e:
        print(f"Error listing todos: {e}")
        raise FileNotFoundError("todo.json file not found or is not readable.")

import json
from typing import Dict, Any
from datetime import datetime

@function_tool
def add_todo(title:str, description:str = "", due_date:str ="") -> Dict[str, Any]:
    """add a todo to todo.json file.
    Args:
        title (str): The title of the todo.
        description (str): The description of the todo.
        due_date (str): The due date of the todo in YYYY-MM-DD format. This can be opetional.
    Returns:
            the newly create item title.
        """
    try:
        try:
            with open('todo.json', 'r') as file:
                todos = json.load(file)
        except FileNotFoundError:
            todos = []
        except json.JSONDecodeError:
            raise ValueError("todo.json file is not a valid JSON format.")
        
        # Create a new todo item
        new_todo = {
            "id": len(todos) + 1,
            "title": title,
            "description": description,
            "completed": False,
            "due_date": due_date if due_date else datetime.now().strptime("%Y-%m-%d"),
        }

        # append and save 
        todos.append(new_todo)
        with open('todo.json', 'w') as file:
            json.dump(todos, file, indent=2)
        print(f"Todo '{title}' added successfully.")
        return new_todo
    except Exception as e:
        print(f"Error adding todo: {e}")
        raise Exception("An error occurred while adding the todo item.")

agent = Agent(
    name="Todo Assistant",
    instructions="You are an expert in managing todos. You can list all todos, add a new todo, and mark a todo as completed.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[list_todos, add_todo],
)

query = input("Enter the query: ")
result = Runner.run_sync(
    agent,
    query,
)

print(result.final_output)
            
