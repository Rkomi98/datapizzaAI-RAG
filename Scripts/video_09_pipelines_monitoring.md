# Video 9: Pipelines and Production Monitoring

## Introduction (1.5 min)

Hey everyone, and welcome to the final video in this series. We've built chatbots, agents, multi-agent systems, and RAG pipelines. But there's one critical topic we haven't covered yet: how do you actually run this stuff in production?

[Visual: Show development environment transforming into production architecture]

Production means reliability, observability, and orchestration. You need to be able to process data through complex workflows, monitor what's happening in real-time, and effectively debug when things inevitably go wrong.

Today, we're covering two critical topics: building pipelines for complex data workflows and implementing comprehensive monitoring with OpenTelemetry, Prometheus, and Grafana.

This is what separates a proof-of-concept from a production system that can actually work at scale.

Alright, let's start with the three main pipeline types.

## Content Main (7.5 min)

### Understanding Pipelines (2 min)

Datapizza-AI provides three distinct pipeline types, each designed for different use cases. Let me break them down for you.

[Visual: Show three pipeline diagrams side by side]

**IngestionPipeline**: For processing documents and loading them into vector stores. The typical flow is Parser → Splitter → Embedder → Storage. This is your RAG ingestion pipeline.

**DagPipeline**: For creating dependency graphs. You define nodes and their connections, and the pipeline executes them in parallel whenever possible. Use this for complex data transformations.

**FunctionalPipeline**: For advanced control flow, including branching, loops, and conditional execution. This is ideal for implementing business logic and multi-step workflows.

Let me show you how each one works.

### IngestionPipeline in Action (1.5 min)

The ingestion pipeline we used in the RAG video is a formal pipeline type in the framework.

```python
from datapizza.pipelines import IngestionPipeline
from datapizza.parsers import TextParser
from datapizza.rag.splitter import NodeSplitter
from datapizza.rag.embedder import NodeEmbedder

components = [
    TextParser(),
    NodeSplitter(max_char=1000),
    NodeEmbedder(client=client, model_name="text-embedding-3-small")
]

pipeline = IngestionPipeline(
    modules=components,
    vector_store=vectorstore,
    collection_name="documents"
)

# Process documents
chunks = pipeline.run(
    file_path="document.txt",
    metadata={"source": "internal_docs"}
)
```

[Show execution]

Each component processes the output of the previous one. The pipeline automatically handles the sequencing, error propagation, and final storage for you.

This pattern is designed to be scalable. You can add a captioner for images or a metatagger for keywords—just insert the new components into the list.

### DagPipeline for Complex Dependencies (2 min)

DAG pipelines allow you to define explicit dependencies between different operations.

```python
from datapizza.pipelines import DagPipeline

class DataLoader(PipelineComponent):
    def _run(self, **kwargs):
        return {"reviews": ["Great product!", "Terrible", "It's okay"]}

class SentimentAnalyzer(PipelineComponent):
    def _run(self, reviews, **kwargs):
        results = [
            {"text": r, "sentiment": self._classify(r)} 
            for r in reviews
        ]
        return {"sentiment_results": results}

class StatisticsCalculator(PipelineComponent):
    def _run(self, sentiment_results, **kwargs):
        sentiments = [r["sentiment"] for r in sentiment_results]
        return {
            "stats": {
                "positive": sentiments.count("positive"),
                "negative": sentiments.count("negative")
            }
        }

pipeline = DagPipeline()
pipeline.add_module("loader", DataLoader())
pipeline.add_module("analyzer", SentimentAnalyzer())
pipeline.add_module("stats", StatisticsCalculator())

pipeline.connect("loader", "analyzer", "reviews", "reviews")
pipeline.connect("analyzer", "stats", "sentiment_results", "sentiment_results")

results = pipeline.run({})
```

[Show execution with timing]

The pipeline executes the nodes in the correct order based on their dependencies. If two nodes have no dependency on each other, they can be run in parallel.

This is perfect for ETL workflows, data processing pipelines, and other multi-step analysis tasks.

### FunctionalPipeline with Branching (2 min)

Functional pipelines support conditional execution, allowing you to build dynamic workflows.

