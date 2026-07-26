# Rules — How to Work on This Project

These are standing rules for any agent (or person) picking up work on this project. Read `memory.md` first, then these rules, before making changes.

## 1. Source of Truth
- `prd.md` is the authoritative statement of the problem, constraints, and required deliverables. Any feature not tracing back to a `prd.md` requirement is a "nice to have," not a priority.
- The official Honeywell screenshot brief (Basis Weight ±2.5%, deliverables list, constraints) overrides any earlier informal draft if they ever conflict.

## 2. Always Update Memory
- Treat context/quota as scarce and unpredictable — it can run out mid-task with no warning. Because of this, **do not wait until a phase or task is fully finished** to update `memory.md`. Update it early and often.
- Concretely:
  - Before starting any non-trivial chunk of work, write a `memory.md` entry stating what you're about to do and what "next step" means if you get cut off right now.
  - After any meaningful sub-step (not just full completion) — a file created, a decision made, a model trained, a bug found — update the entry's "What was done" and "Next step" fields immediately, in place. Don't batch updates for later.
  - The "Next step" field must always be current and specific enough that a brand-new session could resume without re-reading code or re-deriving decisions — e.g. "Next step: implement the XGBoost baseline in /ml/predict.py using the windowed features already saved to /data/features.parquet" rather than "continue Phase 5."
  - If a response/turn is likely to be long (large file generation, long-running command, big refactor), write or update the memory entry *before* starting that long operation, not after — so partial progress is still recoverable.
  - Never leave `memory.md`'s most recent entry stale relative to actual progress — if in doubt, update it again.
- Before starting work in a new session, read `memory.md` fully first — do not re-derive decisions already made.

## 3. Non-Negotiable Requirements (never drop these even under time pressure)
1. Every prediction must come with an explanation (SHAP-derived contributing factors + a plain-language sentence).
2. Every recommendation must be tagged with its **source of inference**.
3. Every suggestion shown in the dashboard must have Accept/Reject (or Useful/Not Useful) controls, and responses must be recorded.
4. The dashboard must show newly discovered correlations, not just re-display existing QCS control loops.
5. The target variable is **Basis Weight**, and the breach threshold is **±2.5%** from the recipe setpoint — do not silently change this threshold.

## 4. Scope Discipline
- This is an intelligence layer on top of QCS/MD Control, not a replacement for it. Do not build actual closed-loop plant control — simulated/what-if only.
- Prefer a working, simplified version of every required deliverable over a polished version of only some of them. Breadth across `prd.md` §6 deliverables beats depth on one module.

## 5. Data & Modeling
- If no real plant dataset is available, clearly label the data as **synthetic/simulated** everywhere it's referenced (code comments, dashboard footer, presentation) — never imply it's real Honeywell plant data.
- Model choice progression should be baseline → better → best (Random Forest → XGBoost/LightGBM → LSTM/Transformer if time allows) — don't jump straight to the most complex model without a baseline to compare against.
- Always evaluate lead time (how far in advance a breach is predicted), not just classification accuracy — early warning is the point.

## 6. Explainability Standard
- Never show a bare risk score/percentage without an accompanying explanation and source tag next to it in the UI.
- Explanation text should name specific variables and their direction of change (e.g. "steam increased," "moisture stayed high"), not generic statements like "multiple factors contributed."

## 7. Code & Repo Conventions
- Backend: FastAPI, Python. ML code lives under `/ml`, API routes under `/backend`.
- Frontend: Next.js + React + Tailwind + shadcn/ui, charts via Apache ECharts/Plotly, as specified in `design.md`.
- Keep the six planning docs (`prd.md`, `architecture.md`, `design.md`, `phases.md`, `rules.md`, `memory.md`) at the project root and treat them as living documents — update them as decisions change, don't let code and docs drift apart.

## 8. Presentation/Submission
- Use Honeywell's provided presentation template — do not build a from-scratch deck.
- Final submission must be PDF or Zip only, per the brief's upload instructions.
- Before submitting, re-check `prd.md` §6 Deliverables and §7 Success Criteria line by line.

## 9. When Uncertain
- If a requirement is ambiguous, default to the interpretation that is more demo-able and more clearly traceable to a `prd.md` line item, and note the assumption in `memory.md`.
- Don't silently drop a required deliverable because it's hard — instead, build the simplest version that satisfies it and note in `memory.md` that it's simplified and why.
