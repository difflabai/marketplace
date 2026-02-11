---
name: business-model-analysis
description: "Analyze business model, competitive positioning, and go-to-market strategy for a product. Use when: (1) designing a business model for a new product, (2) evaluating competitive positioning, (3) planning go-to-market strategy, (4) assessing strategic risks and moats. Triggers on 'business model', 'go-to-market', 'competitive strategy', 'market positioning', 'business model canvas', 'competitive analysis', 'GTM strategy', 'business model analysis'."
---

# Business Model Analysis

Produce a structured analysis covering business model design, competitive positioning, go-to-market strategy, and strategic risk assessment.

## Business Model Canvas

Analyze each component of the business model:

### 1. Value Proposition

- **Core value:** What specific outcome does the customer get?
- **Unique angle:** What makes this different from alternatives?
- **Value delivery:** How quickly does the customer realize value?
- **Switching cost:** What keeps customers once they start?

### 2. Customer Segments

Reference the ICP analysis for detailed segmentation. Summarize:
- Primary segment and why they're first
- Expansion segments and sequencing
- Anti-personas to avoid

### 3. Channels

How does the product reach customers?

| Channel | Type | Cost | Scale | Speed |
|---------|------|------|-------|-------|
| Organic search/SEO | Inbound | Low | High | Slow |
| Content marketing | Inbound | Low | Medium | Slow |
| Social media | Inbound | Low | Medium | Medium |
| Product-led growth | Inbound | Low | High | Medium |
| Paid search (Google) | Paid | Medium | High | Fast |
| Paid social (LinkedIn, Twitter) | Paid | Medium-High | Medium | Fast |
| Community/word of mouth | Organic | Free | Variable | Slow |
| Partnerships | Alliance | Variable | High | Medium |
| Direct outreach | Outbound | High | Low | Fast |

### 4. Customer Relationships

- **Acquisition:** Self-serve, sales-assisted, or partner-led?
- **Onboarding:** Automated, guided, or white-glove?
- **Support:** Self-serve docs, email, chat, or dedicated?
- **Retention:** Product-driven, relationship-driven, or contract-driven?
- **Expansion:** Natural upsell triggers? Account growth signals?

### 5. Revenue Streams

Reference the monetization analysis for detailed pricing. Summarize:
- Primary revenue model
- Target ARPU and rationale
- Expansion revenue opportunities

### 6. Key Resources

What does DiffLab need to deliver this product?

- **Technical:** Infrastructure, APIs, models, data
- **Human:** Team skills required (eng, design, marketing, support)
- **Intellectual:** Domain expertise, proprietary algorithms, brand
- **Existing assets:** What can be reused? (OpenClaw, ATS, agents, etc.)

### 7. Key Activities

What must happen to make this work?

- **Build:** Core product development
- **Operate:** Running the service (hosting, monitoring, support)
- **Grow:** Customer acquisition and retention activities
- **Improve:** Feedback loops and iteration cycles

### 8. Key Partnerships

- **Technology partners:** APIs, platforms, infrastructure providers
- **Distribution partners:** Who has access to your target customers?
- **Content partners:** Co-marketing, thought leadership
- **Strategic partners:** Complementary products for bundling

### 9. Cost Structure

| Category | Type | Estimate | Notes |
|----------|------|----------|-------|
| Hosting/infrastructure | Variable | | Scales with usage |
| API costs (LLMs, etc.) | Variable | | Per-request costs |
| Team (4 people, 2-4 weeks) | Fixed | | MVP build phase |
| Marketing/acquisition | Variable | | CAC investment |
| Tools and subscriptions | Fixed | | Development and ops |

## Competitive Positioning

### Positioning Map

Use WebSearch to research competitors. Build a positioning analysis:

**Search queries:**
- `"{product category}" alternatives comparison`
- `"{competitor}" strengths weaknesses review`
- `"{product category}" market landscape`
- `"best {product category}" 2025 2026`
- `"{competitor}" vs` — autocomplete reveals common comparisons

