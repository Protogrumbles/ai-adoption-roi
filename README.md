# AI Adoption ROI Calculator

A small, local-first estimator for teams deciding whether governed AI adoption
pays for itself — and the 4-week plan for doing it safely if it does.

**Try it:** open `index.html` in any browser. No install, no server, no account,
no data leaves the page. No network requests, no external fonts or CDNs.

## What it does

Enter four numbers — team size, monthly ticket/request volume, avg loaded hourly
cost, current monthly AI tool spend — and get:

- **Hours saved / month** and hours saved per person
- **Gross and net value / month**, and **$ recovered / year (net)**
- **ROI multiple** on AI spend
- **Scenarios** (conservative / expected / optimistic) that move only the
  eligible-share assumption, so you see the range, not just the flattering number
- **A spend / budget view** with a recommended soft cap (5% of gross monthly
  value) — a nudge, never a hard cutoff and never a performance scorecard
- **The 4-week adoption plan** (16 steps: Week 1 See it, Week 2 Identify it,
  Week 3 Own it, Week 4 Prove it) and the **kill-switch registry** concept:
  every agent has a named owner, a declared scope, and a one-action kill switch

It also downloads a `registry.csv` of example rows and a one-page `roi-summary.md`
of your inputs and results — generated locally in your browser.

## The model (every assumption, on the page)

1. **AI-eligible share: 40%** of monthly requests can be AI-assisted. Judgment
   calls, sensitive cases, and novel work stay human.
2. **Time saved per assisted request: 18 minutes (0.30 hr)** — drafting, triage,
   summarising, first-pass answers.
3. Hours saved / mo = volume × 0.40 × 0.30
4. Gross value / mo = hours saved × loaded hourly cost
5. Net value / mo = gross value − AI spend. $ recovered / yr = net × 12
6. ROI multiple = gross value ÷ AI spend (only when spend > 0)
7. Recommended soft spend cap = 5% of gross monthly value

## The worked example (anonymized)

The **Load anonymized Netflix-scale worked example** button fills in:

| Input | Value |
| --- | --- |
| Team size | 85 people |
| Monthly volume | 5,000 requests |
| Loaded hourly cost | $145/hr |
| Current AI spend | $2,400/mo |

Computed outputs (verified by hand and by automated test — see below):

| Output | Value |
| --- | --- |
| Hours saved | **600 / mo** (~7.1 hrs/person/mo; 2,000 assisted requests) |
| Gross value | **$87,000 / mo** |
| Net value | **$84,600 / mo** |
| **$ recovered / yr (net)** | **$1,015,200** |
| ROI (gross) | **36.3x** |
| Soft spend cap | $4,350/mo — spend is $1,950 under cap |
| Scenarios (net $/yr) | Conservative (30%) $754,200 · Expected (40%) $1,015,200 · Optimistic (50%) $1,276,200 |

These inputs are illustrative values chosen so the model reproduces the verified
field anchor of ~600 hours saved per month. **They are not Netflix's real data,
and $1,015,200/yr is the model's output for one team — not the verified program
outcome below.**

### Verified field anchors (context only — never calculator output)

From the large-scale AI-adoption program this calculator's assumptions were
calibrated against:

- **$2.5M/yr recovered** (program-wide, across 57 productions in ~8 weeks)
- **~600 hrs/mo saved** — the anchor the worked example reproduces
- **5–7x faster** handling on AI-assisted work
- **Escalations down ~25%**; **first-contact resolution improved ~65–70%**
- **$0.40/session** prototype cost

Do not quote these as what your team will get. They show what disciplined,
governed adoption achieved at scale; the calculator shows what your own inputs
imply.

## Install / use

**Calculator (browser):** open `index.html`. That's it.

**Claude Code skill:** copy `skill/` to `.claude/skills/ai-adoption-roi-calculator/`
(or `~/.claude/skills/` to use it everywhere). Then ask: `estimate the ROI of AI
adoption for my team`. The skill (`skill/SKILL.md`) wraps the same model, and
`skill/scripts/roi.py` is a CLI mirror of the calculator:

