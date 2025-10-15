# Video 5: Tools and Function Calling

## Introduction (1.5 min)

Hey everyone, and welcome back. Up until now, our LLMs could only generate text. They could explain concepts, answer questions, and even write code—but they couldn't actually *do* anything.

That all changes today with tools and function calling.

[Visual: Show chatbot connected to various tools - calculator, search, database]

Function calling allows LLMs to take action. Whether you need to fetch data from an API, search the web, or run complex calculations, the model can decide which tools to use and execute them autonomously.

This is how you build agents, not just chatbots. It's how you connect LLMs to the real world and make them truly useful.

By the end of this video, you'll know how to define tools, control when they're used, and build interactive applications that combine reasoning with action.

Alright, so what exactly are tools?

## Content Main (7.5 min)

### Defining Your First Tool (2 min)

Here's the cool part: a tool is just a Python function with a decorator. That's it. Check this out:

[Show code]

```python
from datapizza.tools import tool

@tool
def calculator(expression: str) -> str:
    """Performs simple calculations safely."""
    try:
        allowed = set("0123456789+-*/(). ")
        if not set(expression) <= allowed:
            return "Error: invalid characters"
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"
```

The `@tool` decorator tells Datapizza-AI this function can be called by the model. The docstring is important because it tells the model what the tool does.

[Highlight the docstring]

The model reads that docstring and decides whether to use this tool based on the user's request. As in real life, clear documentation means better tool selection.

Now let's use it:

```python
response = client.invoke(
    "Calculate 25 * 4 + 100",
    tools=[calculator],
    tool_choice="auto"
)

# Check if the model called the function
if response.function_calls:
    for call in response.function_calls:
        result = calculator(**(call.arguments or {}))
        print(f"Tool result: {result}")

print(response.text)
```

[Run and show output]

The model sees the question, realizes it needs to perform a calculation, and returns a function call instead of a simple text response. We then execute that function and get the result.

This is the basic pattern: define a tool, pass it to `invoke`, check for function calls, and execute them.

### Multi-Tool Interactions (2.5 min)

Real-world applications often use multiple tools. Let me show you a practical example with a calculator and a search function.

[Show code]

```python
@tool
def calculator(expr: str) -> str:
    """Performs calculations."""
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Error: {e}"

@tool
def search_info(query: str) -> str:
    """Searches for information."""
    # In production, this would hit a real search API
    return f"Results for: {query}"

tools = [calculator, search_info]
memory = Memory()

response = client.invoke(
    "Calculate 25 * 4, then search for Python tutorials",
    tools=tools,
    memory=memory
)
```

[Show the interaction]

Now, here's where it gets interesting. The model might need to make multiple tool calls to answer a single question, so you'll need a loop to handle this.

```python
from datapizza.type import FunctionCallResultBlock

while response.function_calls:
    # Add the model's response to memory
    memory.add_turn(response.content, ROLE.ASSISTANT)
    
    # Execute each tool call
    for call in response.function_calls:
        if call.name == "calculator":
            result = calculator(**(call.arguments or {}))
        elif call.name == "search_info":
            result = search_info(**(call.arguments or {}))
        else:
            result = f"Unknown tool: {call.name}"
        
        # Add tool result to memory
        tool_result = FunctionCallResultBlock(
            id=call.id,
            tool=call.tool,
            result=result
        )
        memory.add_turn([tool_result], ROLE.TOOL)
    
    # Call the model again with tool results
    response = client.invoke(
        input=response,
        tools=tools,
        memory=memory
    )
```

[Walk through this carefully]

This loop handles the full tool execution cycle: the model calls the tools, we execute them, add the results to memory, and then invoke the model again. The model sees those results and either calls more tools or generates a final text response.

[Visual: Show flowchart of the tool execution loop - TODO IN POST PROD near my face]

This is how agents work under the hood. It's a continuous loop of reasoning and action.

### Building a Conversational Tool Interface (3 min)

Now, let's combine everything into a practical, tool-enabled chatbot.

[Show complete code]

```python
from datapizza.tools import tool
from datapizza.memory import Memory
from datapizza.type import ROLE, TextBlock, FunctionCallResultBlock

@tool
def calculator(expr: str) -> str:
    """Performs mathematical calculations."""
    try:
        allowed = set("0123456789+-*/(). ")
        if not set(expr) <= allowed:
            return "Error: invalid characters"
        return f"Result: {eval(expr)}"
    except Exception as e:
        return f"Error: {e}"

client = GoogleClient(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.5-flash"
)

tools = [calculator]
memory = Memory()

print("Chatbot with tools ready! Type 'exit' to quit.")

while True:
    user_input = input("\nYou: ").strip()
    
    if user_input.lower() in ["exit", "quit"]:
        break
    
    if not user_input:
        continue
    
    # Add user message
    memory.add_turn([TextBlock(content=user_input)], ROLE.USER)
    
    # Get response
    response = client.invoke(
        input="",
        memory=memory,
        tools=tools,
        tool_choice="auto"
    )
    
    # Handle tool calls
    while response.function_calls:
        memory.add_turn(response.content, ROLE.ASSISTANT)
        
        for call in response.function_calls:
            print(f"[Using tool: {call.name}]")
            
            result = calculator(**(call.arguments or {}))
            
            tool_result = FunctionCallResultBlock(
                id=call.id,
                tool=call.tool,
                result=result
            )
            memory.add_turn([tool_result], ROLE.TOOL)
        
        response = client.invoke(
            input="",
            memory=memory,
            tools=tools
        )
    
    # Show final response
    print(f"Bot: {response.text}")
    memory.add_turn([TextBlock(content=response.text)], ROLE.ASSISTANT)
```

[Run the chatbot, show conversation]

Try asking it something like, "What's 150 * 83? And what's half of that?"

[Demonstrate the tool being called multiple times]

The model uses the calculator when it's needed but answers conversational questions normally. It knows when to use tools and when to just respond with text.

This is the foundation of agentic behavior—combining reasoning with the ability to take action.

## Conclusion (1 min)

Alright, let's do a quick summary. We defined tools using simple Python functions and the `@tool` decorator. We handled multi-tool scenarios with an execution loop. And we built a conversational chatbot that can decide when to use those tools autonomously.

This is a crucial concept for what's coming next. In the next video, we're building full-fledged AI agents—systems that can plan, reason, and use tools to accomplish complex tasks. This is where it gets seriously powerful.

Before that, try adding your own tools. Maybe a weather API, a database query function, or a file system operation. The pattern is always the same: define the function, add the decorator, and let the model decide when to use it.

If this was helpful, hit that like button. The code is in the description. I'll see you next time when we build our first agent!

[Note for narrator: Build excitement—tools are the gateway to agents]
