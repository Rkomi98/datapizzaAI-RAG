# Video 7: Multi-Agent Systems

## Introduction (1.5 min)

Hey everyone, and welcome back. Single agents are powerful, but let's face it: complex problems often require specialized expertise. You wouldn't ask one person to handle finance, compliance, and engineering all at once. You'd build a team, right?

That's exactly what we're building today: multi-agent systems where specialized agents collaborate to solve complex problems together.

[Visual request in post production: Show organizational chart transforming into agent network]

We'll be building a strategic planning system with three distinct agents: an analyst who extracts key metrics, a risk assessor who identifies potential problems, and a planner who coordinates everything and produces the final report.

By the end of this video, you'll understand agent orchestration, delegation patterns, and how to prevent common pitfalls like infinite loops. This is production-grade architecture.

Alright, let's start with the design.

## Content Main (6.5 min)

### Designing the System (2 min)

Before we write a single line of code, let's design the system architecture. We need three specialized agents, and each one has a very specific job.

[Show diagram - Remember to send the svg - Gif on Github]

**AnalystAgent**: Extracts KPIs and other quantitative metrics. It focuses on numbers, revenue figures, and growth rates.

**RiskAgent**: Identifies operational risks by scanning for keywords like "compliance," "budget," and "deadline."

**StrategicPlanner**: The coordinator. It delegates tasks to the specialists, waits for their responses, and then synthesizes everything into a final, comprehensive report.

[Visual: Show data flow between agents]

The planner doesn't do the actual analysis itself—it orchestrates the workflow. This separation of concerns is a critical design principle. Each agent has one job, does it well, and then returns control to the planner.

And here's why this pattern is so powerful: it scales almost infinitely. Need a legal review? Add a `LegalAgent`. Need a technical assessment? Add an `EngineerAgent`. The planner's logic stays exactly the same; you just add more specialist tools to its arsenal.

Think about how powerful this is for real-world applications. For customer support, you could have a `TechnicalAgent`, a `BillingAgent`, and a `PolicyAgent`, all coordinated by a main planner that routes questions to the right specialist.

### Building Specialist Agents (2 min)

Let's start with the specialists. First, let's define the tools they'll use.

```python
import os
import re
from dotenv import load_dotenv
from datapizza.tools import tool

load_dotenv()

@tool
def extract_kpi(context: str) -> str:
    """Extracts KPIs and metrics from text."""
    patterns = {
        "Revenue": r"(?:revenue|fatturato)[:\s]*([€$]?\d+[\d,.]*[MBK]?)",
        "Growth": r"(\d+[\d,.]*%)\s*(?:growth|yoy)"
    }
    metrics = [
        f"{name}: {match.group(1)}"
        for name, pattern in patterns.items()
        if (match := re.search(pattern, context, re.IGNORECASE))
    ]
    return " | ".join(metrics) if metrics else "No KPIs found"

@tool
def identify_risks(context: str) -> str:
    """Identifies operational risks."""
    risk_map = {
        "Compliance": ["gdpr", "regulation"],
        "Budget": ["budget", "cost", "funding"]
    }
    risks = [
        name for name, keywords in risk_map.items()
        if any(k in context.lower() for k in keywords)
    ]
    return " | ".join(risks) if risks else "No risks identified"
```
Simple pattern matching, but effective. In production, you'd use more sophisticated extraction.

Now the specialist agents:

```python
from datapizza.agents import Agent
from datapizza.clients import ClientFactory
from datapizza.clients.factory import Provider

# Create shared client for all agents
shared_client = ClientFactory.create(
    provider=Provider.OPENAI,
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0.0,
)

analyst_agent = Agent(
    name="AnalystAgent",
    client=shared_client,
    system_prompt=(
        "You are a KPI extraction specialist. "
        "Use the extract_kpi tool on the provided text and return the result."
    ),
    tools=[extract_kpi],
    max_steps=3
)

risk_agent = Agent(
    name="RiskAgent",
    client=shared_client,
    system_prompt=(
        "You are a risk identification specialist. "
        "Use the identify_risks tool on the provided text and return the result."
    ),
    tools=[identify_risks],
    max_steps=3
)
```

[Highlight the system prompts]

Notice how we define clear roles for each specialist: one extracts KPIs, the other identifies risks. The system prompts guide their behavior without being overly restrictive.

The `max_steps=3` parameter is a safety net. If an agent tries to loop, it will hit this limit and stop, preventing runaway API costs.