```sh
python3 skill/scripts/roi.py --team 85 --volume 5000 --hourly 145 --spend 2400
python3 skill/scripts/roi.py --example          # anonymized worked example
python3 skill/scripts/roi.py --example --json   # machine-readable output
```

**Codex / Cursor:** copy `skill/` to `.agents/skills/ai-adoption-roi-calculator/`.

## Files

- `index.html` — the calculator. Single self-contained file.
- `skill/SKILL.md` — the Claude Code skill: when to use it, the model, the
  worked example, handoff rules.
- `skill/.claude-plugin/plugin.json` — plugin metadata.
- `skill/scripts/roi.py` — CLI mirror of the calculator logic (Python 3.10+,
  no dependencies).
- `data/demo-usage-log.json` — fictional one-month usage log (12 rows, 2,000
  requests, $2,400) matching the worked example's spend. Fictional users/tools.
- `data/registry-example.csv` — example kill-switch registry rows.
- `dashboard/index.html` — the companion 16-step progress + spend dashboard
  from the AI Adoption Walkthrough. Copied verbatim; see note below.

## Companion project

This calculator estimates. The **AI Adoption Walkthrough**
(`Protogrumbles/ai-adoption-walkthrough`) governs: a 10-question interview that
generates a tailored 4-week plan, a real `registry.csv`, and a `usage-log.json`
for your team. Run the calculator first — if the net value is clearly positive,
the walkthrough is worth doing.

## Dashboard note

`dashboard/index.html` (46,961 bytes) was copied verbatim from the existing
AI Adoption Walkthrough pack (`ai-adoption-walkthrough-skill/dashboard/`).
Checked before copying: **clean** — no external URLs, no `fetch`/`XMLHttpRequest`,
no external fonts or CDNs; it persists progress with `localStorage` only. It is
included here as the companion progress/spend dashboard for the 16-step plan,
not as part of the calculator itself. It reads a `usage-log.json` from the same
folder when present; the fictional `data/demo-usage-log.json` is the example of
that format (copy it next to the dashboard as `usage-log.json` to see it populated
— but only with fictional data, never real user data).

## What this deliberately is NOT

- Not a promise of savings, a quote, or a guarantee of compliance or security.
  It gives a planning estimate and a governance plan — visibility and control,
  not a promise that nothing can go wrong.
- Not a governance platform. No server, no multi-tenant anything.
- Not a Netflix stack in a box. The patterns are inspired by large-scale practice
  (short-lived scoped identity, one audit log, a named owner per agent, spend
  surfaced in-tool). The implementation here is deliberately lighter.
- Not a replacement for a security review. If you handle regulated data, get one
  before Week 3.

## Testing

The calculator logic (`calculateROI` in `index.html`) is a pure function with no
DOM access, so it is testable headlessly. Verified with Node (stub DOM) and
independently by hand in Python:

- Worked example: 5,000 × 0.40 × 0.30 = **600 hrs/mo**; 600 × $145 = **$87,000/mo**
  gross; $87,000 − $2,400 = **$84,600/mo** net; × 12 = **$1,015,200/yr**;
  $87,000 ÷ $2,400 = **36.3x** ROI.
- Scenarios: 450 / 600 / 750 hrs/mo → **$754,200 / $1,015,200 / $1,276,200** per year.
- Default inputs (25 people, 1,200/mo, $85/hr, $500/mo): 144 hrs/mo,
  $140,880/yr net, 24.5x ROI.
- Zero-spend edge case: ROI reported as not applicable, no division by zero.
- Demo dataset: 12 rows sum to exactly 2,000 requests, 2,500,000 input tokens,
  780,000 output tokens, $2,400.00 — matching the worked example's spend and the
  table in `index.html`.
- `skill/scripts/roi.py --example` reproduces the worked example exactly
  (same constants, same formulas).

## License

MIT. Use it, fork it, adapt it.

Built by Sean Steuer — Senior Program Manager, AI Strategy & Operational
Transformation, Netflix. UVA Darden Digital Product Management is a Coursera
certificate, not a degree.