```python
from datapizza.pipelines import FunctionalPipeline, Dependency

class DocumentClassifier(PipelineComponent):
    def _run(self, documents, **kwargs):
        urgent = [d for d in documents if d.get("priority") == "urgent"]
        return {
            "documents": documents,
            "urgent_documents": urgent,
            "has_urgent": len(urgent) > 0
        }

class NotificationSender(PipelineComponent):
    def _run(self, **kwargs):
        return {"notification_sent": True}

class ReportGenerator(PipelineComponent):
    def _run(self, documents, **kwargs):
        return {"report": f"Processed {len(documents)} documents"}

pipeline = (
    FunctionalPipeline()
    .run(name="load", node=DataLoader())
    .then(name="classify", node=DocumentClassifier(), target_key="documents")
    .branch(
        condition=lambda ctx: ctx.get("classify", {}).get("has_urgent", False),
        if_true=FunctionalPipeline().run("notify", NotificationSender()),
        if_false=FunctionalPipeline().run("report", ReportGenerator())
    )
)

results = pipeline.execute()
```

[Show both branches executing based on different data]

The pipeline routes execution based on runtime conditions. In this case, urgent documents trigger notifications, while normal documents are processed differently.

This is how you can encode complex business logic into reproducible and maintainable workflows.

### Production Monitoring (2 min)

Alright, now let's talk about observability. Because in a production environment, you need to know what's happening at all times.

Datapizza-AI integrates seamlessly with OpenTelemetry for tracing.

```python
from datapizza.tracing import ContextTracing

with ContextTracing().trace("conversation"):
    memory.add_turn([TextBlock(content=user_input)], ROLE.USER)
    response = client.invoke(user_input, memory=memory)
    memory.add_turn([TextBlock(content=response.text)], ROLE.ASSISTANT)
```

[Show trace output with rich console display]

You get automatic tracking of token usage, latency, model usage, and API call patterns right out of the box. The output shows a beautiful summary table with all your metrics.

```
╭─ Trace Summary of conversation ───────────────────────── ╮
│ Total Spans: 3                                           │
│ Duration: 2.45s                                          │
│ ┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━┓
│ ┃ Model       ┃ Prompt Tokens ┃ Completion Tokens ┃ ... ┃
│ ┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━┩
│ │ gpt-4o-mini │ 31            │ 27                │ ... │
│ └─────────────┴───────────────┴───────────────────┴─────┘
╰──────────────────────────────────────────────────────────╯
```

For more detailed logging, you can enable input/output tracing:

```python
# Set environment variable
import os
os.environ["DATAPIZZA_TRACE_CLIENT_IO"] = "TRUE"

# Now traces will include full input/output and memory content
```

You can also add manual spans for granular control:

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with ContextTracing().trace("rag_pipeline"):
    with tracer.start_as_current_span("database_query"):
        data = fetch_from_database()
    
    with tracer.start_as_current_span("data_validation"):
        validate_data(data)
    
    with tracer.start_as_current_span("generation"):
        result = client.invoke(prompt)
```

**Exporting to External Systems**

You can send traces to Zipkin, Grafana, or any OTLP-compatible backend:

```python
from opentelemetry import trace
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

# Set up the trace provider
resource = Resource.create({
    ResourceAttributes.SERVICE_NAME: "my_rag_service",
})
trace.set_tracer_provider(TracerProvider(resource=resource))

# Add Zipkin exporter
zipkin_exporter = ZipkinExporter(
    endpoint="http://localhost:9411/api/v2/spans"
)
span_processor = SimpleSpanProcessor(zipkin_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Now all traces go to both console and Zipkin
```

[Show Zipkin/Grafana dashboard]

This is what production-grade observability looks like. You can debug issues, optimize costs, and monitor performance across your entire stack.

## Conclusion (1.5 min)

Alright, let's do a quick recap of the entire series.

We started with basic chatbots and then added memory and caching. We explored structured outputs and multimodal capabilities. We built autonomous agents and then scaled up to multi-agent systems. We implemented a complete RAG pipeline from scratch. And today, we covered production-level workflows and monitoring.

[Visual: Show journey from Video 1 to Video 9]

You now have everything you need to build production-ready Generative AI applications with Datapizza-AI. I mean, actually ship them to production.

The patterns we've covered—unified clients, explicit memory management, tool-based agents, RAG pipelines, and observability—are the foundations of reliable AI systems that companies are using in the real world.

This isn't just about making things work on your laptop. It's about making them work reliably, at scale, with full visibility and control. That's the difference between a toy project and a real product.

[Visual: Show production architecture diagram]

If you've followed along and built these systems, you're in a very good position. Now, it's time to take them further. Deploy them to production, handle real traffic, and scale them up. That's where the real learning begins.

Thanks for sticking with me through this entire series. Seriously, if you made it this far, you're committed. Now go build something amazing with what you've learned.

If this series was helpful for you, hit that subscribe button and drop a comment with what you're building. I'd love to see it. The code for everything is in the description below.

I'll see you in the next series!

[Note for narrator: This should feel like a graduation—the viewer has learned a complete skill set and is ready for production work]
