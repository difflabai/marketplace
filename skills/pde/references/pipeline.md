# PDE Pipeline Reference

Complete reference for all 6 stages of DiffLab's Product Delivery Engine.

## Pipeline Flow

```
INTAKE → FILTER → VALIDATE → BUILD → LAUNCH → REVENUE
  1        2       3a/3b       4        5         6
```

Each stage produces markdown artifacts. High-level aims (`behavior.md`, `evaluation.md`) are separated from implementation details (`implementation-NN/` folders). Human approval required between every stage.

### Spec Structure

```
specs/{product-name}/
├── behavior.md                    # Stage 1: desired behavior + value proposition
├── evaluation.md                  # Stage 2: success criteria for all stages
├── icp-analysis.md                # Post-Stage 1 parallel analysis
├── monetization-analysis.md       # Post-Stage 1 parallel analysis
├── business-model-analysis.md     # Post-Stage 1 parallel analysis
├── validation-plan.md             # Stage 3a
├── validation-results.md          # Stage 3b
├── implementation-01/             # Stage 4-5: first implementation
│   ├── architecture.md            # Tech stack, infrastructure
│   ├── build-spec.md              # MVP features, timeline
│   ├── tests.md                   # Behavioral tests from behavior.md
│   ├── launch-plan.md             # Soft launch strategy
│   └── assets/
├── revenue-report.md              # Stage 6: product-level metrics
└── DECOMMISSIONED.md              # If decommissioned
```

---

## Stage 1: Intake — Behavior Spec

### Purpose

Transform raw market signals into a behavior spec that captures what the product should do, who it's for, and why — without implementation details.

### Input Sources

- Customer conversations (pain points, feature requests, complaints)
- Training insights (workshop discoveries, skill gaps, workflow friction)
- Product ideas from team brainstorming or user feedback

### Research Process

1. **Problem discovery** — What problem exists? How painful is it?
2. **Customer identification** — Who has this problem? How many of them?
3. **Switch motivation** — Why would someone abandon their current approach?
4. **Strategic fit** — How does this connect to DiffLab's mission and capabilities?

Note: Market signals, competitor analysis, and current solution landscape are captured during the parallel analysis phase (business-model-analysis.md), not in the behavior spec.

### Output Quality Checklist

- [ ] Problem is specific and measurable, not vague
- [ ] Target customer is a real segment, not "everyone"
- [ ] Desired behaviors describe outcomes, not implementations
- [ ] Value proposition articulates clear switch motivation (not just "ours is better")
- [ ] Boundaries defined: scope limits, prohibited behaviors, and safety/permission controls
- [ ] No market research, competitor analysis, or market signals (those go in analysis files)
- [ ] No technology choices or architecture details (those go in implementation folders)

---

## Stage 2: Filter — Evaluation

### Purpose

Binary go/no-go decision using 5 criteria. No external spend at this stage.

### Scoring Model

Each criterion is binary (YES/NO). All 5 must pass.

#### Criterion 1: Mission Alignment

Does this product advance DiffLab's mission of AI-powered productivity?

**Pass:** Direct connection to AI, automation, or developer/business productivity
**Fail:** Tangential, requires pivot from core competencies

#### Criterion 2: MVP Feasibility (2-4 weeks, 4 people)

Can a team of 4 build a minimum viable product in 2-4 weeks?

**Pass:** Clear scope, known technologies, reusable infrastructure
**Fail:** Requires deep R&D, regulatory approval, hardware, or unfamiliar domains

**Estimation approach:**
- List core features (3-5 max for MVP)
- Identify reusable components (OpenClaw, ATS, existing agents)
- Estimate weeks per feature with 4 people
- If total > 4 weeks, scope is too large

#### Criterion 3: Market Size (>= $10M TAM or strategic value)

Is the addressable market large enough to justify investment?

**Pass:** TAM >= $10M (from industry reports or bottom-up) OR strategic value (platform play, data moat, partnership gateway)
**Fail:** Niche market with no path to scale, no strategic value

