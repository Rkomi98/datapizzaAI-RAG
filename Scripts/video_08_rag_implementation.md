# Video 8: Complete RAG Implementation

## Introduction (1.5 min)

Hey everyone, and welcome back. We've built agents, multi-agent systems, and conversational interfaces. Now, we're tackling one of the most practical and powerful applications of LLMs: Retrieval-Augmented Generation, or RAG.

[Visual: Show document being broken into chunks, searched, and used to answer questions]

RAG allows you to build systems that can answer questions using your own private documents—internal wikis, product documentation, research papers, you name it. The LLM doesn't just generate text from its training data; it retrieves relevant context from your documents first.

Today, we're building a complete RAG pipeline from scratch. We'll parse documents, create embeddings, store them in a vector database, retrieve the most relevant chunks, and generate grounded answers. We're covering the full stack.

This is a production-ready pattern that companies are using right now. By the end of this video, you'll have a working knowledge base that you can query using natural language.

Alright, let's dive into the RAG pipeline.

## Content Main (7.5 min)

### Setting Up the Infrastructure (1 min)

A RAG system needs a vector database. We'll be using Qdrant—it's fast, open-source, and incredibly easy to run with Docker.

[Show terminal]

```bash
docker run -p 6333:6333 qdrant/qdrant
```

That's it. Qdrant is now up and running at `localhost:6333`, and you can see the dashboard at that address.

[Show browser with Qdrant dashboard]

Now, let's set up our imports and clients. We need two separate clients: one for embeddings and one for generation.

```python
import os
from dotenv import load_dotenv
from datapizza.clients.openai import OpenAIClient
from datapizza.embedders.openai import OpenAIEmbedder
from datapizza.core.vectorstore import VectorConfig
from datapizza.vectorstores.qdrant import QdrantVectorstore

load_dotenv()

# Client for text generation
client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini"
)

# Embedder client for creating vectors
embedder_client = OpenAIEmbedder(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)
```

We'll use separate clients for embedding and generation throughout this pipeline.

### Ingestion Pipeline: From Documents to Vectors (2.5 min)

The ingestion pipeline processes documents and stores them in the vector database. Datapizza-AI provides the IngestionPipeline class to handle this workflow automatically.

First, let's install the parser we need:

```bash
pip install datapizza-ai-parsers-docling
```

Now, let's set up the complete pipeline:

```python
from datapizza.pipeline import IngestionPipeline
from datapizza.modules.parsers.docling import DoclingParser
from datapizza.modules.splitters import NodeSplitter
from datapizza.embedders import ChunkEmbedder

# First, create the vector database collection
vectorstore = QdrantVectorstore(host="localhost", port=6333)
vectorstore.create_collection(
    "my_documents",
    vector_config=[VectorConfig(name="embedding", dimensions=1536)]
)

# Build the ingestion pipeline
ingestion_pipeline = IngestionPipeline(
    modules=[
        DoclingParser(),  # Parse PDFs and documents
        NodeSplitter(max_char=1000),  # Split into chunks
        ChunkEmbedder(client=embedder_client),  # Add embeddings
    ],
    vector_store=vectorstore,
    collection_name="my_documents"
)

# Run the pipeline
ingestion_pipeline.run("sample.pdf", metadata={"source": "user_upload"})
```

[Show execution]

That's it! The pipeline automatically:
1. Parses the document with DoclingParser (handles PDFs, DOCX, and more)
2. Splits it into manageable chunks with NodeSplitter
3. Generates embeddings with ChunkEmbedder
4. Stores everything in Qdrant

[Show Qdrant dashboard with stored vectors]

You can verify the data was stored by searching:

```python
res = vectorstore.search(
    query_vector=[0.0] * 1536,
    collection_name="my_documents",
    k=2,
)
print(res)
```

Your documents are now searchable by semantic similarity. Let's build the retrieval pipeline.

### Retrieval Pipeline: From Query to Answer (3 min)

Now, when a user asks a question, we need to find the relevant chunks and generate an answer. We'll use DagPipeline for this—it's perfect for handling complex retrieval workflows with multiple dependencies.

