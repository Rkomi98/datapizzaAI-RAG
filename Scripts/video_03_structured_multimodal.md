# Video 3: Structured Responses and Multimodal Capabilities

## Introduction (1.5 min)

Hey everyone, and welcome back. So far, we've built a text-based chatbot with memory and caching. That's a solid foundation, but modern applications require much more than that.

You'll often need structured data, like JSON responses that you can parse and use programmatically. You'll also need to work with more than just text, including images, audio, and documents—the entire multimodal stack.

[Visual: Show text bubbles transforming into JSON structures and media files]

Today, we're covering two major capabilities: getting reliable structured outputs using Pydantic models and working with multimodal inputs like images and audio.

By the end of this video, you'll be able to extract structured data from LLM responses and build chatbots that can "see" and "hear," not just read text.

Alright, let's start by exploring two approaches to getting structured data.

## Main Content (8 min)

### Getting JSON with Prompt Engineering (1.5 min)

The simplest way to get JSON from an LLM is to just ask for it. But there's a catch: you need to be very precise with your instructions.

[Show code]

```python
client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0.7
)

prompt = """
Return a valid JSON object only, with no extra text.
Schema:
{
  "title": string,
  "status": one of [planned, in_progress, done],
  "tasks": array of {
    "name": string,
    "owner": string,
    "eta_days": integer
  }
}
"""

response = client.invoke(prompt)
data = json.loads(response.text)
print("Title:", data["title"]) 
```

[Show the output]

While this can work, it's often brittle. For more reliable results, you should use features like JSON mode or function calling, which guarantee valid JSON. Otherwise, you'll need to implement robust parsing and validation yourself.

That's why there's a much better way.

### Structured Responses with Pydantic (2.5 min)

Instead of just hoping for valid JSON, you can enforce it using Pydantic models. This way, the framework handles the validation for you automatically.

[Show code]

```python
from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    name: str
    owner: str
    eta_days: int

class ProjectSummary(BaseModel):
    title: str
    status: str
    tasks: List[Task]

response = client.structured_response(
    input="Summarize our Q4 project plan",
    output_cls=ProjectSummary
)

# Get the validated, typed object
project = response.structured_data[0]
print(project.title)
print(project.status)

for task in project.tasks:
    print(f"{task.name} - {task.owner} - {task.eta_days} days")
```

[Run code, show output]

See the difference? You get a typed Python object back, complete with full IDE autocomplete. There's no need for manual parsing or `try-except` blocks to check for malformed JSON.

[Visual: Show IDE autocomplete working on the project object]

The model is constrained to return data that matches your schema. If it fails to do so, you'll get a validation error before your code even sees the response.

This is how you build reliable, production-ready systems. You define your data model, and you let Pydantic enforce it.

### Working with Images (2 min)

Now, let's talk about vision. Modern LLMs can analyze images, and Datapizza-AI makes this incredibly straightforward.

You can provide images in three ways: via URLs, as base64-encoded data, or directly from file paths. Let's take a look at all three.

[Show code - This is one of the last images ever taken by NASA's InSight Mars lander. Captured on Dec. 11, 2022, it shows InSight's seismometer on the Red Planet's surface.]

```python
from datapizza.type import Media, MediaBlock, TextBlock

# Method 1: From URL
media = Media(
    extension="jpg",
    media_type="image",
    source_type="url",
    source="https://images-assets.nasa.gov/image/PIA25680/PIA25680~orig.jpg?w=1024&h=1024&fit=clip&crop=faces%2Cfocalpoint",
    detail="high"
)

response = client.invoke([
    TextBlock(content="Describe this image in detail"),
    MediaBlock(media=media)
])
```

[Show example output]

The model sees the image and can describe it, answer questions about it, extract text from it—whatever you need.

[Show code for base64]

```python
# Method 2: Base64 encoding (for local files)
import base64

with open("diagram.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

media = Media(
    extension="png",
    media_type="image",
    source_type="base64",
    source=image_data,
    detail="high"
)

response = client.invoke([
    TextBlock(content="Extract the workflow steps from this diagram"),
    MediaBlock(media=media)
])
```

[Run and show analysis]

This is powerful for document processing—analyzing charts, extracting table data, reading handwritten notes. The model can see structure that traditional OCR might miss.

### Working with Audio (1.5 min)

But we're not limited to just images. Modern multimodal models can also work with audio—transcription, translation, sentiment analysis, you name it.

[Show code]

```python
# Audio from URL
audio_media = Media(
    extension="mp3",
    media_type="audio",
    source_type="url",
    source="https://example.com/recording.mp3"
)

response = client.invoke([
    TextBlock(content="Transcribe this audio and summarize the main points"),
    MediaBlock(media=audio_media)
])
```

[Show transcription output]

You can also load audio from local files using base64 encoding, just like we did with images.

```python
# Audio from local file
with open("meeting.wav", "rb") as f:
    audio_data = base64.b64encode(f.read()).decode()

audio_media = Media(
    extension="wav",
    media_type="audio",
    source_type="base64",
    source=audio_data
)

response = client.invoke([
    TextBlock(content="What is being discussed in this recording?"),
    MediaBlock(media=audio_media)
])
```

[Show analysis]

This opens up voice interfaces, meeting transcription, podcast analysis—any audio-based use case you can imagine. And just like with images, you can combine audio with memory for multi-turn conversations about the content.

[Show a multimodal conversation example]

You can even combine this with memory for ongoing visual conversations:

```python
memory = Memory()

image_block = MediaBlock(media=media)  # reuse whichever Media you defined above

# First turn: show image
memory.add_turn([
    TextBlock(content="Analyze this architecture diagram"),
    image_block
], ROLE.USER)

response = client.invoke("", memory=memory)
memory.add_turn([TextBlock(content=response.text)], ROLE.ASSISTANT)

# Second turn: reference the image
response = client.invoke(
    "What improvements would you suggest?", 
    memory=memory
)
```

[Demonstrate the conversation flow]

The model remembers the image across multiple turns, so you don't have to send it again.

## Conclusion (1 min)

Let's do a quick recap. We covered two methods for getting structured outputs: basic JSON prompting and robust Pydantic models. You should always use Pydantic when you need reliable, typed data.

We also explored multimodal capabilities, showing you how to work with both images and audio using URLs, base64 encoding, or file paths. This opens the door to document analysis, visual Q&A, voice interfaces, and multimodal conversations—pretty much anything you can imagine.

[Visual: Show structured data and images as building blocks]

In the next video, we'll be working with multiple LLM providers using `ClientFactory`, and you'll learn how to build custom adapters for providers that aren't supported out of the box. This is super useful if you're working with specialized or custom models.

Before then, try building something multimodal yourself—maybe a document analyzer or an image-based chatbot. As always, experiment with it! The patterns we covered today are the foundation for much more complex applications.

Drop a like if this was helpful, and I'll see you in the next video, where we'll learn how to manage different clients!

[Note for narrator: Energy should be building—we're adding capabilities fast]