**TAM estimation methods:**
- Top-down: Industry report market size x addressable %
- Bottom-up: Number of potential customers x annual willingness to pay
- Comparable: Similar product revenue x growth rate

#### Criterion 4: Competitive Edge

Does DiffLab have a domain, relationship, or technical advantage?

**Pass:** Proprietary data, existing customer relationships, unique technical capability, first-mover in niche
**Fail:** Commodity market, no differentiation, competing with well-funded incumbents

#### Criterion 5: Clear Monetization

Is there an obvious way to charge money?

**Pass:** SaaS subscription, usage-based pricing, marketplace fee, licensing — with comparable pricing evidence
**Fail:** Unclear revenue model, requires advertising scale, depends on network effects before value

### Decommission Conditions

Any of these present = immediate decommission recommendation:

- **Heavy sales motion:** Requires outbound sales, long sales cycles, enterprise procurement
- **Compliance cycles:** Needs SOC2, HIPAA, FedRAMP, or regulatory approval before launch
- **High validation cost:** >$50K to reach first paying customer
- **Enterprise dependency:** Requires enterprise sales without an identified partner

### Failure Criteria Definition

At the end of Stage 2, define product-specific failure thresholds for Stages 3-6:

```markdown
## Failure Criteria

- Stage 3a: [responses needed] responses, [%] pain threshold
- Stage 3b: [signal type] required to advance
- Stage 5: [%] activation target, [days] to achieve
- Stage 5: Paying users within [days] of launch
- Stage 6: [%] retention at [days]
- Stage 6: Revenue sustainability threshold: $[amount]/month by [days]
```

---

## Stage 3: Validate

See `references/validation.md` for the complete Stage 3 deep-dive.

**Summary:**
- 3a: Problem validation via landing page + survey (pain rating)
- 3b: Solution & WTP via waitlist + pricing + pre-orders
- Highest priority for automation
- Pass/fail criteria are quantitative

---

## Stage 4: Build — Implementation Folder

### Purpose

Define the minimum viable feature set and technical approach for a 2-4 week build. All Stage 4 artifacts go in an `implementation-NN/` folder.

### Output

```
specs/{product-name}/implementation-01/
├── architecture.md    # Tech stack, infrastructure, key decisions
├── build-spec.md      # MVP features, timeline, team allocation
├── tests.md           # Behavioral tests derived from behavior.md
└── assets/
```

### MVP Scoping Rules

1. **Core value only** — What is the one thing this product must do well?
2. **3-5 features max** — If you can't list them on one hand, scope is too large
3. **Ship ugly, learn fast** — No polish, no edge cases, no optimization
4. **Leverage existing infra** — Reuse OpenClaw, ATS, agents, templates before building new

### Architecture (architecture.md)

- Tech stack choices with rationale
- Existing DiffLab assets to leverage
- Key technical decisions and alternatives considered
- Integration points with external services
- Infrastructure and deployment setup

### Behavioral Tests (tests.md)

- Derived directly from desired behaviors in `behavior.md`
- Given/when/then format for each behavior
- Manual verification steps
- Metrics to instrument in production

### Build Spec (build-spec.md)

1. **Core features** with acceptance criteria
2. **Out of scope** (explicit deferral list)
3. **2-4 week timeline** with weekly milestones
4. **Team allocation** (4 people, named roles)

### Timeline Template

- **Week 1:** Core feature 1 + infrastructure setup
- **Week 2:** Core features 2-3 + integration
- **Week 3:** Core features 4-5 + basic testing
- **Week 4:** Bug fixes + soft launch prep (if 4-week build)

---

## Stage 5: Launch — Soft Launch

### Purpose

Deploy to waitlist from Stage 3b. Measure activation, retention, and conversion. The launch plan goes in the current implementation folder as `implementation-NN/launch-plan.md`.

### Soft Launch Process

1. **Deploy** to production environment
2. **Invite waitlist** in waves (not all at once)
   - Wave 1: 10% of waitlist (canary)
   - Wave 2: 50% if canary metrics healthy
   - Wave 3: Remaining 100%
