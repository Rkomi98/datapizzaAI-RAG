# Datapizza-AI pipeline guide

This guide provides practical examples for using the three pipeline types available in Datapizza-AI:

- **IngestionPipeline**: for processing and ingesting documents into vector stores
- **DagPipeline**: for creating dependency graphs between components  
- **FunctionalPipeline**: for functional pipelines with branching, loops, and dependencies

## Table of Contents

- [1. Ingestion pipeline](#1-ingestion-pipeline)
  - [Description](#description)
  - [Main components](#main-components)
  - [Practical example](#practical-example)
  - [Flow diagram](#flow-diagram)
- [2. Dag pipeline](#2-dag-pipeline)
  - [Description](#description-1)
  - [Main features](#main-features)
  - [Practical example](#practical-example-1)
  - [Flow diagram](#flow-diagram-1)
- [3. Functional pipeline](#3-functional-pipeline)
  - [Description](#description-2)
  - [Advanced features](#advanced-features)
  - [Practical example](#practical-example-2)
  - [Flow diagram](#flow-diagram-2)
  - [YAML configuration example](#yaml-configuration-example)
  - [Usage from Python](#usage-from-python)
- [YAML configuration](#yaml-configuration)
  - [Example for DagPipeline](#example-for-dagpipeline)
- [Pipeline comparison](#pipeline-comparison)

## 1. Ingestion pipeline

### Description

The IngestionPipeline is designed to process documents and ingest them into vector stores. It's ideal for building knowledge bases and RAG systems.

### Main components

- **Parser**: content extraction from documents
- **Splitter**: content division into chunks
- **Embedder**: vector embeddings generation
- **Vector store**: chunk storage with embeddings

### Practical example

```python
import os
from dotenv import load_dotenv

load_dotenv()

from datapizza.clients.openai import OpenAIClient

class FileReader(PipelineComponent):
    def _run(self, file_path: str, **kwargs) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    async def _a_run(self, file_path: str, **kwargs) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"), 
    model="text-embedding-3-small"
)

components = [
    FileReader(),
    TextSplitter(
        max_char=200,
        overlap=50
    ),
    NodeEmbedder(
        client=client,
        model_name="text-embedding-3-small"
    )
]

pipeline = IngestionPipeline(
    modules=components,
    vector_store=None,
    collection_name=None
)

chunks = pipeline.run(
    file_path="document.txt",
    metadata={"source": "example"}
)

print(f"Generated {len(chunks)} chunks from document")
```

### Important notes

- **NodeEmbedder vs ClientEmbedder**: use `NodeEmbedder` in pipelines because it works with lists of `Chunk` objects. `ClientEmbedder` is for single strings.
- **Metadata**: applied by `IngestionPipeline.run()` after chunk creation, not during splitting
- **Embeddings**: `NodeEmbedder` adds embeddings to existing `Chunk` objects, doesn't create new ones

### Flow diagram

![Ingestion Pipeline Flow](ingestion-pipeline-flow.svg)


## 2. Dag pipeline

### Description

The DagPipeline allows creating dependency graphs (DAG - Directed Acyclic Graph) between components, where each node can depend on the results of previous nodes.

### Main features

- **Nodes**: components that perform specific operations
- **Connections**: define dependencies between nodes
- **Parallel execution**: independent nodes are executed in parallel
- **Error handling**: controlled error propagation through the graph

### Practical example

```python

class DataLoader(PipelineComponent):
    def _run(self, **kwargs):
        return {"reviews": ["Excellent product!", "I don't like it", "Average"]}
    async def _a_run(self, **kwargs):
        return self._run(**kwargs)

class SentimentAnalyzer(PipelineComponent):
    def _run(self, reviews, **kwargs):
        analyzed = [
            {
                "text": r,
                "sentiment": "positive" if "excellent" in r.lower() else "negative" if "don't" in r.lower() else "neutral"
            }
            for r in reviews
        ]
        return {"sentiment_results": analyzed}
    async def _a_run(self, reviews, **kwargs):
        return self._run(reviews=reviews, **kwargs)

class StatisticsCalculator(PipelineComponent):
    def _run(self, sentiment_results, **kwargs):
        sentiments = [r["sentiment"] for r in sentiment_results]
        stats = {
            "positive": sentiments.count("positive"),
            "negative": sentiments.count("negative"), 
            "neutral": sentiments.count("neutral")
        }
        return {"statistics": stats}
    async def _a_run(self, sentiment_results, **kwargs):
        return self._run(sentiment_results=sentiment_results, **kwargs)

class MetadataExtractor(PipelineComponent):
    def _run(self, reviews, **kwargs):
        metadata = {
            "total_reviews": len(reviews),
            "avg_length": sum(len(r) for r in reviews) / len(reviews),
            "timestamp": "2025-09-15"
        }
        return {"metadata": metadata}
    async def _a_run(self, reviews, **kwargs):
        return self._run(reviews=reviews, **kwargs)

class ReportGenerator(PipelineComponent):
    def _run(self, sentiment_results, statistics, metadata, **kwargs):
        report = f"""
ANALYSIS REPORT - {metadata['timestamp']}
Total reviews: {metadata['total_reviews']}
Average length: {metadata['avg_length']:.1f}

SENTIMENT:
- Positive: {statistics['positive']}
- Negative: {statistics['negative']}
- Neutral: {statistics['neutral']}

DETAILS:
{chr(10).join(f"- {r['text']}: {r['sentiment']}" for r in sentiment_results)}
        """
        return {"final_report": report.strip()}
    async def _a_run(self, sentiment_results, statistics, metadata, **kwargs):
        return self._run(sentiment_results=sentiment_results, statistics=statistics, metadata=metadata, **kwargs)

pipeline = DagPipeline()

pipeline.add_module("data_loader", DataLoader())
pipeline.add_module("sentiment_analyzer", SentimentAnalyzer())
pipeline.add_module("statistics_calculator", StatisticsCalculator())
pipeline.add_module("metadata_extractor", MetadataExtractor())
pipeline.add_module("report_generator", ReportGenerator())

pipeline.connect(
    source_node="data_loader",
    target_node="sentiment_analyzer",
    source_key="reviews",
    target_key="reviews"
)

pipeline.connect(
    source_node="sentiment_analyzer",
    target_node="statistics_calculator",
    source_key="sentiment_results",
    target_key="sentiment_results"
)

pipeline.connect(
    source_node="data_loader",
    target_node="metadata_extractor",
    source_key="reviews",
    target_key="reviews"
)

pipeline.connect(
    source_node="sentiment_analyzer",
    target_node="report_generator",
    source_key="sentiment_results",
    target_key="sentiment_results"
)

pipeline.connect(
    source_node="statistics_calculator",
    target_node="report_generator",
    source_key="statistics",
    target_key="statistics"
)

pipeline.connect(
    source_node="metadata_extractor",
    target_node="report_generator",
    source_key="metadata",
    target_key="metadata"
)

results = pipeline.run({})
print(results["report_generator"]["final_report"])
```

### Flow diagram

![DAG Pipeline Flow](dag-pipeline-flow.svg)


## 3. Functional pipeline

### Description

The FunctionalPipeline offers a functional approach to pipeline construction with support for conditional branching, loops, and complex dependencies.

### Advanced features

- **Branching**: conditional execution of sub-pipelines
- **Foreach**: iteration over data collections
- **Dependencies**: explicit dependency management between nodes
- **Composition**: combination of complex pipelines

### Practical example

```python

class DataLoader(PipelineComponent):
    def _run(self, **kwargs):
        documents = [
            {"id": 1, "title": "Bug Critical", "content": "System crash", "priority": "urgent"},
            {"id": 2, "title": "Feature Request", "content": "New feature", "priority": "normal"},
            {"id": 3, "title": "Security Issue", "content": "Vulnerability found", "priority": "urgent"}
        ]
        return {"documents": documents}
    async def _a_run(self, **kwargs):
        return self._run(**kwargs)

class Classifier(PipelineComponent):
    def _run(self, documents, **kwargs):
        if isinstance(documents, dict) and "documents" in documents:
            documents = documents["documents"]
        elif documents is None:
            documents = []
        
        urgent_docs = [d for d in documents if isinstance(d, dict) and d.get("priority") == "urgent"]
        has_urgent = len(urgent_docs) > 0
        
        return {
            "classified_documents": documents,
            "urgent_documents": urgent_docs,
            "has_urgent": has_urgent
        }
    async def _a_run(self, documents, **kwargs):
        return self._run(documents=documents, **kwargs)

class NotificationSender(PipelineComponent):
    def _run(self, **kwargs):
        return {
            "notification_sent": True,
            "message": "⚠️ Urgent documents detected! Notification sent to the team.",
            "timestamp": "2025-09-15T10:00:00Z"
        }
    async def _a_run(self, **kwargs):
        return self._run(**kwargs)

class DocumentProcessor(PipelineComponent):
    def _run(self, document, **kwargs):
        processed = {
            **document,
            "processed": True,
            "word_count": len(document["content"].split()),
            "processing_time": "2025-09-15T10:00:00Z"
        }
        return processed
    async def _a_run(self, document, **kwargs):
        return self._run(document=document, **kwargs)

class ReportGenerator(PipelineComponent):
    def _run(self, classified_documents, **kwargs):
        total = len(classified_documents)
        urgent_count = sum(1 for d in classified_documents if d.get("priority") == "urgent")
        normal_count = total - urgent_count
        
        report = f"""
DOCUMENT ANALYSIS REPORT
========================
Total documents: {total}
Urgent documents: {urgent_count}
Normal documents: {normal_count}

DETAILS:
{chr(10).join(f"- {d['title']}: {d['priority']}" for d in classified_documents)}
        """
        
        return {
            "final_report": report.strip(),
            "statistics": {
                "total": total,
                "urgent": urgent_count,
                "normal": normal_count
            }
        }
    async def _a_run(self, classified_documents, **kwargs):
        return self._run(classified_documents=classified_documents, **kwargs)

notification_pipeline = FunctionalPipeline().run(
    name="send_notification",
    node=NotificationSender()
)

standard_processing_pipeline = (
    FunctionalPipeline()
    .foreach(
        name="process_documents",
        dependencies=[Dependency(node_name="classified_documents", target_key=None)],
        do=DocumentProcessor()
    )
    .then(
        name="generate_report",
        node=ReportGenerator(),
        target_key="classified_documents",
        dependencies=[Dependency(node_name="classify", target_key="classified_documents")]
    )
)

pipeline = (
    FunctionalPipeline()
    .run(name="load_data", node=DataLoader())
    .then(name="classify", node=Classifier(), target_key="documents")
    .branch(
        condition=lambda ctx: ctx.get("classify", {}).get("has_urgent", False),
        dependencies=[Dependency(node_name="classify")],
        if_true=notification_pipeline,
        if_false=standard_processing_pipeline
    )
)

results = pipeline.execute()
```

### Flow diagram

![Functional Pipeline Flow](functional-pipeline-flow.svg)

### Data flow notes

- **Data passing**: in FunctionalPipeline, `target_key="documents"` passes the ENTIRE result of the previous node (e.g. `{"documents": [...]}`) to the `documents` parameter of the next node
- **Input handling**: components should handle both dictionaries and lists as input to be flexible
- **Context access**: use `lambda ctx: ctx.get("node_name", {}).get("key")` to access data in branching


### YAML configuration example

Example YAML configuration for the functional pipeline with conditional branching:

```yaml
name: "document_processing_pipeline"
description: "Functional pipeline with conditional branching"

steps:
  - name: "load_data"
    component: "DataLoader" 
  - name: "classify"
    component: "Classifier"
    depends_on: "load_data"
    input_key: "documents"
  - name: "notification_branch"
    type: "conditional_branch"
    condition: "has_urgent_documents"
    depends_on: "classify"
    if_true:
      - name: "send_notification"
        component: "NotificationSender"
    if_false:
      - name: "process_documents"
        component: "DocumentProcessor"
        type: "foreach"
      - name: "generate_report"  
        component: "ReportGenerator"

components:
  DataLoader:
    class: "pipeline_components.DataLoader"
    output_keys: ["documents"]
  Classifier:
    class: "pipeline_components.Classifier"
    output_keys: ["classified_documents", "has_urgent"]
  NotificationSender:
    class: "pipeline_components.NotificationSender"
  DocumentProcessor:
    class: "pipeline_components.DocumentProcessor"
  ReportGenerator:
    class: "pipeline_components.ReportGenerator"
```

See `functional_pipeline_example.yaml` for the complete configuration file with all parameters and sample data.

### Usage from Python

To use the YAML configuration from Python:

```python

pipeline = FunctionalPipeline.from_yaml("functional_pipeline_example.yaml")

results = pipeline.execute()

if "send_notification" in results:
    print("URGENT BRANCH EXECUTED:")
    print(results["send_notification"]["message"])
else:
    print("STANDARD BRANCH EXECUTED:")
    print(results["generate_report"]["final_report"])
```

This example demonstrates:
- Loading external modules from custom packages
- Parameter configuration for each module via YAML
- Dependency definition between nodes with `target_key`
- Multi-step pipeline completely configured externally


## YAML configuration

All pipelines support YAML configuration for greater flexibility and reusability.

### Example for DagPipeline

Loading and using DagPipeline from YAML configuration:

```python
import os
import sys

# Setup path to find mymodules (required for notebooks)
examples_dir = "/home/mcalcaterra/Documenti/GitHub/Datapizza/Datapizza-AI/PizzAI/Pipeline/examples"
sys.path.insert(0, examples_dir)

# Create DagPipeline instance and load YAML configuration
dag_pipeline = DagPipeline()
dag_pipeline.from_yaml(os.path.join(examples_dir, "dag_config.yaml"))

# Execute pipeline (data generated automatically by modules)
results = dag_pipeline.run({})

# Access results from each node
print(f"Executed nodes: {list(results.keys())}")
for node_name, result in results.items():
    print(f"{node_name}: {result}")
```

The YAML file `examples/dag_config.yaml` defines custom modules (`DocumentLoader`, `TextProcessor`) and their automatic connections.

**Execution**:
```bash
cd Pipeline/examples
python3 dag_yaml_example.py
```


### Example for FunctionalPipeline

Loading and using FunctionalPipeline from YAML configuration:

```python
import os
import sys

# Setup path to find mymodules (required for notebooks)
examples_dir = "/home/mcalcaterra/Documenti/GitHub/Datapizza/Datapizza-AI/PizzAI/Pipeline/examples"
sys.path.insert(0, examples_dir)

# Load functional pipeline from YAML file
pipeline = FunctionalPipeline.from_yaml(os.path.join(examples_dir, "functional_pipeline_config.yaml"))

# Execute complete pipeline
results = pipeline.execute()

# Show flow results
if "build_report" in results:
    print(results["build_report"]["final_report"])
else:
    print("Pipeline completed successfully!")

print(f"Executed modules: {list(results.keys())}")
```

The YAML file defines external modules (`DocumentLoader`, `TextProcessor`, `DataValidator`, `ReportBuilder`) and dependencies between steps with `target_key`.


## Pipeline comparison

| Feature | IngestionPipeline | DagPipeline | FunctionalPipeline |
|---------|------------------|-------------|-------------------|
| **Use case** | Document processing | Dependency graphs | Complex pipelines |
| **Complexity** | Low | Medium | High |
| **Branching** | No | No | Yes |
| **Loops** | No | No | Yes (foreach) |
| **Parallelism** | Sequential | Automatic | Controlled |
| **Vector store** | Integrated | Manual | Manual |


