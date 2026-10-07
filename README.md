# Customer Support Agent (Microsoft Foundry)

A small Python script that creates an agent in a Microsoft Foundry project, sends it one message, and prints the reply.

`main.py` does three things:

1. Creates (or adds a new version of) an agent named `customer-support-agent` that uses the `gpt-5` deployment and the Code Interpreter tool.
2. Starts a conversation with the agent.
3. Sends `"Hello, I need help with my order."` and prints the agent's answer.

It uses `azure-ai-projects` **2.x**. Code samples written for 1.x (`agents.create_agent`, `agents.threads`, `agents.runs`) won't work with this version.

## Prerequisites

- [VS Code](https://code.visualstudio.com/) with the **Python** extension (`ms-python.python`)
- Python 3.10 or later (tested with 3.13)
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
- An Azure subscription with:
  - a Foundry project
  - a model deployment in that project (this repo uses `gpt-5`)
  - the **Azure AI User** role (or higher) on the project for your account

## 1. Open the folder in VS Code

**File → Open Folder…** and choose the `Agent` folder (the one with `main.py`).

Open a terminal in VS Code with **Terminal → New Terminal** (`` Ctrl+` ``). All commands below run there.

## 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Your prompt should now start with `(.venv)`.

If PowerShell says running scripts is disabled, run this once and then activate again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

On macOS/Linux, activate with `source .venv/bin/activate` instead.

Then tell VS Code to use this environment: **Ctrl+Shift+P → Python: Select Interpreter** and pick the one under `.venv`.

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## 4. Sign in to Azure

```powershell
az login
```

If your account has more than one tenant or subscription, pick the one that contains your Foundry project:

```powershell
az account set --subscription "<subscription-name-or-id>"
```

The script uses `DefaultAzureCredential`, which picks up this login, so you don't need an API key.

## 5. Create the `.env` file

Create a file named `.env` next to `main.py`:

```
PROJECT_ENDPOINT=https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
MODEL_DEPLOYMENT_NAME=gpt-5
```

**Where to find `PROJECT_ENDPOINT`:** in the [Foundry portal](https://ai.azure.com), open your project. The **Overview** page shows the project endpoint.

It must be the **project** endpoint (`...services.ai.azure.com/api/projects/...`). The model's endpoint from the deployment page (`...cognitiveservices.azure.com/`) is for the plain OpenAI client and gives a `404 Resource not found` here.

You can also get it from the CLI:

```powershell
az resource list --resource-type "Microsoft.CognitiveServices/accounts/projects" --query "[].id" -o tsv
az resource show --ids "<id-from-above>" --query "properties.endpoints" -o json
```

**`MODEL_DEPLOYMENT_NAME`** is the deployment name shown under **Models + endpoints** in your project. It may differ from the model name.

`.env` is listed in `.gitignore`, so it won't be committed.

## 6. Run it

From the terminal:

```powershell
python main.py
```

Or open `main.py` and click the **▶ Run Python File** button at the top right of the editor.

Expected output (the reply text will vary):

```
Created agent: customer-support-agent (ID: customer-support-agent:1, version: 1)
I'm happy to help. Could you share:
- Your order number
...
```

The agent also appears in the Foundry portal under your project's **Agents** page.

## Debugging in VS Code (optional)

To step through the code, set a breakpoint by clicking left of a line number in `main.py`, then press **F5** and choose **Python Debugger → Python File**.

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `ValueError: Parameter 'endpoint' must not be None.` | `.env` missing or not next to `main.py` | Create `.env` as in step 5 and run from the `Agent` folder |
| `ResourceNotFoundError: (404) Resource not found` | `PROJECT_ENDPOINT` is the `cognitiveservices.azure.com` endpoint | Use the project endpoint (`.../api/projects/<project-name>`) |
| `DefaultAzureCredential failed to retrieve a token` | Not signed in | Run `az login` |
| `(401)` / `(403)` / `PermissionDenied` | Your account lacks a role on the project | Ask for **Azure AI User** on the project, or sign in to the right tenant |
| `AttributeError: 'AgentsOperations' object has no attribute 'threads'` (or `create_agent`) | 1.x sample code with the 2.x SDK | Use `conversations` / `responses` as in `main.py` |
| `ModuleNotFoundError` | Wrong interpreter selected | Activate `.venv` and select it via **Python: Select Interpreter** |

## Notes

- Each run adds a new version of `customer-support-agent` if the definition changed; it does not create a separate agent.
- To continue the conversation, call `openai_client.responses.create(...)` again with the same `conversation.id`.
