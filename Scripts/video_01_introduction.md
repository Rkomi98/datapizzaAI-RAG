# Video 1: Introduction to Datapizza-AI

## Introduction (2 min)

Hey everyone, and welcome to the complete guide to the Datapizza-AI framework. I'm Mirko Calcaterra, an AI engineer at Datapizza, and in this series, we'll show you how to build production-ready AI applications from the ground up.

If you've been trying to build with LLMs, you've likely found yourself wrestling with inconsistent APIs, debugging mysterious errors, or wondering how to ship something that won't break in production. If so, you're in the right place.

[Visual: Show messy code snippets transforming into clean, organized structure]

Datapizza-AI is a framework that gives you clear interfaces and predictable behavior for everything from simple chatbots to complex multi-agent systems. Think of it as your reliable foundation for GenAI work.

Now, before we dive in, a quick heads-up: this is a hands-on series. By the end of these nine videos, you'll have built chatbots, AI agents, and RAG systems—the whole stack. And you'll actually understand how they work under the hood.

In this first video, you'll learn what makes Datapizza-AI different and get your first chatbot running in about seven lines of code. It's a pretty solid start.

Alright, let's take a look at what we're covering today.

## Content Main (6.5 min)

### What Problem Does Datapizza-AI Solve? (2 min)

Okay, so let's be honest—building with LLMs can be incredibly frustrating. You have different APIs for OpenAI, Anthropic, and Google, and each one has its own quirks and edge cases. Memory management is all over the place, and when something breaks in production, good luck figuring out why.

Datapizza-AI is designed to solve these problems by providing an easy-to-use framework that merges powerful tools and customizations with full control over your application, making it much easier to monitor and debug everything you build.

[Visual: Split screen showing different provider APIs side by side]

Specifically, Datapizza-AI gives you:

**First**: A unified client interface. Whether you're using GPT, Claude, or Gemini, your code will look the same. You can write it once and swap providers with ease.

**Second**: Built-in memory management. No more manually tracking conversation history or losing context mid-chat.

**Third**: End-to-end observability. You can actually see what's happening inside your application—from token usage to response times, across the entire pipeline.

[Visual: Diagram showing unified architecture]

The framework isn't trying to abstract everything away; you still have full control. But it handles the tedious parts so you can focus on building what matters.

### Quick Installation and Setup (1.5 min)

Alright, time to install this thing. It takes about 30 seconds, seriously. You'll need Python 3.12 or higher.

[Show terminal]

```bash
pip install datapizza-ai
```

That's it for the core. If you want a specific provider, install the client (OpenAI is already present in the library):

```bash
pip install datapizza-ai-clients-openai
```

Create a `.env` file for your API keys:

```
OPENAI_API_KEY=sk-your-key-here
```

[Note for narrator: Speak casually, like you're helping a friend set this up]

### Your First Working Example (3 min)

Now for the fun part—let's write some code. I'm going to show you the simplest possible chatbot, then we'll break down exactly what's happening.

[Show code editor]

```python
import os
from dotenv import load_dotenv
from datapizza.clients.openai import OpenAIClient

load_dotenv()

client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    system_prompt="You are a helpful AI assistant."
)

response = client.invoke("Explain quantum computing in one sentence")
print(response.text)
```

[Run the code, show output]

That's it. Seven lines of actual code and you have a working LLM client.

Here's what's happening: We load environment variables, create a client with our API key and model choice, add a system prompt to set behavior, and invoke it with a question.

[Highlight each part as you explain]

The `response` object gives you not just the text but also valuable metadata, like tokens used and model info—everything you need for monitoring.

Notice that we're using `response.text` to get the answer. The framework wraps everything in structured objects, so you always know what you're working with.

[Visual: Show response object structure]

This simple pattern—client, invoke, response—is the foundation for everything we'll build in this series.

## Conclusion (1.5 min)

Alright, let's do a quick recap of what we've covered.

Datapizza-AI gives you a unified interface across different LLM providers, handles memory and context automatically, and provides full visibility into your application's behavior, allowing you to easily debug and maintain control over your code.

We installed the framework in seconds and built a working chatbot in just seven lines of code.

[Visual: Show key points as bullets]

In the next video, we're going to take this much further. We'll add conversation memory so the chatbot can remember what you've said, implement caching to save money and improve speed, and handle errors properly so your application remains stable in production.

And this is just the beginning. By the end of this series, you'll be building multi-agent systems and production-ready RAG pipelines—real, complete products.

If you're coding along with us, and I hope you are, try modifying the system prompt or asking different questions. Experiment with it and get comfortable with this basic client pattern, because it's the foundation for everything that follows.

The code is in the description below, and if you found this video useful, please hit the like button. I'll see you in the next one!

