# Phases — Implementation Roadmap

Each phase should end with a checked-off item in `memory.md` before moving to the next, so the agent (or a new session) always knows exactly where the project stands.

## Phase 0 — Setup
- Confirm dataset(s) available (historical QCS/DCS export, recipe data, alarm logs, operator action logs). If no real dataset is provided, build a **synthetic grade-change simulator** that generates plausible time-series for stock flow, filler flow, steam pressure, machine speed, moisture, ash, basis weight, caliper, with injected "grade change" events and occasional induced off-spec deviations.
- Set up repo structure: `/backend`, `/frontend`, `/ml`, `/data`.
- Set up FastAPI skeleton + Next.js skeleton + PostgreSQL schema.

## Phase 1 — Data Collection / Simulation
- Define unified schema: timestamp, recipe_id, basis_weight, moisture, ash, machine_speed, steam_pressure, stock_flow, filler_flow, caliper, operator_action, alarm_count, recipe_setpoints, recipe_limits.
- Load or simulate historical transitions (aim for many transitions with a mix of successful and off-spec/broke outcomes so the model has both classes to learn from).

## Phase 2 — Preprocessing
- Handle missing values, remove outliers, time-synchronize all signals.
- Normalize/scale features.
- Generate sliding windows: e.g. past 5 minutes of data → predict next 2 minutes of Basis Weight behavior, recomputed every ~30s.

## Phase 3 — Feature Engineering
- Rolling mean/std, slope, rate of change, lag features.
- Recipe-difference features (distance from current value to target setpoint).
- Transition-duration / time-since-grade-change feature.
- Derived signals: steam change rate, machine speed acceleration, moisture drift, stock flow difference.

## Phase 4 — Correlation Discovery
- Run correlation matrix, mutual information, Granger causality, and Dynamic Time Warping across variable pairs.
- Rank and store discovered relationships with a confidence score and discovery method (this becomes the "new correlations" deliverable).
- Flag relationships not already encoded as control loops in QCS — these are the genuinely "new" ones the brief asks for.

## Phase 5 — Prediction Engine
- Baseline model: Random Forest / Logistic Regression → establish a floor.
- Improve: XGBoost / LightGBM.
- If time allows and data is sufficiently sequential: LSTM or small Temporal Transformer.
- Target: probability that Basis Weight deviates >±2.5% from setpoint within the prediction horizon, plus predicted trajectory.
- Evaluate against held-out historical transitions (precision/recall on breach detection + lead-time-before-breach).

## Phase 6 — Recommendation Engine
- Rule engine encoding recipe/process limits as hard guardrails.
- Historical similarity search (k-NN) to retrieve past transitions with similar signatures and what setpoint changes correlated with recovery.
- Constrained optimization to propose specific setpoint deltas (e.g. "-3% stock flow") that minimize predicted deviation within recipe/actuator limits.
- Every recommendation must carry a `source_of_inference` tag.

## Phase 7 — Explainable AI
- Integrate SHAP against the prediction model to get per-prediction feature contributions.
- Generate plain-language explanation strings from the top contributing features (template-based is fine: "Predicted because X increased while Y remained high and Z lagged").

## Phase 8 — Dashboard
- Build pages per `design.md`: Overview, Live Monitoring, AI Prediction, AI Recommendations, Correlation Explorer, Digital Twin/What-if Simulator, Historical Replay, Alarm Center, Operator Feedback.
- Wire dashboard to backend via REST (historical) + WebSocket (live/simulated stream).
- Ensure every prediction/recommendation panel shows: risk score, explanation, source of inference, and Accept/Reject controls.

## Phase 9 — Operator Feedback Loop
- Persist every operator response (Useful/Not Useful/Applied/Ignored/Modified) tied to its recommendation ID.
- Build a simple accuracy/quality view (e.g. "% of accepted recommendations that led to successful stabilization") to satisfy the "evaluate quality/accuracy" deliverable.
- Note: full retraining-on-feedback loop can be described as a roadmap item if time-constrained; a working feedback *capture* mechanism is the hard requirement.

## Phase 10 — Documentation & Presentation
- Fill Honeywell's provided presentation template.
- Prepare architecture diagram, module explanations, and demo script (see `design.md` §4 Demo Narrative).
- Package deliverables (solution + docs + dashboard evidence) into PDF/Zip per submission instructions.
- Final review against `prd.md` §6 Deliverables and §7 Success Criteria checklist.

## Suggested Priority Order If Time-Constrained
1. Prediction Engine (Phase 5) — this is the core judged capability.
2. Explainability (Phase 7) — explicitly called out as a major judging criterion.
3. Recommendation Engine (Phase 6) — required, differentiates from a plain classifier.
4. Dashboard core views: Overview + AI Prediction + AI Recommendations (Phase 8, partial).
5. Correlation Explorer + Feedback Loop (Phases 4 & 9) — required deliverables, can be simpler versions.
6. Digital Twin / What-if Simulator, Historical Replay — high-impact but can be simplified/mocked if time runs out.