3. **Implement pricing** from Stage 3b validation data
4. **Monitor** daily for first 2 weeks

### Key Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| Activation | Users who complete core action | > 5% of invites |
| Day-1 retention | Users who return day after signup | > 30% |
| Day-7 retention | Users active 7 days post-signup | > 15% |
| Paid conversion | Free users who upgrade to paid | Varies by model |

### Launch Checklist

**Pre-launch:**
- [ ] Production deployment tested
- [ ] Payment processing configured and tested
- [ ] Analytics/metrics tracking verified
- [ ] Onboarding flow works end-to-end
- [ ] Support channel ready (email or chat)
- [ ] Waitlist email templates prepared

**Launch day:**
- [ ] Wave 1 invitations sent
- [ ] Error monitoring active
- [ ] First-hour metrics reviewed

**Post-launch week 1:**
- [ ] Daily metrics review
- [ ] User feedback collected (survey or interviews)
- [ ] Critical bugs triaged and fixed
- [ ] Wave 2 decision made

---

## Stage 6: Revenue & Scale

### Purpose

Track revenue metrics and decide: scale internally or partner.

### Metrics Dashboard

| Metric | Formula | Health Threshold |
|--------|---------|-----------------|
| MRR | Sum of monthly subscription revenue | Growing month-over-month |
| ARR | MRR x 12 | Reference point |
| ARPU | MRR / customers | Stable or growing |
| CAC | Marketing spend / new customers | < 1/3 of LTV |
| LTV | ARPU x avg customer lifespan | > 3x CAC |
| Churn | Lost customers / total customers | < 5% monthly |
| Net retention | (MRR at end - new MRR) / MRR at start | > 100% |

### Scale vs. Partner Decision Framework

**Scale internally when:**
- Retention > 20% at 30 days (product-market fit signal)
- LTV:CAC ratio > 3:1 (healthy unit economics)
- Team has capacity (not overloaded with other products)
- Growth is organic (word of mouth, content, not just paid)

**Partner (rev share / licensing) when:**
- Product works but distribution is the bottleneck
- Market requires sales motion DiffLab can't support
- Revenue plateaus below team sustainability threshold
- Partner has existing customer base and distribution

### Partner Models

| Model | When to Use | Typical Terms |
|-------|-------------|---------------|
| Revenue share | Partner handles sales/support | 20-40% to partner |
| Licensing | Partner white-labels the product | Annual license fee |
| Acquisition | Product is successful but non-core | Negotiate based on ARR multiple |

### Decommission at Stage 6

If after 90 days:
- Revenue plateaus below sustainability → consider partner or decommission
- Retention < 20% at 30 days → major pivot or decommission
- No path to profitability identified → decommission

---

## Cross-Stage Patterns

### Artifact Commit Messages

When pushing artifacts to the PDE repo via `gh api`, use this format for the `message` field:
```
Stage N ({Stage Name}): {product-name} — {brief description}
```

Examples:
- `Stage 1 (Intake): ai-tutor — behavior spec for AI tutoring platform`
- `Analysis: ai-tutor — ICP, monetization, business model`
- `Stage 2 (Filter): ai-tutor — evaluation PASS, all criteria met`
- `Stage 3a (Problem Validation): ai-tutor — landing page and survey deployed`
- `Stage 3b (Solution Validation): ai-tutor — VALIDATED, 12 pre-orders`
- `Stage 4 (Build): ai-tutor — implementation-01 architecture, tests, build spec`
- `Stage 5 (Launch): ai-tutor — implementation-01 soft launch to 200 waitlist users`
- `Stage 6 (Revenue): ai-tutor — Q1 report, $8K MRR, scaling`
- `DECOMMISSIONED: ai-tutor — < 5% activation after 2 weeks`

### Training Feed Loop

```
Training Sessions → Customer Conversations → Problem Discovery → Stage 1 Intake
```

Every workshop, training session, or customer interaction is a potential product signal. Capture these as brief intake notes even if they don't immediately become full product briefs.
