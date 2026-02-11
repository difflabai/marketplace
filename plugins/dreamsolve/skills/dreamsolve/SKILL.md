---
description: Manage projects, tasks, their files, and run agents in DreamSolve
---

Use DreamSolve to manage projects, tasks, nodes, files, and AI agents.

## Node Management

Nodes are the core building blocks. Company, Project, and Task are the most used. 
Other Types include: Action, Assignment, BusinessUnit, Context, Decision, Delta, Experiment, File, Hypothesis, Issue, KnowledgeTuple, Log, Memory, Module, Package, Person, Problem, Resource, Team.

- **createNode**: Create a node of any type. Requires `type` and `name`. Optional: `description`, `parentId`, `status` (pending/running/completed/onhold), `data`.
- **readNode**: Read a node by ID. Use `includeChildren: true` to fetch child nodes.
- **updateNode**: Update a node's name, description, status, parentId, containerId, or data.
- **deleteNode**: Soft-delete a node and all its children.
- **listChildNodes**: List direct children of a node. Filter with `includeTypes`.
- **searchNodes**: Search by `query` (full-text on name/description), `type`, `status`, `parentId`, `containerId`. Default limit: 50, max: 200.

## Task Tools

- **createTasksFromPlan**: Parse plan text and create multiple sub-nodes within a parent. Pass `nodeId` and `plan` (free-form text or bullet points).
- **assignTask**: Assign a task by `taskId` with either `assigneeId` or `assigneeName`.
- **determineSuitability**: Analyze child nodes using the GenAI Tractability Grid to classify as AI, Human, or Hybrid.

## File Management

- **searchFiles**: Search files associated with a node across S3, Google Drive, and public URLs.
- **readFile**: Read file content (<=1MB returned directly, larger files return download URL). Requires `nodeId` and `fileId`.
- **createFile**: Create a file and associate with a node. Requires `nodeId` and `name`. Optional: `description`, `content`, `mimeType`.
- **updateFile**: Update file metadata or content.

## Agent Management

- **searchAgents**: Discover available AI agents. Filter by `query` or `category` (e.g., Researcher, Planner, Critic).
- **executeAgent**: Run an agent in `conversational` or `node-assignment` mode. Requires `agentId`, `mode`, and `userInput`. Use `nodeId` for node-assignment mode. Use `conversationId` to continue a conversation.

## Autonomous Agent Authentication

The default connection uses OAuth via `mcp-remote`, which opens a browser for the user to sign in. For autonomous agents running on separate systems from their user (e.g., headless servers, CI/CD pipelines, unattended automation), use Ed25519 key pair authentication instead. This replaces the browser-based OAuth flow with a keypair registration and JWT token exchange.

### When to Use This

Use agent authentication when:
- The agent runs headlessly without access to a browser
- The agent operates on a different machine than the user
- The agent needs unattended, long-running access to DreamSolve

For interactive use where the user is present, use the default OAuth flow (no extra setup needed).

### Step 1: Generate an Ed25519 Key Pair

Generate a key pair and extract the raw 32-byte public key as base64url:

```bash
openssl genpkey -algorithm Ed25519 -out agent_private.pem
PK=$(openssl pkey -in agent_private.pem -pubout -outform DER | tail -c 32 | basenc --base64url | tr -d '=')
echo "Public key: $PK"
```

Store `agent_private.pem` securely. It is the agent's identity.

### Step 2: Build the Registration URL

Construct the URL and share it with a human who has access to the target organization:

```
https://dreamsolve.ai/invitations/agent/organization/<ORG_ID>/register?pk=<PK>&name=<AGENT_NAME>
```

- `ORG_ID` — target organization ID (the user can find this in their DreamSolve organization settings)
- `PK` — the base64url public key from Step 1
- `name` — a human-readable label for the agent (optional)

Ask the user to open this URL, sign in, select a role for the agent, and approve. After approval the page displays an `agentUserId` — the user must share this value back.

### Step 3: Authenticate with a Signed JWT

Sign a short-lived JWT with the private key and exchange it for bearer tokens:

```bash
AGENT_USER_ID="<agentUserId from the user>"

# Build and sign the JWT
JWT=$(python3 -c "
import json, time, base64, subprocess, tempfile, os
def b64u(data): return base64.urlsafe_b64encode(data).rstrip(b'=').decode()
header = b64u(json.dumps({'alg':'EdDSA','typ':'JWT'}).encode())
now = int(time.time())
payload = b64u(json.dumps({'sub':'$AGENT_USER_ID','iat':now,'exp':now+300}).encode())
msg = f'{header}.{payload}'.encode()
tmp = tempfile.NamedTemporaryFile(delete=False)
tmp.write(msg); tmp.close()
sig = subprocess.check_output(['openssl','pkeyutl','-sign','-inkey','agent_private.pem','-rawin','-in',tmp.name])
os.unlink(tmp.name)
print(f'{header}.{payload}.{b64u(sig)}')
")

# Exchange for access and refresh tokens
curl -s -X POST https://dreamsolve.ai/api/v1/agents/auth/token \
  -H "Content-Type: application/json" \
  -d "{\"agent_jwt\": \"$JWT\"}"
```

The response contains `access_token` (valid 1 hour, `mcp_` prefix) and `refresh_token` (valid 30 days, `mcpr_` prefix).

### Step 4: Make MCP Tool Calls

Use the access token as a Bearer token on the MCP server endpoint:

```bash
curl -s -X POST https://dreamsolve.ai/api/mcp/server \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0", "id": 1,
    "method": "tools/call",
    "params": {"name": "searchNodes", "arguments": {"query": "my project"}}
  }'
```

All the same MCP tools listed above (createNode, searchNodes, assignTask, etc.) work identically with agent tokens.

### Step 5: Refresh Tokens

Before the access token expires, refresh it:

```bash
curl -s -X POST https://dreamsolve.ai/api/v1/agents/auth/refresh \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\": \"$REFRESH_TOKEN\"}"
```

This returns a new `access_token`. Refresh proactively before the 1-hour expiry to avoid interruptions.

### Deactivation

When an agent is removed from an organization (via organization settings), its key is immediately deactivated. The agent can be re-registered with a new key pair.

## Guidelines

- When creating projects, ask the user for a clear goal description (passed as `desiredState`).
- When creating tasks from a plan, break the plan into actionable items before passing to createTasksFromPlan.
- Use searchNodes to find existing projects and tasks before creating duplicates.
- Use searchAgents to discover agents before executing them.
- Use the default OAuth flow (via `mcp-remote`) when the user is present. Only use agent key pair authentication for headless or unattended operation on a separate system.
- When using agent auth, store the private key and credentials securely. Never log or expose the private key or refresh token.