### Competitive Matrix

| Factor | Us | Competitor A | Competitor B | Competitor C |
|--------|----|-----------|-----------|-----------|
| Core feature | | | | |
| Price point | | | | |
| Target segment | | | | |
| Key strength | | | | |
| Key weakness | | | | |

### Differentiation Strategy

Choose a primary differentiation axis:

| Strategy | Description | Best When |
|----------|-------------|-----------|
| **Cost leadership** | Cheapest option | Market is commoditized |
| **Feature leadership** | Best/most features | Complex problem space |
| **Niche focus** | Best for specific segment | Underserved vertical exists |
| **UX/simplicity** | Easiest to use | Incumbents are complex |
| **Speed/performance** | Fastest results | Time-to-value matters |
| **AI-native** | Built with AI at core | Incumbents are retrofitting AI |
| **Integration** | Works with existing tools | Ecosystem lock-in opportunity |

### Moat Analysis

Evaluate sustainable competitive advantages:

| Moat Type | Strength (1-5) | Evidence |
|-----------|---------------|----------|
| Network effects | | More users = more value? |
| Switching costs | | How hard to leave? |
| Data advantage | | Proprietary data that improves over time? |
| Brand/trust | | Known and trusted in segment? |
| Technical IP | | Hard-to-replicate technology? |
| Cost advantage | | Structurally cheaper to deliver? |
| Ecosystem lock-in | | Integrations that create stickiness? |

## Go-to-Market Strategy

### Phase 1: Pre-Launch (Stage 3)

- Validate problem and WTP via landing pages and surveys
- Build waitlist from validation respondents
- Establish presence in 1-2 target communities

### Phase 2: Soft Launch (Stage 5)

- Deploy to waitlist in waves
- Focus on activation and early retention
- Collect testimonials and case studies from early users

### Phase 3: Growth (Stage 6)

Primary growth loops to evaluate:

| Loop | Mechanism | Effort | Scalability |
|------|-----------|--------|-------------|
| **Content/SEO** | Publish content → rank → attract users | High | High |
| **Product-led** | Users invite others / share output | Low | High |
| **Community** | Help in forums → build trust → convert | Medium | Medium |
| **Partnerships** | Integrate with popular tools → co-market | Medium | High |
| **Paid acquisition** | Ads → landing page → signup | Low effort, high cost | Medium |

**Recommended primary loop:** [Choose based on product type and target segment]

### Distribution Strategy

- **Self-serve:** Product is simple enough for users to onboard alone
- **Sales-assisted:** Product requires guidance but not a full sales process
- **Partner-led:** Partner handles distribution (if scaling via partnership per Stage 6)

## Risk Assessment

### Key Assumptions to Validate

| Assumption | Validation Method | Stage |
|-----------|-------------------|-------|
| Problem is painful enough | Survey (pain 4+) | 3a |
| Customers will pay $X | Pricing validation | 3b |
| We can build MVP in 2-4 weeks | Build spec review | 4 |
| We can acquire customers affordably | Launch metrics | 5 |
| Customers will retain | 30-day retention | 6 |

### Biggest Risks

Identify the top 3 risks and mitigation strategies:

| Risk | Likelihood (1-5) | Impact (1-5) | Score | Mitigation |
|------|-----------------|-------------|-------|------------|
| [Risk 1] | | | | [Strategy] |
| [Risk 2] | | | | [Strategy] |
| [Risk 3] | | | | [Strategy] |

### What Could Make This a 10x Outcome?

Identify upside scenarios:
- What if adoption exceeds expectations?
- Is there a platform play (others build on top)?
- Could this become a data moat?
- Is there M&A potential?

## Output

Write the analysis to the product's PDE spec directory using the template at `../pde/assets/templates/business-model-analysis.md`. The analysis feeds into Stage 2 (Filter) for scoring mission alignment, competitive edge, and monetization clarity.
