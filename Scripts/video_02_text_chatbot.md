# Video 2: Building Your First Text-Only Chatbot

## Introduction (1.5 min)

Hey everyone, and welcome back. In the last video, we got Datapizza-AI up and running and made our first LLM call. But let's be honest—it wasn't really a chatbot yet. It had no memory, no error handling, and none of the features you'd need to ship it to production.

Today, we're going to fix all of that. We're building a proper conversational chatbot that remembers your conversation history, handles errors gracefully, and even implements caching to help you save money.

[Visual: Show progression from basic invoke to full chatbot]

This is the foundation you'll need for everything else in this series. Once you understand memory, caching, and the response lifecycle, you'll be able to build anything.

Alright, let's dive into the three core concepts we'll be covering.

## Content Main (7 min)

### Understanding Memory (2.5 min)

Okay, so here's something that often trips people up: LLMs don't actually remember anything. At all. Every single time you send a request, you have to include the entire conversation history. That's just how these models work.

[Visual: Diagram showing stateless LLM receiving full context]

Datapizza-AI simplifies this with three key objects: `Memory`, `TextBlock`, and `ROLE`.

Let me show you how this works in practice:

```python
import os
from dotenv import load_dotenv
from datapizza.memory import Memory
from datapizza.clients.openai import OpenAIClient
from datapizza.type import ROLE, TextBlock

memory = Memory()
load_dotenv()

client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    system_prompt="You are a helpful assistant that can answer questions and help with tasks.",
)

message = TextBlock(content="What is capital of Italy?")

response = client.invoke(message.content, memory=memory)
print(response.text)

# Add the user message as a turn
memory.add_turn(message, ROLE.USER)

# Add the assistant response as a turn
memory.add_turn(
    TextBlock(content=response.text),
    ROLE.ASSISTANT,
)
message = TextBlock(content="What did I ask you before?")
memory.add_turn(message, ROLE.USER)
response = client.invoke(message.content, memory=memory)
print(response.text)
memory.add_turn(
    TextBlock(content=response.text), 
    ROLE.ASSISTANT
    )
```

[Show code running with output]

See what's happening here? We're manually tracking the conversation. When the user says something, we store it. When the model responds, we store that too.

And here's a critical point: always use `response.text` when storing the assistant's reply. Don't pass the entire response object directly, as it's not a string. Memory expects strings wrapped in a `TextBlock`.

[Highlight the .text property]

This pattern—add user turn, invoke with memory, add assistant turn—is how every chatbot in Datapizza-AI works. It's a fundamental concept to get comfortable with.

### Implementing Caching (2 min)

Now, let's talk about money for a second. Every time you hit an LLM API, you're paying for tokens. If someone asks the same question twice, you're literally paying twice for the exact same answer.

That's incredibly wasteful. Caching fixes this, and it's remarkably simple to implement.

[Show code]

```python
import time
from datapizza.clients.openai import OpenAIClient
from datapizza.cache import MemoryCache

client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    cache=MemoryCache()
)

# First request hits the API
t0 = time.perf_counter()
response1 = client.invoke("What is machine learning?")
t1 = time.perf_counter()
print("first:", response1.text)
print(f"⏱️ time (first): {t1 - t0:.3f}s")

# Second identical request hits the cache
t2 = time.perf_counter()
response2 = client.invoke("What is machine learning?")
t3 = time.perf_counter()
print("second:", response2.text)
print(f"⏱️ time (second): {t3 - t2:.3f}s")
```

[Demonstrate timing difference]

The first request might take two to three seconds, but the second one is instant. While we can't show the difference in cost directly, the second scenario has zero API cost.

The cache key is computed from your prompt and other parameters, so the same input will always result in the same cached output. A different input will trigger a fresh API call.

[Visual: Show cache hit vs cache miss flowchart]

For production environments, you'd typically use `RedisCache` instead of `MemoryCache` so that your cache persists across restarts and works in distributed systems. But for local development, `MemoryCache` is perfect. If you need more information about RedisCache please check the official documentation on datapizza-ai!

### Building the Complete Chatbot (2.5 min)

Now, let's put it all together into something you can actually use. We'll build it line by line.

[Show full code]

```python
import os
from datapizza.clients.openai import OpenAIClient
from datapizza.memory import Memory
from datapizza.type import ROLE, TextBlock

class Chatbot:
    def __init__(self, client):
        self.client = client
        self.memory = Memory()
    
    def send(self, user_input: str) -> str:
        # Store user message
        self.memory.add_turn(
            [TextBlock(content=user_input)], 
            ROLE.USER
        )
        
        # Get response with memory
        response = self.client.invoke(user_input, memory=self.memory)
        
        # Store assistant response
        self.memory.add_turn(
            [TextBlock(content=response.text)], 
            ROLE.ASSISTANT
        )
        
        # Show token usage
        total = (response.prompt_tokens_used or 0) + 
                (response.completion_tokens_used or 0)
        print(f"[tokens: {total}]")
        
        return response.text

client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o"
)

bot = Chatbot(client)

# Simple chat loop
while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        break
    print("Bot:", bot.send(user_input))
```

[Run the chatbot, show conversation]

Look at what we have now: a complete chatbot with proper memory management, token tracking, and a clean, reusable interface.

The chatbot now remembers context across multiple turns. If you introduce yourself and then ask, "What's my name?", it'll remember.

[Demonstrate this in the running chatbot]

We're also tracking tokens with every response, so you know exactly what you're spending. In a production environment, you would log this to your monitoring system.

And notice the error handling—we're catching exceptions in a `try-except` block to gracefully handle any API failures.

## Conclusion (1.5 min)

Alright, let's wrap this up. Here's what we just built.

We added proper conversation memory using `Memory`, `TextBlock`, and `ROLE`. We implemented caching to eliminate redundant API calls and save you money. And we built a complete chatbot class that handles the entire conversation lifecycle.

[Visual: Show three key components]

This is your new chatbot foundation. Everything from here on out—tools, agents, and RAG systems—will build on this exact pattern.

In the next video, we'll explore structured outputs so you can get reliable JSON responses, and we'll dive into multimodal capabilities, like sending images and audio to your models. Things are about to get much more interesting.

Before that, though, try extending this chatbot. Add a system prompt, experiment with different temperatures, or swap OpenAI for Claude or Gemini using the same code—all you have to do is install a different client. That's the power of this unified interface. So far, we've only dealt with text-based chatbots, but in the next video, we'll dive into structured and multimodal content.

If this was helpful, smash that like button and drop a comment if you run into any issues. I'll see you in the next one!

