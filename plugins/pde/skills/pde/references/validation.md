# Stage 3: Validation Deep-Dive

Complete guide for the highest-priority automation stage. Covers landing page generation, survey funnel design, analytics setup, deployment, and response analysis.

## Table of Contents

1. [Overview](#overview)
2. [Stage 3a: Problem Validation](#stage-3a-problem-validation)
3. [Stage 3b: Solution & WTP](#stage-3b-solution--willingness-to-pay)
4. [Landing Page Generation](#landing-page-generation)
5. [Survey Funnel Design](#survey-funnel-design)
6. [Analytics & Tracking](#analytics--tracking)
7. [Deployment](#deployment)
8. [Response Analysis](#response-analysis)
9. [Traffic Generation](#traffic-generation)

---

## Overview

Stage 3 validates two things sequentially:
1. **3a — Problem exists and is painful** (landing page → survey with pain rating)
2. **3b — Customers will pay for a solution** (landing page → waitlist + pricing + pre-orders)

Both substages are asynchronous — deploy assets, drive traffic, collect responses, then analyze. This is not a synchronous conversation.

### Timeline

- **3a:** Deploy landing page + survey → 2-4 weeks of data collection
- **3b:** Deploy updated landing page with solution + pricing → 2-4 weeks of data collection
- Total Stage 3 duration: 4-8 weeks

---

## Stage 3a: Problem Validation

### Hypothesis

State the problem hypothesis clearly:

> "{Target customer} experiences {specific problem} when {context}, and rates this pain at 4+ out of 5."

### Landing Page Components

The Stage 3a landing page focuses on the problem, not the solution:

1. **Headline** — Name the problem directly ("Tired of X?", "Still struggling with Y?")
2. **Pain point list** — 3-4 specific frustrations the target customer recognizes
3. **Social proof** (optional) — Stats, quotes, or data showing the problem is widespread
4. **CTA** — "Share your experience" linking to the survey funnel
5. **No solution reveal** — Don't describe what you're building yet

### Survey Questions

**Required questions:**

| # | Question | Type | Purpose |
|---|----------|------|---------|
| 1 | What's your role/title? | Text | Validate target customer |
| 2 | How painful is {problem} for you? | 1-5 scale | Core metric |
| 3 | What are you currently using to handle this? | Text | Understand alternatives |
| 4 | Email (optional) | Email | Build waitlist for 3b |

**Optional questions (keep survey short — 4-6 questions max):**

| Question | Purpose |
|----------|---------|
| How often do you encounter this problem? | Frequency validation |
| How much time do you spend on this weekly? | Quantify pain |
| What would an ideal solution look like? | Solution ideation |

### Pass Criteria

| Metric | Threshold | Status |
|--------|-----------|--------|
| Total responses | >= 30 | Required |
| Pain rated 4 or 5 | >= 60% of responses | Required |
| Email opt-in | >= 40% | Bonus (builds waitlist) |

### Fail Outcomes

- **< 30 responses after adequate promotion:** Traffic problem. Try different channels before decommissioning.
- **>= 30 responses but < 60% rate 4+:** Problem isn't painful enough. Decommission or pivot the problem framing.

---

## Stage 3b: Solution & Willingness to Pay

### Hypothesis

> "{Target customer} will {sign up for waitlist / select a pricing tier / pre-order} when presented with {solution description} at {price point}."

### Landing Page Updates for 3b

Enhance the 3a landing page with:

1. **Solution section** — What you're building and how it solves the problem
2. **Feature highlights** — 3-4 key capabilities (not exhaustive)
3. **Pricing tiers** — 2-3 options with clear value differentiation
4. **Waitlist form** — Email + name for interest signal
5. **Pre-order button** — Strongest signal (payment commitment)

### Pricing Tier Design

Use 3 tiers:

| Tier | Strategy | Example |
|------|----------|---------|
| Starter | Low barrier, limited features | $19/mo — Core feature only |
| Pro | Most popular, full features | $49/mo — All features |
| Team | Premium, collaboration | $99/mo — Team features + support |

**Pricing research:**
- Check competitor pricing (from Stage 1 brief)
- Survey 3a respondents directly if sample is large enough
- Price slightly below competitors for new market entry

### Signal Strength Interpretation

| Signal | Evidence | Decision |
|--------|----------|----------|
| **Strong** | Pre-orders with payment or deposit | Advance to Build |
| **Validated** | Waitlist signups + pricing tier selection | Advance to Build |
| **Weak** | Waitlist signups only, no pricing engagement | Iterate messaging/pricing or decommission |
| **Fail** | Low traffic, minimal signups | Decommission |

### Quantitative Thresholds

Define before launching 3b:
- Minimum waitlist signups: typically >= 50
- Minimum pricing engagement: >= 30% of visitors view pricing
- Pre-order target: >= 5 (any pre-orders are strong signal for early-stage)

---

## Landing Page Generation

### Using the Template

Read `assets/templates/landing-page.html` and customize:

1. **Replace placeholder text:**
   - `[Product Name]` → actual product name
   - `[Value Proposition]` → one-sentence hook from product brief
   - `[Pain point 1/2/3]` → from product brief's problem statement
   - `[survey-funnel-url]` → URL where survey will be deployed

2. **Customize styling:**
   - Primary color to match product identity
   - Font choice (system fonts are fine for validation)
   - Hero image or illustration (optional — text-only is fine for validation)

3. **Add analytics tracking** (see Analytics section below)

### Landing Page Best Practices

- **Single CTA** — One clear action per page (survey for 3a, waitlist/pre-order for 3b)
- **Above the fold** — Headline + CTA visible without scrolling
- **Mobile-first** — Most traffic will be mobile
- **Fast loading** — No frameworks, minimal JS, inline CSS
- **No navigation** — Landing pages don't need headers/footers/menus
- **Social proof** — Even a single stat or testimonial increases conversion

### 3b Landing Page Additions

For Stage 3b, add to the 3a page:

```html
<!-- Solution section -->
<section class="solution">
    <h2>Introducing [Product Name]</h2>
    <p>[Solution description]</p>
    <ul>
        <li>[Feature 1]</li>
        <li>[Feature 2]</li>
        <li>[Feature 3]</li>
    </ul>
</section>

<!-- Pricing section -->
<section class="pricing">
    <div class="tier">
        <h3>Starter</h3>
        <p class="price">$X/mo</p>
        <ul>[features]</ul>
        <a href="#waitlist" class="cta">Join Waitlist</a>
    </div>
    <!-- Repeat for each tier -->
</section>

<!-- Waitlist form -->
<section id="waitlist">
    <h2>Get Early Access</h2>
    <form id="waitlistForm">
        <input type="text" name="name" placeholder="Name" required>
        <input type="email" name="email" placeholder="Email" required>
        <select name="tier">
            <option>Which plan interests you?</option>
            <option value="starter">Starter ($X/mo)</option>
            <option value="pro">Pro ($X/mo)</option>
            <option value="team">Team ($X/mo)</option>
        </select>
        <button type="submit">Join Waitlist</button>
    </form>
</section>
```

---

## Survey Funnel Design

### Using the Template

Read `assets/templates/survey-funnel.html` and customize:

1. Replace `[problem]` with the specific problem from the product brief
2. Adjust questions to match the product domain
3. Keep to 4-6 questions maximum (completion rate drops with more)
4. Ensure pain rating scale (1-5) is always included

### Survey Best Practices

- **Short** — 4-6 questions, 2-3 minutes to complete
- **Required questions first** — Pain rating and role before optional fields
- **One question per screen** (if multi-step) — reduces cognitive load
- **Progress indicator** — "Question 2 of 5" increases completion
- **Thank you page** — Confirm submission and set expectations
- **Email last** — Asking for email after they've invested time increases opt-in

### Response Collection Options

Choose one backend for collecting responses:

| Platform | Complexity | Cost | Best For |
|----------|-----------|------|----------|
| Google Sheets (via Apps Script) | Low | Free | Quick validation |
| Airtable form | Low | Free tier | Structured data |
| Typeform | Medium | Free tier (10 responses/mo) | Better UX |
| Custom endpoint | High | Varies | Full control |

**Google Sheets approach (recommended for speed):**

1. Create a Google Sheet with columns matching form fields
2. Deploy a Google Apps Script web app that accepts POST requests
3. Point the survey form's submit action to the Apps Script URL
4. Responses appear in the spreadsheet in real-time

---

## Analytics & Tracking

### Minimum Tracking Requirements

| Event | When | What to Capture |
|-------|------|-----------------|
| Page view | Landing page loads | Source, device, location |
| CTA click | User clicks survey/waitlist button | Button label |
| Survey start | User begins survey | Timestamp |
| Survey complete | User submits survey | All responses |
| Waitlist signup | User joins waitlist | Email, tier selection |
| Pre-order | User commits to purchase | Amount, tier |

### Google Analytics 4 Setup

Add to landing page `<head>`:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

Track custom events:

```javascript
// CTA click
gtag('event', 'cta_click', { event_category: 'engagement', event_label: 'survey_start' });

// Survey completion
gtag('event', 'survey_complete', { event_category: 'conversion', pain_rating: rating });

// Waitlist signup
gtag('event', 'waitlist_signup', { event_category: 'conversion', tier: selectedTier });
```

### PostHog Alternative

If using PostHog (self-hostable, more privacy-friendly):

```html
<script>
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
  posthog.init('phc_XXXXXXXXXX', {api_host: 'https://app.posthog.com'});
</script>
```

---

## Deployment

### Recommended Platforms

| Platform | Setup Time | Cost | Best For |
|----------|-----------|------|----------|
| GitHub Pages | 5 min | Free | Static HTML, already on GitHub |
| Vercel | 5 min | Free | Static + serverless functions |
| Netlify | 5 min | Free | Static + form handling built-in |

### GitHub Pages Deployment

Simplest option since PDE repo is already on GitHub:

1. Place HTML files in `specs/{product-name}/assets/`
2. Enable GitHub Pages in repo settings (source: main branch)
3. Landing page available at `https://difflabai.github.io/pde/specs/{product-name}/assets/landing-page.html`

**Note:** GitHub Pages URL is long. Use a URL shortener or custom domain for traffic campaigns.

### Vercel Deployment

For more control (serverless functions for form handling):

```bash
cd specs/{product-name}/assets/
npx vercel --prod
```

### Netlify Deployment

Netlify has built-in form handling (no backend needed):

Add `netlify` attribute to forms:
```html
<form name="survey" netlify>
```

Responses appear in Netlify dashboard automatically.

---

## Response Analysis

### Stage 3a Analysis

After collecting >= 30 responses:

1. **Calculate pain distribution:**
   ```
   Rating 1: X responses (X%)
   Rating 2: X responses (X%)
   Rating 3: X responses (X%)
   Rating 4: X responses (X%)
   Rating 5: X responses (X%)

   Pain 4+: X responses (X%) — threshold: >= 60%
   ```

2. **Segment by role** — Is pain concentrated in target customer segment?

3. **Analyze workarounds** — What are people currently using? Common themes?

4. **Email opt-in rate** — How many want to hear about a solution?

### Stage 3b Analysis

After collecting sufficient responses:

1. **Traffic metrics:**
   - Total visitors
   - Bounce rate
   - Time on page
   - Pricing section scroll depth

2. **Conversion funnel:**
   ```
   Visitors → Pricing viewed → Waitlist signup → Tier selected → Pre-order
   X          X (X%)           X (X%)           X (X%)          X (X%)
   ```

3. **Signal classification:**
   - Count pre-orders → any = strong signal
   - Count waitlist + tier selection → strong if > 10% of visitors
   - Count waitlist-only → moderate signal
   - Low overall engagement → weak/fail

4. **Pricing validation:**
   - Which tier is most selected?
   - Is there a pricing sensitivity pattern?
   - Compare to competitor pricing from Stage 1

### Results Documentation

Write findings to `validation-results.md` using the template. Include:
- Raw metrics (visitors, responses, conversions)
- Signal strength classification
- Pain distribution chart (for 3a)
- Conversion funnel (for 3b)
- Recommendation (advance/iterate/decommission)
- Lessons learned

---

## Traffic Generation

### Free Channels

| Channel | Effort | Expected Volume | Best For |
|---------|--------|----------------|----------|
| Personal network | Low | 20-50 | Quick initial responses |
| LinkedIn post | Low | 50-200 | B2B products |
| Reddit (relevant subreddit) | Medium | 50-500 | Developer/niche products |
| Hacker News (Show HN) | Medium | 100-1000 | Technical products |
| Twitter/X thread | Low | 50-200 | Tech audience |
| Product Hunt (upcoming) | Medium | 100-500 | Consumer/prosumer |

### Paid Channels (if needed)

| Channel | Minimum Budget | Expected CPC | Best For |
|---------|---------------|-------------|----------|
| Google Ads | $200 | $1-5 | High-intent search |
| LinkedIn Ads | $500 | $5-15 | B2B targeting |
| Facebook/Instagram | $200 | $0.50-3 | Consumer products |

### Traffic Generation Tips

- **Start free** — Personal network + 1-2 organic channels
- **Test messaging** — Try different headlines in posts
- **Track sources** — Use UTM parameters (`?utm_source=linkedin&utm_campaign=validation`)
- **Adequate promotion period** — 2-4 weeks minimum before concluding insufficient traffic
- **Don't buy vanity traffic** — Prefer fewer, targeted visitors over high volume from wrong audience
