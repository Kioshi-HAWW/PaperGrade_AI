# Design — GradeSense AI UI/UX Spec

## 1. Concept
**Name:** GradeSense AI (alt: Honeywell IntelliGrade)
**Theme:** Dark industrial, glassmorphism with subtle industrial accents.
**Palette:** Black / Charcoal base, Neon Blue (primary accent), Honeywell Red (critical/brand), Emerald Green (safe/normal), Orange (warning).

## 2. Navigation

### Top Bar
Logo · Current Recipe · Machine Status · Current Shift · Notifications · AI Copilot · Profile

### Left Sidebar
- 🏠 Overview
- 📈 Live Monitoring
- 🤖 AI Prediction
- 🧠 AI Recommendations
- 📊 Correlation Explorer
- 🛰 Digital Twin / What-if Simulator
- 📚 Historical Replay
- ⚠ Alarm Center
- 📝 Operator Feedback
- ⚙ Settings

## 3. Page Specs

### 3.1 Overview (Home) — where judges spend the most time
- Plant status header: Production Status, Machine Health, Current Grade → Target Grade, animated transition progress bar, remaining time, overall risk score.
- KPI cards (animated): Current Basis Weight, Moisture, Steam Pressure, Machine Speed, AI Confidence — each with current value + trend indicator (Stable / Optimal / +3% etc.).

### 3.2 Live Monitoring
- Real-time, interactive multi-variable charts (zoom, brush, hover) for Basis Weight, Moisture, Steam, Speed, Stock Flow, Ash, Caliper.
- Overlay capability (compare two variables on one chart).
- Hover tooltip shows timestamp + values + live prediction state (Stable/At Risk).

### 3.3 AI Prediction (hero page)
- Large circular risk gauge (0–100%), color-coded green → yellow → orange → red, animated pulse when risk rises.
- Prediction timeline: Now / 30s / 1min / 3min / 5min, with a dotted projected trajectory line.
- Current vs. predicted-future vs. limit values shown directly (e.g. Current 181 → Future 187 → Limit 185, "Exceeds limit in 72 sec").

### 3.4 AI Recommendations
- Recommendation cards, not paragraphs: each shows the action ("Reduce Stock Flow 3%"), confidence %, expected recovery time, and a "Simulate" button.
- Multiple ranked recommendations shown together so the operator can compare.

### 3.5 Explainable AI (embedded within Prediction/Recommendation views)
- Contribution pie/bar chart: which variables drove this prediction (e.g. Steam 38%, Moisture 26%, Speed 18%, Stock Flow 11%, Others 7%).
- Plain-language explanation directly under the chart (e.g. "High steam pressure combined with decreasing moisture caused rapid basis weight increase.") plus a confidence %.
- Source-of-inference tag on every explanation/recommendation (historical match, recipe rule, correlation discovery, etc.) — required by the brief.

### 3.6 Correlation Explorer (high differentiation)
- Interactive network graph (nodes = variables, edges = discovered correlations) e.g. Steam — Moisture — Basis Weight — Paper Break.
- Click a node to see correlation strength (e.g. Steam↔Moisture: Strong Positive, 0.89) and update the graph around it.
- Time slider to see how correlation strength evolves across a transition or across historical transitions.

### 3.7 Digital Twin / What-if Simulator (killer feature)
- Simplified visual of the paper machine: Headbox → Press → Dryer → Calender → Reel, sections color-coded Green/Yellow/Red by predicted health.
- Clicking a section shows its live and predicted values (steam, moisture, predicted output, temperature).
- **What-if sliders** (Steam, Machine Speed, Stock Flow, etc.) — moving a slider immediately updates predicted Risk %, Recovery time, and predicted Basis Weight, without touching the real plant. This is the scenario-planning centerpiece judges are expected to remember.

### 3.8 Historical Replay
- Play / Pause / 2x / 4x / 8x playback of a past transition.
- Overlay: "At 09:12 Steam increased → AI would have recommended Reduce Speed → Deviation avoided" — demonstrates the model retroactively against real outcomes.

### 3.9 Alarm Center
- Modern notification list: 🔴 High Risk / 🟡 Drift Warning / 🟢 Stable, each with root cause, recommended action, and who acknowledged it.

### 3.10 Operator Feedback
- Every prediction/recommendation carries: 👍 Helpful / 👎 Not Helpful / Applied / Ignored, plus an optional comment field.
- This feed is what closes the continuous-learning loop and satisfies the "accept/reject" deliverable requirement.

### 3.11 AI Chat Copilot
- Floating bottom-right "Ask GradeSense" assistant.
- Operator can ask natural-language questions ("Why is Basis Weight increasing?", "Show similar transitions") and get grounded answers referencing the same prediction/explanation/recommendation data shown elsewhere in the UI (not a separate black box).

### 3.12 Mobile Companion (stretch goal)
- Supervisor-facing summary: current risk %, push notification when a transition risk crosses a threshold, link to open recommendation.

## 4. Demo Narrative (for judging)
1. Live plant overview with animated KPIs.
2. AI detects a future Basis Weight deviation ~90 seconds before it occurs.
3. Risk gauge shifts green → red.
4. Digital Twin highlights the affected section (e.g. Dryer).
5. AI explains *why* (contribution breakdown + plain-language sentence + source tag).
6. What-if simulator tests 2–3 corrective actions side by side.
7. Best recommendation applied (virtually) — risk gauge falls back to safe zone, recovery time shown.
8. Historical replay shows a similar past incident and how this system would have prevented it.
9. Operator marks the recommendation Useful/Applied — feedback loop closes.

## 5. Frontend Tech Stack
| Component | Recommendation |
|---|---|
| Frontend framework | Next.js + React |
| Styling | Tailwind CSS + shadcn/ui |
| Charts | Apache ECharts |
| Animations | Framer Motion |
| Network graph | React Flow |
| Process-flow / digital twin visuals | SVG + D3.js (3D via React Three Fiber only if time allows) |
| Real-time | WebSockets |
