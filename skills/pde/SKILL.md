---
name: pde
description: "Product Delivery Engine — automate DiffLab's 6-stage product pipeline (INTAKE → FILTER → VALIDATE → BUILD → LAUNCH → REVENUE) with specification-driven workflows and human approval gates. Separates high-level product aims (behavior, evaluation) from implementation details (numbered implementation folders). Use when: (1) evaluating a new product idea or market signal, (2) advancing a product through pipeline stages, (3) creating validation landing pages and survey funnels, (4) generating stage artifacts, (5) checking product status, (6) decommissioning a product. Triggers on 'new product idea', 'product brief', 'behavior spec', 'evaluate product', 'validate product', 'landing page', 'survey funnel', 'build spec', 'launch plan', 'revenue report', 'product pipeline', 'advance stage', 'decommission product'."
---

# Product Delivery Engine (PDE)

Specification-driven product pipeline. High-level aims (behavior + evaluation) are separated from implementation details (numbered implementation folders). Each stage produces markdown artifacts committed to the `difflabai/pde` repo with human approval before advancing.

## Quick Start

### New Product

1. User provides product idea or market signal
2. Research the market (WebSearch for trends, competitors, TAM)
3. Generate `behavior.md` from `assets/templates/behavior.md`
4. Write to `specs/{product-name}/behavior.md` in the PDE repo
5. Present spec and ask user to approve
6. On approval, launch 3 parallel analysis subagents (ICP, monetization, business model)
7. Present analysis results, then advance to Filter

### Advance Existing Product

1. User names the product and target stage
2. Read `behavior.md` and `evaluation.md` for high-level context
3. Determine current stage from which artifacts exist (see Check Status)
4. Execute the next stage workflow
5. Present artifact and ask user to approve before advancing

### Check Status

Scan `specs/{product-name}/` and apply the **first matching rule** (top to bottom):

1. `DECOMMISSIONED.md` exists → **Product decommissioned** — stop
2. `revenue-report.md` exists → **Stage 6 active**
3. `implementation-NN/launch-plan.md` exists (highest NN) → **Stage 5 in progress**
4. `implementation-NN/build-spec.md` exists (highest NN) → **Stage 4 in progress**
5. `validation-results.md` exists → **Stage 3 complete** — ready for Build
6. `validation-plan.md` exists → **Stage 3a in progress** — awaiting validation data
7. `evaluation.md` exists → **Stage 2 complete** — ready for Validate
8. All 3 analysis files exist (`icp-analysis.md`, `monetization-analysis.md`, `business-model-analysis.md`) → **Analysis complete** — ready for Filter
9. Only `behavior.md` exists → **Stage 1 complete** — launch parallel analysis

## Spec Structure

Each product has two layers:

**High-level (product-wide, implementation-independent):**
- `behavior.md` — Desired behavior and value proposition
- `evaluation.md` — Success criteria and pass/fail thresholds for every stage
- Analysis files — ICP, monetization, business model
- `validation-plan.md` / `validation-results.md` — Market validation data
- `revenue-report.md` — Revenue metrics and scale decisions

**Implementation-specific (in numbered folders):**
- `implementation-01/architecture.md` — Tech stack, infrastructure decisions
- `implementation-01/build-spec.md` — MVP features, timeline, team allocation
- `implementation-01/tests.md` — Behavioral tests derived from behavior.md
- `implementation-01/launch-plan.md` — Soft launch strategy, metrics setup
- `implementation-01/assets/` — Implementation-specific copies of launch assets (originals live in `specs/{product-name}/assets/`)

## Implementation Routing

**Always work in the current (highest-numbered) implementation folder** unless the user explicitly says they want a new implementation.

To start a new implementation: create `implementation-NN/` where NN is the next number. New implementations inherit the same `behavior.md` and `evaluation.md` — only the implementation approach changes.

## PDE Repo Operations

The PDE repo lives at `https://github.com/difflabai/pde`. All product artifacts go in `specs/{product-name}/`.

### Clone or Update

Before any operation, ensure the repo is present and up-to-date:

```bash
# Clone if not already present
if [ ! -d "pde" ]; then
  git clone https://github.com/difflabai/pde.git
fi
# Always pull latest before writing
cd pde && git pull origin main
```

### Initialize Product Directory

```bash
mkdir -p specs/{product-name}
```

### Commit Stage Artifact

After user approves each stage artifact:

```bash
git pull origin main
git add specs/{product-name}/
git commit -m "{Stage}: {product-name} — {brief description}"
git push origin main
```

If push fails due to conflicts, pull again, resolve conflicts (prefer keeping both changes), and retry.

### Product Naming

Use kebab-case: `ai-code-reviewer`, `spec-validator`, `landing-gen`

### Artifact Map

