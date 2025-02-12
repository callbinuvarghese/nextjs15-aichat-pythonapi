#pip install fastapi uvicorn


from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from loguru import logger  
from typing import List, Dict, Any
import random
import asyncio
import os

from fastapi.middleware.cors import CORSMiddleware
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=openai.api_key)


app = FastAPI()

origins = [
    "http://localhost:3000",  # Your Next.js development URL
    "http://localhost", # if your nextjs is running on localhost
    "http://127.0.0.1:3000",   # Also include 127.0.0.1 if needed
    # Add other origins as needed (e.g., your production domain)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Important if you're using cookies or sessions
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


large_text_responses = [  # Your list of large texts
    "1. This is a very long text that will be streamed in chunks.  It's just an example, but you can put any large text here.  This text is designed to be longer than a single chunk so you can see the chunking in action.  It's important to have varied lengths of text for realistic testing.",
    "2. Another large text example.  This one is also quite long and will be streamed chunk by chunk.  The purpose is to demonstrate how the client can handle responses that are larger than a single chunk and reassemble them into a complete message.  This is crucial for handling responses from large language models.",
    "3. This is a third example of a large text.  It's important to have multiple examples so that you can test the streaming functionality with different content.  Varied text lengths and content help ensure that your client-side code is robust and can handle different scenarios.  This text, like the others, will be broken down into chunks and streamed to the client.",
    "4. Here's a fourth large text example.  This one is slightly different in structure and content to provide further testing variations.  When working with streaming data, it's essential to test with diverse data to uncover any potential edge cases or issues in your client-side code.  This text, along with the others, will be streamed chunk by chunk."
]

html_table = """
<table border="1">
    <tr>
        <th>Name</th>
        <th>Age</th>
        <th>City</th>
    </tr>
    <tr>
        <td>Alice</td>
        <td>25</td>
        <td>New York</td>
    </tr>
    <tr>
        <td>Bob</td>
        <td>30</td>
        <td>Los Angeles</td>
    </tr>
    <tr>
        <td>Charlie</td>
        <td>35</td>
        <td>Chicago</td>
    </tr>
</table>
"""

# Placeholder for your actual language model or processing logic
async def generate_text_stream_old(messages: List[Dict[str, Any]]):
    """
    This function simulates streaming text generation.  Replace it with your
    actual model or processing logic.
    """

    # Example 1: Simple chunking (replace with your model's output)
    #for chunk in ["This is ", "a ", "stream ", "of ", "text.\n"]:
    #    yield chunk
        # Simulate some processing time (optional)
        # await asyncio.sleep(0.5)  # If you need asynchronous operations

    # Example 2: Streaming from a large string (replace with your model's output)
    large_text = random.choice(large_text_responses)
    chunk_size = 10  # Adjust chunk size as needed
    for i in range(0, len(large_text), chunk_size):
         yield large_text[i:i + chunk_size]
         await asyncio.sleep(0.1)


# **Streaming text generation function**
async def generate_text_stream(messages: List[Dict[str, Any]]):
    """Generates text stream from OpenAI"""
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            stream=True,
        )
        
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:  # Check if content is not None
                yield content.encode("utf-8")
    except openai.OpenAIError as e:
        logger.error(f"OpenAI Error: {e}")
        yield f"Error: {e}\n".encode("utf-8")
    except Exception as e:
        logger.exception("Unexpected error during OpenAI API call")
        yield f"Error: Unexpected server issue\n".encode("utf-8")

@app.post("/chat/stream")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        messages = data.get("messages")

        if not messages:
            raise HTTPException(status_code=400, detail="Messages are required")

        #logger.debug(f"Received messages: {messages}") 

        # Print the received messages to the console
        print("Received messages:")
        for message in messages:
            #print(message)  # Print each message object
            logger.debug(f"Received messages: {messages}") 
        # Respond with a random message from the list
        #random_response = random.choice(large_text_responses)
        #return JSONResponse({"response": random_response})  # Return JSON response

        # async def generate_stream():
        #     async for chunk in generate_text_stream(messages):  # Use async generator
        #         #logger.debug(f"chunk {chunk}")
        #         yield chunk.encode("utf-8") # Important: Encode to bytes
        
        return StreamingResponse(generate_text_stream(messages), media_type="text/event-stream")

    except HTTPException as e:
        return {"error": e.detail}, e.status_code
    except Exception as e:
        print(f"An unexpected error occurred: {e}") # For debugging on server
        return {"error": "An internal server error occurred"}, 500


@app.post("/chat/html")  # Endpoint for single HTML response
async def chat_html_endpoint(request: Request):
    try:
        data = await request.json()
        messages: List[Dict[str, Any]] = data.get("messages")

        if not messages:
            raise HTTPException(status_code=400, detail="Messages are required")

        logger.info(f"Received messages for HTML: {messages}")

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
        )

        html_content = "".join(f"HTML:<p>{choice.message.content}</p>" for choice in response.choices)
        return HTMLResponse(content=html_content)

    except openai.OpenAIError as e:  # Corrected exception handling
        logger.error(f"OpenAI Error: {e}")
        return HTMLResponse(content=f"<p>Error: {e}</p>", status_code=500)
    except Exception as e:
        logger.exception("An unexpected error occurred during OpenAI API call")
        return HTMLResponse(content=f"<p>Error: An unexpected error occurred</p>", status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)  # Make accessible from network

