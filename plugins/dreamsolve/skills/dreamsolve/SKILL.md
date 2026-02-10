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

## Guidelines

- When creating projects, ask the user for a clear goal description (passed as `desiredState`).
- When creating tasks from a plan, break the plan into actionable items before passing to createTasksFromPlan.
- Use searchNodes to find existing projects and tasks before creating duplicates.
- Use searchAgents to discover agents before executing them.
