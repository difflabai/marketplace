---
name: monetization-analysis
description: "Analyze monetization strategy, pricing models, and revenue potential for a product. Use when: (1) choosing a revenue model for a new product, (2) designing pricing tiers, (3) benchmarking against competitor pricing, (4) estimating unit economics, (5) evaluating willingness to pay. Triggers on 'monetization', 'pricing strategy', 'revenue model', 'how to charge', 'pricing tiers', 'unit economics', 'willingness to pay', 'monetization analysis'."
---

# Monetization Analysis

Produce a structured analysis of revenue model options, pricing strategy, and unit economics projections for a product.

## Revenue Model Evaluation

Evaluate which model fits the product. Score each on a 1-5 scale for fit:

### Model Options

| Model | Best For | Consideration |
|-------|----------|---------------|
| **SaaS subscription** | Recurring value, software tools | Predictable revenue, requires retention |
| **Usage-based** | Variable consumption, APIs | Scales with customer, harder to predict |
| **Freemium** | Large market, viral potential | Conversion rate is critical metric |
| **Marketplace/platform fee** | Two-sided markets | Need both supply and demand |
| **One-time purchase** | Standalone tools, templates | Simple but no recurring revenue |
| **Licensing** | Enterprise, white-label | Higher deal size, longer sales cycle |
| **Hybrid** | Complex value chains | Combines models (e.g., subscription + usage) |

### Model Scoring Criteria

| Factor | Question |
|--------|----------|
| Value alignment | Does pricing scale with the value customers receive? |
| Simplicity | Can a customer understand what they'll pay in 10 seconds? |
| Predictability | Can you forecast revenue reliably? |
| Competitive fit | How do competitors charge? Would deviating confuse the market? |
| MVP feasibility | Can you implement this model in a 2-4 week MVP? |

## Pricing Research

### Competitor Benchmarking

Use WebSearch to research competitor pricing:
- `"{competitor}" pricing` — direct pricing pages
- `"{competitor}" pricing plans OR tiers` — tier structure
- `"{product category}" pricing comparison` — aggregated comparisons
- `"{competitor}" vs "{competitor}" pricing` — head-to-head
- `site:g2.com "{product category}" pricing` — review site data

Build a competitor pricing table:

| Competitor | Model | Lowest Tier | Mid Tier | Top Tier | Notes |
|-----------|-------|-------------|----------|----------|-------|
| [Name] | [Type] | $[X]/mo | $[X]/mo | $[X]/mo | [Key differentiator] |

### Value Metric Identification

The value metric is what you charge for. It should:
- **Scale with value** — customers who get more value pay more
- **Be easy to measure** — both you and the customer can track it
- **Be predictable** — customers can estimate their cost before buying
- **Grow naturally** — usage increases as customer succeeds

Common value metrics:
- Per user / per seat
- Per project / per workspace
- Per API call / per transaction
- Per GB / per unit of consumption
- Per feature tier (feature gating)
- Flat rate (simplest, least scalable)

### Willingness to Pay Estimation

Methods to estimate WTP:
1. **Competitor proxy:** If competitors charge $X, market accepts ~$X
2. **Value-based:** Calculate customer ROI, price at 10-20% of value created
3. **Cost-plus:** Your cost + target margin (weak but useful as floor)
4. **Van Westendorp:** Survey asking "too cheap / cheap / expensive / too expensive" price points

## Tier Design

### Three-Tier Framework

Design 3 tiers with clear differentiation:

| Aspect | Starter | Pro | Team/Enterprise |
|--------|---------|-----|-----------------|
| **Target** | Individual / tryout | Power user / SMB | Teams / larger orgs |
| **Price anchor** | Low barrier | "Most popular" | Premium |
| **Feature gating** | Core only | Full features | Full + collaboration + support |
| **Value metric limit** | Low cap | Higher cap | Unlimited or custom |
| **Support** | Self-serve | Email | Priority / dedicated |

### Pricing Psychology

- **Anchor high:** Show the expensive plan first (left-to-right or top-to-bottom)
- **Highlight "popular":** Visual emphasis on the middle tier drives selection
- **Annual discount:** Offer 15-20% off for annual billing to improve cash flow and retention
- **Round numbers:** $49 is better than $47.99 for B2B
- **Free trial over freemium:** When possible, time-limited trial converts better than permanent free tier

## Unit Economics Projection

### Key Metrics to Estimate

| Metric | Formula | Target |
|--------|---------|--------|
| **ARPU** | Monthly revenue / paying customers | Based on tier distribution |
| **CAC** | Marketing + sales cost / new customers | < 1/3 of LTV |
| **LTV** | ARPU x avg customer lifespan (months) | > 3x CAC |
| **Payback period** | CAC / ARPU | < 12 months |
| **Gross margin** | (Revenue - COGS) / Revenue | > 70% for software |

### Estimation Approach

1. **ARPU estimate:** Assume tier distribution (e.g., 60% Starter, 30% Pro, 10% Team) and calculate weighted average
2. **CAC estimate:** Based on planned acquisition channels and their typical costs
3. **LTV estimate:** ARPU x (1 / monthly churn rate). Use industry benchmarks for churn (5% monthly for SMB SaaS is typical)
4. **Break-even:** Total fixed costs / (ARPU - variable cost per customer) = customers needed

### Revenue Scenarios

Model three scenarios:

| Scenario | Monthly customers | ARPU | MRR | ARR |
|----------|------------------|------|-----|-----|
| Conservative | [X] | $[X] | $[X] | $[X] |
| Base | [X] | $[X] | $[X] | $[X] |
| Optimistic | [X] | $[X] | $[X] | $[X] |

## Monetization Risks

Identify and assess:

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Price too high (low conversion) | | | A/B test, validate in Stage 3b |
| Price too low (unsustainable) | | | Monitor unit economics, plan price increase |
| Wrong value metric | | | Watch usage patterns, be ready to pivot |
| Free alternatives emerge | | | Differentiate on quality/support/integration |
| Churn exceeds projections | | | Retention focus, onboarding investment |

## Output

Write the analysis to the product's PDE spec directory using the template at `assets/templates/monetization-analysis.md`. The analysis feeds into Stage 2 (Filter criterion 5: clear monetization) and Stage 3b (pricing tier validation).
