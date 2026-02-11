# [Product Name] — Validation Plan

**Stage:** 3 — VALIDATE
**Date:** YYYY-MM-DD
**Status:** [Planning / 3a In Progress / 3a Complete / 3b In Progress / Complete]

---

## Stage 3a: Problem Validation

### Hypothesis

> "[Target customer] experiences [specific problem] when [context], and rates this pain at 4+ out of 5."

### Landing Page

- **URL:** [To be deployed]
- **File:** `assets/landing-page.html`
- **Headline:** [Problem-focused headline]
- **Pain points:**
  1. [Pain point 1 from product brief]
  2. [Pain point 2]
  3. [Pain point 3]
- **CTA:** "Share your experience" → survey funnel

### Survey Funnel

- **URL:** [To be deployed]
- **File:** `assets/survey-funnel.html`
- **Questions:**
  1. What's your role? (text)
  2. How painful is [problem] for you? (1-5 scale)
  3. What are you currently using to handle this? (text)
  4. Email — optional (email)

### Success Criteria

| Metric | Target | Actual |
|--------|--------|--------|
| Total responses | >= 30 | |
| Pain rated 4 or 5 | >= 60% | |
| Email opt-in | >= 40% (bonus) | |

### Traffic Strategy

| Channel | Action | Expected Reach |
|---------|--------|---------------|
| [Channel 1] | [Specific action] | [Estimate] |
| [Channel 2] | [Specific action] | [Estimate] |
| [Channel 3] | [Specific action] | [Estimate] |

### Deployment

- **Platform:** [GitHub Pages / Vercel / Netlify]
- **Analytics:** [Google Analytics / PostHog]
- **Response collection:** [Google Sheets / Airtable / Netlify Forms]
- **Launch date:** [Date]
- **Data collection period:** [X weeks]

---

## Stage 3b: Solution & Willingness to Pay

### Hypothesis

> "[Target customer] will [sign up / select tier / pre-order] when presented with [solution] at [price point]."

### Solution Presentation

**Product description:** [One paragraph describing the solution]

**Key features:**
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

### Pricing Tiers

| Tier | Price | Features | Target Segment |
|------|-------|----------|---------------|
| Starter | $[X]/mo | [Core feature] | [Who] |
| Pro | $[X]/mo | [All features] | [Who] |
| Team | $[X]/mo | [Team features + support] | [Who] |

### Landing Page Updates

- Add solution section with features
- Add pricing tier display
- Add waitlist form with tier selection
- Add pre-order mechanism (optional)

### Success Criteria

| Signal | Evidence | Threshold |
|--------|----------|-----------|
| Strong | Pre-orders with payment | >= [X] |
| Validated | Waitlist + tier selection | >= [X] signups, [X]% select tier |
| Weak | Waitlist only | Iterate or decommission |
| Fail | Low traffic/signups | Decommission |

### Timeline

- **3b launch date:** [Date]
- **Data collection period:** [X weeks]
- **Review date:** [Date]

---

## Checklist

### 3a Checklist

- [ ] Landing page customized from template
- [ ] Survey funnel customized from template
- [ ] Analytics tracking configured
- [ ] Response collection backend set up
- [ ] Deployed to hosting platform
- [ ] Traffic campaigns launched
- [ ] Responses collected (>= 30)
- [ ] Results analyzed
- [ ] Decision documented

### 3b Checklist

- [ ] Landing page updated with solution + pricing
- [ ] Waitlist form integrated
- [ ] Pre-order mechanism configured (optional)
- [ ] Redeployed
- [ ] Traffic campaigns launched
- [ ] Responses collected
- [ ] Signal strength classified
- [ ] Results documented in validation-results.md
- [ ] Decision: advance / iterate / decommission