Let's build the complete retrieval pipeline:

```python
from datapizza.pipeline import DagPipeline
from datapizza.modules.rewriters import ToolRewriter
from datapizza.modules.prompt import ChatPromptTemplate

# Initialize components
query_rewriter = ToolRewriter(
    client=client,
    system_prompt="Rewrite user queries to improve retrieval accuracy."
)

# Use the same embedder from ingestion
retriever = QdrantVectorstore(host="localhost", port=6333)

prompt_template = ChatPromptTemplate(
    user_prompt_template="User question: {{user_prompt}}",
    retrieval_prompt_template="Retrieved content:\n{% for chunk in chunks %}{{ chunk.text }}\n{% endfor %}"
)

# Build the DAG
dag_pipeline = DagPipeline()
dag_pipeline.add_module("rewriter", query_rewriter)
dag_pipeline.add_module("embedder", embedder_client)
dag_pipeline.add_module("retriever", retriever)
dag_pipeline.add_module("prompt", prompt_template)
dag_pipeline.add_module("generator", client)

# Connect the modules
dag_pipeline.connect("rewriter", "embedder", target_key="text")
dag_pipeline.connect("embedder", "retriever", target_key="query_vector")
dag_pipeline.connect("retriever", "prompt", target_key="chunks")
dag_pipeline.connect("prompt", "generator", target_key="memory")

# Run the pipeline
query = "tell me something about this document"
result = dag_pipeline.run({
    "rewriter": {"user_prompt": query},
    "prompt": {"user_prompt": query},
    "retriever": {"collection_name": "my_documents", "k": 3},
    "generator": {"input": query}
})

print(f"Generated response: {result['generator']}")
```

[Show execution with flow diagram]

Let me break down what's happening here:

1. **Query Rewriting**: The user's query is rewritten for better retrieval
2. **Embedding**: The rewritten query is converted to a vector
3. **Retrieval**: We search the vector database for similar chunks
4. **Prompt Formatting**: Retrieved chunks are formatted into a prompt
5. **Generation**: The LLM generates an answer using the context

[Visual: Show complete RAG flow diagram with all steps]

The DagPipeline automatically handles the data flow between components. Each module processes its input and passes the output to the next one.

### Making It Production-Ready (1 min)

This works great, but a production-ready RAG system needs a bit more sophistication. Here are a few key patterns we've already seen in action:

**Query rewriting**: We already included this in our DagPipeline—it transforms vague questions into better search queries automatically.

**Metadata filtering**: You can filter by document metadata during retrieval:

```python
result = dag_pipeline.run({
    "rewriter": {"user_prompt": query},
    "prompt": {"user_prompt": query},
    "retriever": {
        "collection_name": "my_documents",
        "k": 3,
        "filter": {"source": "user_upload"}  # Only search specific sources
    },
    "generator": {"input": query}
})
```

**Configuration-based pipelines**: You can also define your entire ingestion pipeline using YAML configuration files, making it easy to version control and modify without changing code.

These are the patterns that make RAG systems reliable and scalable in production.

## Conclusion (1 min)

Let's do a quick recap of the full pipeline. We use IngestionPipeline to parse documents, split them into chunks, generate embeddings, and store them in Qdrant. Then we use DagPipeline for retrieval—it handles query rewriting, embedding, vector search, prompt formatting, and answer generation in one cohesive workflow.

[Visual: Show complete pipeline with all steps]

This is how you make LLMs genuinely useful for real-world business problems. Product support, internal documentation, and research assistance are all built on this exact foundation.

Next up is our final video, where we'll cover pipelines for building complex workflows and implementing production monitoring so you can actually deploy this stuff with confidence.

Before that, I encourage you to build your own knowledge base. Ingest some of your own documents, query them, and experiment with different chunk sizes and reranking strategies. See for yourself how retrieval quality affects the accuracy of the final answer. It's fascinating to tune.

This is what production-grade AI engineering looks like. If you're still with me, hit that subscribe button, and I'll see you in the final video!

[Note for narrator: This should feel like a culmination—we're building real, deployable systems]
