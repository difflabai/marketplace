# [Product Name] — Launch Plan

**Stage:** 5 — LAUNCH
**Date:** YYYY-MM-DD
**Launch date:** YYYY-MM-DD
**Status:** [Planning / Pre-Launch / Live / Post-Launch Review]

---

## Soft Launch Strategy

### Waitlist Deployment

- **Waitlist size:** [X] (from Stage 3b)
- **Wave 1 (canary):** [X] users ([X]%) — [Date]
- **Wave 2:** [X] users ([X]%) — [Date, if Wave 1 metrics healthy]
- **Wave 3 (full):** Remaining users — [Date]

### Pricing

From Stage 3b validation:

| Tier | Price | Features |
|------|-------|----------|
| [Tier 1] | $[X]/mo | [Features] |
| [Tier 2] | $[X]/mo | [Features] |
| [Tier 3] | $[X]/mo | [Features] |

## Metrics Setup

### Activation

| Metric | Definition | Target | Tracking Method |
|--------|-----------|--------|----------------|
| Registration | User creates account | [X]% of invites | [Tool] |
| Onboarding complete | User finishes setup | [X]% of registrations | [Tool] |
| First value | User completes core action | [X]% of registrations | [Tool] |

### Retention

| Metric | Definition | Target |
|--------|-----------|--------|
| Day 1 | Returns day after signup | [X]% |
| Day 7 | Active 7 days post-signup | [X]% |
| Day 30 | Active 30 days post-signup | [X]% |

### Conversion

| Metric | Definition | Target |
|--------|-----------|--------|
| Free → paid | Upgrades to paid tier | [X]% |
| Trial → paid | Converts after trial | [X]% |

### Failure Triggers (from Stage 2)

- < [X]% activation from waitlist within 2 weeks → diagnose or decommission
- No paying users after 30 days → pivot pricing or decommission

## Launch Checklist

### Pre-Launch

- [ ] Production deployment tested
- [ ] Payment processing configured and tested
- [ ] Analytics tracking verified (all events firing)
- [ ] Onboarding flow works end-to-end
- [ ] Error monitoring active (Sentry or similar)
- [ ] Support channel ready (email address or chat)
- [ ] Waitlist invitation emails drafted
- [ ] Pricing page live

### Launch Day (Wave 1)

- [ ] Wave 1 invitations sent
- [ ] Monitor error rates (first 2 hours)
- [ ] Check first signups complete onboarding
- [ ] Review first-hour activation metrics
- [ ] Respond to any support requests

### Post-Launch Week 1

- [ ] Daily metrics review (activation, errors, support volume)
- [ ] User feedback collection (survey or 3 interviews)
- [ ] Critical bugs triaged and fixed
- [ ] Wave 2 go/no-go decision
- [ ] First retention data available (Day 1)

### Post-Launch Week 2

- [ ] Wave 2/3 deployment (if metrics healthy)
- [ ] Day-7 retention data reviewed
- [ ] First conversion data (if free tier exists)
- [ ] Compile Week 2 summary

---

**Next:** Advance to Stage 6 — Revenue & Scale
