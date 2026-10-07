from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os

load_dotenv()

#Initialize the project client with the endpoint and credential
project_client = AIProjectClient(
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential()
)

agent = project_client.agents.create_version(
    agent_name="customer-support-agent",
    definition=PromptAgentDefinition(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        instructions="You are a helpful customer support agent. Answer questions about our products and services.",
        tools=[CodeInterpreterTool()],
    ),
)

print(f"Created agent: {agent.name} (ID: {agent.id}, version: {agent.version})")

#Get an OpenAI client authenticated against the project
openai_client = project_client.get_openai_client()

#Create a conversation (replaces threads in the 1.x SDK)
conversation = openai_client.conversations.create()

#Send a user message and run the agent on the conversation
response = openai_client.responses.create(
    conversation=conversation.id,
    input="Hello, I need help with my order.",
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

#Print the agent's reply
print(response.output_text)
