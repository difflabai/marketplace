---
name: icp-analysis
description: "Analyze and define the Ideal Customer Profile for a product or business. Use when: (1) identifying target customer segments, (2) building buyer personas, (3) evaluating product-market fit from a customer perspective, (4) refining who to target for a new product idea. Triggers on 'ideal customer profile', 'target customer', 'customer segments', 'buyer persona', 'who is the customer', 'ICP analysis', 'customer research'."
---

# Ideal Customer Profile Analysis

Produce a structured ICP analysis that identifies, segments, and ranks target customers for a product.

## Analysis Framework

Evaluate potential customers across four dimensions:

### 1. Demographics & Firmographics

**For B2B products:**
- Company size (employees, revenue)
- Industry / vertical
- Geography / markets served
- Growth stage (startup, scale-up, enterprise)
- Technology stack and maturity
- Budget authority and procurement process

**For B2C products:**
- Age range, income bracket
- Occupation / role
- Location (urban/suburban/rural, region)
- Technology comfort level
- Spending patterns in the category

### 2. Psychographics

- Goals and aspirations related to the problem space
- Frustrations and pain points (what keeps them up at night)
- Values that influence purchasing decisions
- Risk tolerance (early adopter vs. late majority)
- Decision-making style (data-driven, peer-influenced, authority-driven)

### 3. Behavioral Signals

- How they currently solve the problem (workarounds, tools, manual processes)
- Where they spend time online (communities, forums, social platforms)
- How they discover new tools (search, peers, analysts, social)
- Purchase triggers (what event makes them start looking)
- Buying cycle length and complexity

### 4. Economic Fit

- Willingness to pay for this category of solution
- Customer acquisition cost feasibility (can we reach them affordably?)
- Expected lifetime value
- Expansion potential (do they grow into higher tiers?)
- Churn risk factors

## Segmentation Methodology

### Step 1: Identify All Potential Segments

Use WebSearch to research:
- Who complains about this problem online (forums, Reddit, Twitter, reviews)
- Job postings that mention the problem or related tools
- Industry reports on the problem space
- Competitor customer bases (who do they target?)

### Step 2: Score and Rank Segments

Rate each segment on a 1-5 scale:

| Factor | Weight | Description |
|--------|--------|-------------|
| Pain severity | 30% | How painful is this problem for them? |
| Reachability | 25% | Can we find and reach them affordably? |
| Willingness to pay | 25% | Will they pay enough to sustain the business? |
| Market size | 20% | Is the segment large enough to matter? |

**Weighted score = (Pain x 0.3) + (Reach x 0.25) + (WTP x 0.25) + (Size x 0.2)**

### Step 3: Define Primary and Secondary Segments

- **Primary segment:** Highest weighted score. This is who you build for first.
- **Secondary segments:** Score within 20% of primary. These are expansion targets.
- **Anti-personas:** Customers who look like a fit but aren't. Explicitly call them out to avoid wasted effort.

### Step 4: Build Customer Profiles

For each segment, create a profile:

```
## [Segment Name]

**One-liner:** [Who they are in one sentence]
**Example:** [A specific example person or company]

**Demographics:** [Key traits]
**Pain:** [Their specific version of the problem]
**Current solution:** [What they use today]
**Purchase trigger:** [What makes them start looking]
**Willingness to pay:** [Price range and model preference]
**Where to find them:** [Channels, communities, platforms]
**Weighted score:** [X.X / 5.0]
```

## Research Approach

Use WebSearch with these query patterns:

- `"{problem}" site:reddit.com` — real user complaints and discussions
- `"{problem}" frustrating OR painful OR hate` — pain validation
- `"{competitor}" reviews pricing` — competitor customer analysis
- `"{industry}" "{problem}" market size` — segment sizing
- `"{role}" "{problem}" tools` — behavioral signals
- `"{problem}" site:linkedin.com` — professional context

## Anti-Persona Identification

Explicitly identify who is NOT a good customer:

- **Too small:** Can't afford the solution or don't have the problem at scale
- **Too large:** Need enterprise features, compliance, or sales cycles you can't support
- **Wrong vertical:** Problem manifests differently and your solution doesn't fit
- **DIY preference:** Strong preference for building in-house, won't buy
- **Low pain:** Have the problem but it's not painful enough to pay to solve

## Output

Write the analysis to the product's PDE spec directory using the template at `../pde/assets/templates/icp-analysis.md`. The analysis feeds directly into the PDE pipeline's Stage 2 (Filter) to validate market fit and competitive edge.
