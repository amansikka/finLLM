from text import main
from text import return_query
from dotenv import load_dotenv
import os
import anthropic
client = anthropic.Client(api_key="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")

context = main()
query = return_query()
result = query + " here is the given context for the prompt: " + context


response = client.messages.create(
    model="claude-3-sonnet-20240229",
    system="You are an expert investment banker who answers questions in a thoughtful step by step manner", 
    messages=[
        {"role": "user", "content": result} 
    ],
    max_tokens=4000
)

print(response.content[0].text)





