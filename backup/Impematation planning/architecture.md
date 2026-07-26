# Architecture — GradeSense AI (Grade Change Intelligence Platform)

## 1. System Overview
The platform is an **intelligence layer on top of** Honeywell QCS/MD Control — it does not replace control execution. It ingests historical + streaming process data, predicts Basis Weight deviation risk during grade transitions, explains *why*, recommends corrective setpoints, and learns from operator feedback.

## 2. High-Level Module Flow
```
Historical Data (QCS / DCS historian / MIS / Alarms / Operator Actions)
        │
        ▼
Data Ingestion & Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
Correlation Discovery Engine
        │
        ▼
Prediction Engine  ───► Risk Score (Basis Weight ±2.5% breach probability)
        │
        ▼
Recommendation Engine ───► Quantified setpoint changes + source of inference
        │
        ▼
Explainability Layer (SHAP / LIME) ───► "Why" behind every prediction/recommendation
        │
        ▼
Dashboard (real-time + historical replay + what-if simulator)
        │
        ▼
Operator Feedback Capture (accept / reject / modify) ───► feeds back into training data
```

## 3. Module Breakdown

### 3.1 Data Ingestion Layer
**Inputs:** QCS history, historical process data, recipe data, alarm logs, operator actions, sensor/scanner data, failure/broke logs, MIS reports.
**Core fields:** timestamp, recipe ID, basis weight, moisture, ash, machine speed, steam pressure, stock flow, filler flow, caliper, operator action, alarm count, recipe setpoints/limits.
**Output:** unified, time-synchronized dataset.

### 3.2 Preprocessing
- Missing value handling
- Outlier removal
- Time synchronization across sensors/loops
- Feature scaling / normalization
- Sliding window generation, e.g. **use past 5 minutes to predict next 2 minutes**, recomputed every ~30 seconds.

### 3.3 Feature Engineering
Beyond raw values, generate:
- Rolling mean / rolling std
- Slope / rate of change
- Lag features
- Recipe difference (current vs. target setpoint)
- Transition duration / time since grade change began
- Derived signals: steam change rate, machine speed acceleration, moisture drift, stock flow difference

### 3.4 Correlation Discovery Engine
Purpose: surface hidden/undocumented relationships between loops (a core judged requirement).
**Methods:** correlation matrix, mutual information, SHAP-based importance, Dynamic Time Warping (for lagged relationships), Granger causality (for directional influence).
**Output example:** `Steam Pressure ↑ → Moisture ↓ → Basis Weight Drift ↑` with a strength/confidence score, tagged with the discovery method used (this becomes the "source of inference" tag required in deliverables).

### 3.5 Prediction Engine
**Task:** binary/probabilistic — will Basis Weight exceed ±2.5% of setpoint within the prediction horizon?
**Model progression (baseline → best):**
- Baseline: Logistic Regression / Random Forest
- Improved: XGBoost / LightGBM (tabular, fast, interpretable via SHAP)
- If sufficient sequential data: LSTM or a small Temporal Transformer for trajectory-aware prediction
**Output:** Risk score (0–100%) + predicted future Basis Weight trajectory + time-to-breach estimate.

### 3.6 Recommendation Engine
Goes beyond "risk = high" to **quantified, actionable setpoint changes**:
- e.g. "Reduce Stock Flow by 3%", "Increase Machine Speed by 1.5%", "Decrease Steam by 2 PSI"
**Methods:**
- Rule engine (recipe/process-limit based guardrails)
- Historical similarity search (k-NN over past transitions with similar signatures — "find the 10 most similar past grade changes and see what worked")
- Constrained optimization (search setpoint deltas that minimize predicted deviation subject to recipe/actuator limits)
- Future extension: Reinforcement Learning policy trained on historical success/failure trajectories

### 3.7 Explainability Layer
- SHAP (primary) / LIME (secondary) to attribute the prediction to contributing features.
- Output format matches the judged requirement directly:
  > "Predicted because stock flow increased while moisture remained high and machine speed lagged."
- Every recommendation is tagged with its **source of inference** (e.g. "historical similarity: Transition #4821", "recipe constraint", "correlation discovery: Steam→Moisture link").

### 3.8 Dashboard / Presentation Layer
See `design.md` for full UI spec. Key required views:
- Live monitoring + risk gauge
- Correlation explorer (new relationships found)
- Future-state projection (if current trend/trajectory continues)
- Suggested setpoints w/ expected recovery time
- Historical replay
- What-if simulator (digital-twin-lite)
- Accept/Reject feedback capture on every suggestion

### 3.9 Operator Feedback Loop
Every prediction/recommendation gets a response: **Useful / Not Useful / Applied / Ignored / Modified**.
These are stored and used to:
1. Evaluate suggestion accuracy/quality over time (required deliverable).
2. Become future training labels (continuous learning loop).

## 4. Tech Stack
| Layer | Technology |
|---|---|
| Frontend | Next.js + React, Tailwind CSS + shadcn/ui |
| Charts | Apache ECharts / Plotly |
| Animations | Framer Motion |
| Network/Correlation graph | React Flow |
| Backend / API | FastAPI |
| ML | Python, scikit-learn, XGBoost, LightGBM, (optional LSTM via PyTorch) |
| Explainability | SHAP |
| Database | PostgreSQL |
| Real-time updates | WebSockets |
| Deployment | Docker |

## 5. Data Flow Between Modules (interface contracts)
- **Ingestion → Feature Engineering:** clean, time-aligned rows keyed by timestamp + recipe ID.
- **Feature Engineering → Correlation Engine:** windowed feature matrix.
- **Feature Engineering → Prediction Engine:** windowed feature matrix + labels (historical breach/no-breach).
- **Prediction Engine → Recommendation Engine:** risk score + top contributing features + predicted trajectory.
- **Recommendation Engine → Explainability Layer:** chosen setpoint deltas + the evidence used to choose them.
- **Explainability Layer → Dashboard:** structured JSON `{risk_score, predicted_trajectory, contributing_factors[], recommendations[], source_of_inference}`.
- **Dashboard → Feedback Store:** `{recommendation_id, operator_response, timestamp}` → looped back into training data store.

## 6. Non-Functional Requirements
- Explainability output must accompany **every** prediction and recommendation, not just headline risk scores.
- Recommendation source of inference must be visible per Honeywell's deliverable requirement.
- System should be demo-able against a simulated/replayed historical dataset (no live plant connection required for hackathon).
