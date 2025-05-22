import os

from dotenv import load_dotenv
from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from smolagents import (CodeAgent, InferenceClientModel, LiteLLMModel,
                        ToolCallingAgent, VisitWebpageTool, WebSearchTool)

from src.visit_page import visit_webpage as visit_webpage

###############
print("")

load_dotenv()
LLM_API_TOKEN = os.getenv('LLM_API_TOKEN')
MODEL_ID = os.getenv('MODEL_ID')
LLM_API_BASE = os.getenv('LLM_API_BASE')

PHOENIX_COLLECTOR_ENDPOINT = os.getenv('PHOENIX_COLLECTOR_ENDPOINT')


#############

print("\n▁▁▁▂▄▆█ 🌍 Web Search Tool 🌍 █▆▄▂▁▁▁\n")

print("\n")
print(f"🤖 Model:           {MODEL_ID}")
print(f"🏭 LM API:          {LLM_API_BASE}")
print(f"🔭 Telemetry:       {PHOENIX_COLLECTOR_ENDPOINT}")
print("\n")

########### Telemetry

### USING ARIZE CLOUD
# tracer_provider = None
if PHOENIX_COLLECTOR_ENDPOINT and "app.phoenix.arize.com" in PHOENIX_COLLECTOR_ENDPOINT:
    from arize.otel import register
    register(
        space_id = os.getenv('PHOENIX_SPACE_ID'),
        api_key = os.getenv('PHOENIX_API_KEY'),
        project_name = "smolchat", # name this to whatever you would like
    )

## Local / Docker
elif PHOENIX_COLLECTOR_ENDPOINT and ":6006" in PHOENIX_COLLECTOR_ENDPOINT:
    from phoenix.otel import register
    register(
      endpoint=PHOENIX_COLLECTOR_ENDPOINT,
      project_name="smolchat", # Default is 'default'
      verbose=True,
      auto_instrument=True
    )

######

model = LiteLLMModel(model_id=MODEL_ID, api_base=LLM_API_BASE, api_key=LLM_API_TOKEN) # Could use 'gpt-4o'

web_agent = ToolCallingAgent(
    tools=[WebSearchTool(), visit_webpage],
    model=model,
    max_steps=10,
    name="web_search_agent",
    description="Runs web searches for you."
)

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[web_agent],
    additional_authorized_imports=["time", "numpy", "pandas"]
)

print("\n⟫⟫ Please provide a query")
print("⟫⟫ For example, 'What is today's forecast for Charlotte, North Carolina?'\n")
while True:
    query = input("🔎: ")
    answer = manager_agent.run(query)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    print(answer)
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")