### Building the Coordinator (3 min)

Now for the most interesting part—the planner that coordinates everything.

First, we wrap each specialist agent as a tool.

```python
@tool
def run_kpi_analysis(query: str) -> str:
    """Delegates to the KPI analyst."""
    print("  -> Delegating to AnalystAgent...")
    result = analyst_agent.run(query)
    if result.text:
        return result.text
    return "Analysis incomplete"

@tool
def run_risk_assessment(query: str) -> str:
    """Delegates to the risk assessor."""
    print("  -> Delegating to RiskAgent...")
    result = risk_agent.run(query)
    if result.text:
        return result.text
    return "Assessment incomplete"
```

[Show this pattern clearly]

This is the key insight: agents themselves can become tools. The planner calls these tools, which in turn run the other agents.

Now, let's build the planner itself.

```python
strategic_planner = Agent(
    name="StrategicPlanner",
    client=shared_client,
    system_prompt=(
        "You are a strategic consultant. Follow these steps:\n"
        "1. Call run_kpi_analysis on the request\n"
        "2. Call run_risk_assessment on the same request\n"
        "3. Synthesize findings into a final report with:\n"
        "   - **KPI Summary**\n"
        "   - **Risk Areas**\n"
        "   - **Recommendation** (one actionable sentence)\n"
        "Make the report concise and actionable."
    ),
    tools=[run_kpi_analysis, run_risk_assessment],
    max_steps=8
)
```

[Show execution]

```python
scenario = (
    "Fintech product growing 30% YoY, €2M revenue, "
    "needs GDPR compliance roadmap."
)

report = strategic_planner.run(scenario)

# Extract and print the final text
if report.text:
    print(report.text)
else:
    print(report)
```

[Run and show the full delegation chain, an example output I hope to obtain is]:
```
### Final Report

**KPI Summary**
- **Growth Rate**: The fintech product is experiencing a 30% year-over-year growth.
- **Revenue**: Current revenue stands at €2M, indicating a strong upward trajectory.

**Risk Areas**
- **Compliance Risk**: The absence of a GDPR compliance roadmap poses a significant risk.

**Recommendation**
Develop an immediate GDPR compliance roadmap to align with data protection regulations.
```

Watch the flow: the planner receives the task, calls the KPI tool (which runs the `AnalystAgent`), gets the result, calls the risk tool (which runs the `RiskAgent`), gets that result, and finally synthesizes everything into a final report.

[Visual: Agent gif to be shown here]

Three agents, coordinated execution, and a single, unified output. This is multi-agent orchestration in action.

### Preventing Common Pitfalls (1 min)

Multi-agent systems can fail in predictable ways. Here's how to avoid some of the most common issues:

**Problem 1: Infinite loops**
Solution: Always set `max_steps` on every single agent. Always.

**Problem 2: Ambiguous delegation**
Solution: Be explicit in your system prompts. "Call tool X exactly once" is much better than "use tool X if needed."

**Problem 3: Lost context**
Solution: Be specific in your system message: “Invoke tool X exactly once; do not loop.”

**Problem 4: Uncontrolled tool calls**
Solution: Use `terminate_on_text=True` for specialist agents that should run once and then return a result.

[Show side-by-side comparison of good vs bad configurations]

These constraints might seem restrictive, but they're what make multi-agent systems reliable enough for production environments.

## Conclusion (1.5 min)

Alright, let's wrap this up. We designed a three-agent system with specialists and a coordinator. We wrapped those agents into tools to enable delegation. And we learned how to prevent common issues like loops to ensure reliable execution.

This pattern can scale to any level of complexity you need. Five specialists? Ten? Twenty? The coordinator's logic remains the same: delegate, collect, and synthesize.

In the next video, we're building a complete RAG system—retrieval-augmented generation—for answering questions based on your own documents. It's a trendy topic and a super practical stuff.

Before that, try extending this system yourself. Add a third specialist—maybe a `FinancialAgent` or a `TechnicalAgent`—and see how the planner adapts automatically. It's pretty amazing when you see it all work together.

Multi-agent systems are where Datapizza-AI really starts to shine. You're building production-grade AI architectures now, not just simple toy examples.

If you're getting value from this series, smash that like button and drop a comment if you build something cool with this. I'll see you next time!

[Note for narrator: This should feel like a major architectural lesson—we're building systems now, not just apps]
