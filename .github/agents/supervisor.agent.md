# Supervisor Agent

## Overview

The **Supervisor Agent** is the central orchestrator of the phi-agents multi-agent system. It acts as an intelligent coordinator that:

- **Routes queries** to specialist agents (Web Search, Finance, Weather, SQL, API)
- **Synthesizes results** from multiple agents into cohesive answers
- **Ensures consistency** and quality across agent responses
- **Manages delegation** by analyzing queries and determining optimal agent involvement
- **Provides oversight** of the entire team's performance

## Purpose

Modern AI systems often require multiple specialized capabilities. The supervisor agent solves the coordination problem by:

1. **Understanding query intent** — determining which specialists are needed
2. **Delegating efficiently** — routing to appropriate agents without unnecessary calls
3. **Synthesizing intelligently** — combining results with cross-domain insights
4. **Maintaining quality** — ensuring sources are cited and answers are well-organized
5. **Learning patterns** — improving routing decisions over time

## Capabilities

The supervisor can handle:

- **Multi-domain queries**: "Compare financial performance of tech companies with latest AI news"
- **Complex routing**: "Find flights to NYC and check weather predictions for next week"
- **Data synthesis**: "Which F1 driver had the best 2024 season by wins and sponsor sentiment?"
- **Ambiguous requests**: Asks clarifying questions when query intent is unclear
- **Source attribution**: Always cites which agent contributed each part of the answer

## How It Works

### Query Analysis
When a query arrives, the supervisor:
1. Parses the query to identify domains (finance, weather, web, database, API)
2. Determines which agents should participate
3. Formulates specific questions for each agent
4. Waits for responses from all relevant agents

### Response Synthesis
After agents respond:
1. Collects all results with source attribution
2. Identifies connections across domains
3. Organizes information logically (tables for data, narrative for context)
4. Provides final answer with comprehensive sources

### Agent Team
The supervisor coordinates with:

| Agent | Purpose | Example Domains |
|-------|---------|-----------------|
| **Web Search Agent** | Real-time web searches | News, trends, current events |
| **Finance Agent** | Stock data & analyst insights | Market data, recommendations |
| **Weather Agent** | Weather forecasts & historical data | Climate, forecasts, patterns |
| **SQL Agent** | Database queries | Formula 1 data, structured queries |
| **API Agent** | HTTP API calls | Custom endpoints, microservices |

## Usage Examples

### Example 1: Multi-Domain Query
```
User: "What's the latest news about Tesla and how is the stock performing?"

Supervisor routes to:
- Web Search Agent → finds recent Tesla news
- Finance Agent → gets current stock price and analyst sentiment
→ Synthesizes: "Tesla stock is at $X (source: Finance Agent). Latest news: ... (source: Web Search)"
```

### Example 2: Complex Routing
```
User: "Find the best route to London next week considering weather"

Supervisor routes to:
- Web Search Agent → travel options
- Weather Agent → London forecast for next week
→ Synthesizes: "Recommended departure day is Tuesday (weather: clear). Routes: ..."
```

### Example 3: Data Integration
```
User: "Which F1 team won most races in 2023 and what's their latest news?"

Supervisor routes to:
- SQL Agent → queries F1 race results
- Web Search Agent → finds latest team news
→ Synthesizes: "Red Bull won 21 races in 2023. Latest: ..."
```

## Running the Supervisor

### Standalone Test
```bash
python src/phi_agents/functions/supervisor_agent.py
```

### In Streamlit UI
The supervisor is available as the primary agent in `run_agents.py`:
```bash
streamlit run src/phi_agents/run_agents.py --server.port 8501
```

### As FastAPI Endpoint
Deploy through `my-mainapp.py` with supervisor routing:
```bash
uvicorn src.phi_agents.app.my-mainapp:app --env-file .env --reload
```

## Configuration

### Model Selection
Switch the underlying model in `supervisor_agent.py`:

```python
# Default: OpenAI GPT-4o
model=OpenAIChat(id="gpt-4o"),

# Alternative: HuggingFace
# model=HuggingFace(id="meta-llama/Llama-3.2-3B-Instruct"),

# Alternative: Google Gemini
# model=Gemini(id="gemini-1.5-flash"),
```

### Customizing Instructions
Edit the `instructions` list in `supervisor_agent.py` to change routing logic:

```python
instructions=[
    "Your custom instruction 1",
    "Your custom instruction 2",
    # ... add domain-specific rules
]
```

## Design Patterns

The supervisor follows the agent factory pattern used throughout phi-agents:

```python
def supervisor_agent(model_id: str = "openai:gpt-4o"):
    """Factory function that returns a configured Agent instance."""
    supervisor = Agent(
        name="Supervisor",
        role="...",
        model=OpenAIChat(...),
        instructions=[...],
        show_tool_calls=True,
        markdown=True,
    )
    return supervisor
```

## Integration with Agent Team

In `run_agents.py`, the supervisor can be:

1. **Added as team lead**: Supervisor coordinates all other agents
   ```python
   agent_team = Agent(
       model=OpenAIChat(id="gpt-4o"),
       team=[supervisor_agent(), web_agent(), finance_agent(), ...],
       instructions=[...],
   )
   ```

2. **Used as standalone orchestrator**: Supervisor calls other agents internally
   ```python
   supervisor = supervisor_agent()
   response = supervisor.run("Your query here", stream=True)
   ```

## Performance Tips

- **Minimize agent calls**: Supervisor should only route to necessary agents
- **Cache results**: Reuse responses for repeated queries within sessions
- **Monitor latency**: Track which agent combinations are slowest
- **Batch requests**: Group queries to reduce round trips
- **Stream responses**: Use `stream=True` for faster perceived performance

## Future Enhancements

Potential improvements to the supervisor agent:

- [ ] Learn routing patterns from user feedback
- [ ] Implement result caching for common queries
- [ ] Add cost optimization (route to cheaper agents when possible)
- [ ] Support async agent execution (parallel instead of sequential)
- [ ] Add confidence scoring for delegated tasks
- [ ] Implement fallback routing if primary agent fails

---

**File**: `src/phi_agents/functions/supervisor_agent.py`  
**Framework**: agno  
**Dependencies**: openai, huggingface_hub (optional), google-generativeai (optional)