| Stage | File | Layer |
|-------|------|-------|
| 1 Intake | `behavior.md` | High-level |
| 1+ ICP Analysis | `icp-analysis.md` | High-level |
| 1+ Monetization | `monetization-analysis.md` | High-level |
| 1+ Business Model | `business-model-analysis.md` | High-level |
| 2 Filter | `evaluation.md` | High-level |
| 3a Validate | `validation-plan.md` | High-level |
| 3b Validate | `validation-results.md` | High-level |
| 4 Build | `implementation-NN/architecture.md` | Implementation |
| 4 Build | `implementation-NN/build-spec.md` | Implementation |
| 4 Build | `implementation-NN/tests.md` | Implementation |
| 5 Launch | `implementation-NN/launch-plan.md` | Implementation |
| 6 Revenue | `revenue-report.md` | High-level |
| Decommissioned | `DECOMMISSIONED.md` | High-level |

## Pipeline Stages

### Stage 1: Intake

**Input:** Market signals, customer conversations, training insights, AI trends
**Output:** `specs/{product-name}/behavior.md`

1. Research the problem space using WebSearch — market trends, competitors, customer pain
2. Read the template from `assets/templates/behavior.md`
3. Fill in: problem statement, desired behaviors, boundaries, value proposition, market signals, strategic alignment
4. Focus on what the product should do and must not do, not how to build it
5. Write to PDE repo and present to user
6. **Gate:** User approves behavior spec → launch parallel analysis

### Parallel Analysis (Post-Intake)

After the user approves `behavior.md`, launch 3 parallel analysis subagents. Send all 3 Task tool calls in a **single message** so they run concurrently.

Before launching, verify the companion skills exist:
- `skills/icp-analysis/SKILL.md`
- `skills/monetization-analysis/SKILL.md`
- `skills/business-model-analysis/SKILL.md`

If any skill file is missing, warn the user and skip that analysis.

**Launch these 3 Task calls in one message:**

Task call 1 — ICP Analysis:
- `subagent_type`: `general-purpose`
- `description`: `"ICP analysis for {product-name}"`
- `prompt`: `"You are an Ideal Customer Profile analyst. Read the behavior spec at specs/{product-name}/behavior.md in the difflabai/pde repo. Read the ICP analysis skill instructions from skills/icp-analysis/SKILL.md. Read the output template from skills/pde/assets/templates/icp-analysis.md. Conduct research using WebSearch, then fill in the template — replace all [Placeholder] markers with actual values. Write the result to specs/{product-name}/icp-analysis.md in the PDE repo."`

Task call 2 — Monetization Analysis:
- `subagent_type`: `general-purpose`
- `description`: `"Monetization analysis for {product-name}"`
- `prompt`: `"You are a monetization strategy analyst. Read the behavior spec at specs/{product-name}/behavior.md in the difflabai/pde repo. Read the monetization analysis skill instructions from skills/monetization-analysis/SKILL.md. Read the output template from skills/pde/assets/templates/monetization-analysis.md. Conduct research using WebSearch, then fill in the template — replace all [Placeholder] markers with actual values. Write the result to specs/{product-name}/monetization-analysis.md in the PDE repo."`

Task call 3 — Business Model Analysis:
- `subagent_type`: `general-purpose`
- `description`: `"Business model analysis for {product-name}"`
- `prompt`: `"You are a business model analyst. Read the behavior spec at specs/{product-name}/behavior.md in the difflabai/pde repo. Read the business model analysis skill instructions from skills/business-model-analysis/SKILL.md. Read the output template from skills/pde/assets/templates/business-model-analysis.md. Conduct research using WebSearch, then fill in the template — replace all [Placeholder] markers with actual values. Write the result to specs/{product-name}/business-model-analysis.md in the PDE repo."`

**After all 3 Task results return:**

1. Check each result for success. If any analysis failed, inform the user which one(s) failed and ask whether to retry, skip, or abort
2. Present a summary of each successful analysis to the user
3. Commit all analysis artifacts together: `git commit -m "Analysis: {product-name} — ICP, monetization, business model"`
4. Advance to Stage 2 (Filter)

### Stage 2: Filter

**Input:** `behavior.md` + all 3 analysis files
**Output:** `specs/{product-name}/evaluation.md`

1. Read `behavior.md`, `icp-analysis.md`, `monetization-analysis.md`, and `business-model-analysis.md`
2. Read template from `assets/templates/evaluation.md`
3. Score 5 filter criteria:
   - Use ICP analysis to inform criteria 3 (market size) and 4 (competitive edge)
   - Use monetization analysis to inform criterion 5 (clear monetization)
   - Use business model analysis to inform criteria 1 (mission) and 2 (MVP feasibility)
4. Define product-specific success thresholds for Stages 3-6
5. Define decommission conditions
6. **Gate:** All 5 pass → advance to Validate. Any fail → recommend decommission

### Stage 3: Validate (Highest Priority for Automation)

Asynchronous validation via landing pages and survey funnels. See `references/validation.md` for the complete guide.

#### Stage 3a: Problem Validation

**Output:** `specs/{product-name}/validation-plan.md` + landing page and survey assets

1. Read `behavior.md` and `evaluation.md` for context
2. Read template from `assets/templates/validation-plan.md`
3. Define hypothesis and success criteria (from `evaluation.md` thresholds)
4. Generate landing page from `assets/templates/landing-page.html` — customize with messaging from `behavior.md`
5. Generate survey funnel from `assets/templates/survey-funnel.html`
6. Write assets to `specs/{product-name}/assets/` (shared, not implementation-specific)
7. Provide deployment guidance (Vercel, Netlify, or GitHub Pages)
8. **Gate:** User approves plan and assets → deploy and collect responses

#### Stage 3b: Solution & Willingness to Pay

**Output:** `specs/{product-name}/validation-results.md`

1. Review 3a response data (user provides metrics)
2. If 3a passed, update the landing page in `specs/{product-name}/assets/` — uncomment the Stage 3b sections (solution description, pricing tiers, waitlist form) and fill in values from the behavior spec and validation data
3. Add waitlist form + pre-order mechanism
4. Deploy and collect responses
5. Analyze signal strength against thresholds in `evaluation.md`
6. Read template from `assets/templates/validation-results.md`
7. Document results with metrics and recommendation
8. **Gate:** User approves results → advance to Build or decommission

### Stage 4: Build

**Output:** `specs/{product-name}/implementation-NN/` with `architecture.md`, `build-spec.md`, `tests.md`

1. Read `behavior.md` and `evaluation.md` for high-level requirements
2. Read all analysis and validation artifacts for context
3. Create the implementation folder:
   ```bash
   mkdir -p specs/{product-name}/implementation-01/assets
   ```
4. Read template from `assets/templates/architecture.md` — define tech stack, infrastructure, key decisions
5. Read template from `assets/templates/tests.md` — derive behavioral tests from `behavior.md`
6. Read template from `assets/templates/build-spec.md` — define MVP features, timeline, team allocation
7. Write all 3 files to the implementation folder
8. **Gate:** User approves build spec → begin implementation

### Stage 5: Launch

**Output:** `specs/{product-name}/implementation-NN/launch-plan.md`

1. Read `behavior.md`, `evaluation.md`, and all implementation files
2. Read template from `assets/templates/launch-plan.md`
3. Define soft launch strategy to waitlist from Stage 3b
4. Set pricing from validation results
5. Configure metrics from `evaluation.md` thresholds
6. Create launch checklist
7. Copy validation assets from `specs/{product-name}/assets/` into `implementation-NN/assets/` for the specific launch configuration (originals stay in the shared location)
8. **Gate:** User approves launch plan → execute soft launch

### Stage 6: Revenue & Scale

**Output:** `specs/{product-name}/revenue-report.md` (product-level, not per-implementation)

1. Read all prior artifacts
2. Collect metrics from user (MRR, activation, retention, conversion)
3. Read template from `assets/templates/revenue-report.md`
4. Compare metrics against thresholds in `evaluation.md`
5. Evaluate scale vs. partner decision
6. **Gate:** User approves strategy → execute

## Using Templates

When filling in a template:
1. Read the template file from `assets/templates/`
2. Replace every `[Placeholder]` or `[PLACEHOLDER]` marker with actual values derived from research and prior artifacts
3. For HTML templates with commented-out sections (e.g., `<!-- Stage 3b additions -->`), leave them commented until the relevant stage instructs you to uncomment them
4. Do not leave any placeholder markers in the final artifact

## Human Approval Gate Pattern

Every stage follows this pattern:

1. **Generate** — Read template, replace all placeholders with research and context, write artifact
2. **Present** — Show artifact summary to user with key findings and the recommendation
3. **Decide** — Ask: "Approve {stage} and advance to {next stage}?"
   - **Approve** → commit artifact, advance
   - **Iterate** → user provides specific feedback; incorporate it, regenerate the artifact, and present again (do not advance until approved)
   - **Decommission** → write `DECOMMISSIONED.md` with reason
4. **Commit** — On approval: `git pull`, `git add`, `git commit`, `git push`

## Decommissioning a Product

When a product fails at any stage:

1. Write `specs/{product-name}/DECOMMISSIONED.md` with:
   - Stage where decommissioned
   - Date
   - Reason (which criteria from `evaluation.md` failed)
   - Lessons learned
   - Whether pivot is recommended
2. Commit: `git commit -m "DECOMMISSIONED: {product-name} — {reason}"`

## Research Capabilities

For Intake and Filter stages, use WebSearch to gather:
- **Market trends** — industry reports, analyst forecasts, funding rounds
- **Competitive landscape** — existing products, pricing, feature gaps
- **TAM estimation** — market size from industry reports, bottom-up calculation
- **Customer pain** — forum discussions, review complaints, support threads
- **Technology trends** — AI/ML capabilities enabling new solutions

If WebSearch returns no useful results for a query, try alternative search terms (broader or more specific). If research is still insufficient, note the gap in the artifact and flag it to the user — do not fabricate data.

## Training Feed

Every training session and customer conversation is a potential Intake signal. When the user mentions insights from workshops, training, or customer calls, treat them as Stage 1 input and offer to create a behavior spec.

## References

For detailed stage guidance:
- **Full pipeline details:** Read `references/pipeline.md` — complete criteria, scoring models, and stage workflows
- **Stage 3 validation deep-dive:** Read `references/validation.md` — landing page generation, survey design, analytics setup, deployment, and response analysis
