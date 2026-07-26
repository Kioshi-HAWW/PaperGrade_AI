# 📊 GradeSense AI — Official 6-Slide Pitch Deck Blueprint (PDF Ready)

> **Strict Hackathon Rules Applied**:
> ✅ Exactly 6 Slides (Title + 5 Content Slides)
> ✅ Zero long paragraphs (100% Bullet Points, Flow Diagrams, Infographics & Cards)
> ✅ Ultra-precise & easy to understand
> ✅ Highlights Uniqueness & Novelty

---

## 🎨 Global Canva Design Theme

* **Canvas Ratio**: `16:9` Widescreen
* **Color Palette**: Dark Navy Background (`#0F172A`), Honeywell Red Accents (`#EE3124`), Neon Blue (`#38BDF8`), Emerald Green (`#10B981`)
* **Format Requirement**: Export from Canva as **PDF Standard / PDF Print** for portal upload.

---

## 🔹 SLIDE 1: TITLE SLIDE
*(Slide 1 of 6)*

### 🎨 Visual Layout
* Centered bold title card over a subtle dark industrial paper-mill background.
* Top right: Honeywell Red logo / accent tag.

### 📝 Slide Content (Exact Copy)

#### Top Badge
> `HONEYWELL HACKATHON 2026 — PAPER GRADE CHANGE INTELLIGENCE`

#### Main Title
# **GradeSense AI**
### **AI-Powered Decision Intelligence for Paper Grade Transitions**

#### Key Sub-Points
* ⏱️ **120-Second Early Warning**: Predicts Basis Weight quality breaches (>±2.5%) before they occur.
* 🧠 **Explainable AI (TreeSHAP)**: Translates black-box ML into human-readable root cause explanations.
* ⚡ **1-Click Closed-Loop Advisory**: Global active prompt banner with real-time process stabilization.

#### Presenter Details
* **Team**: Kioshi-HAWW
* **Repo**: `github.com/Kioshi-HAWW/PaperGrade_AI`
* **Live System**: `http://localhost:8000/`

---

## 🔹 SLIDE 2: PROPOSED SOLUTION & NOVELTY
*(Slide 2 of 6)*

### 🎨 Visual Layout
* 2-Column Infographic Cards (Red "Current Problem" vs Green "GradeSense Solution") + Bottom Novelty Banner.

### 📝 Slide Content (Exact Copy)

```
       CURRENT PROBLEM (🔴)                       GRADESENSE AI SOLUTION (🟢)
┌──────────────────────────────────────┐    ┌──────────────────────────────────────┐
│ • Off-Spec Paper (>±2.5% BW Breach)  │    │ • 120s Early Breach Warning          │
│ • Frequent Sheet Web Breaks          │    │ • TreeSHAP Root Cause Explanations   │
│ • Long Recovery Lag (20–45 minutes)  │    │ • Explicit Setpoint Recommendations  │
│ • Reactive Manual Operator Control   │    │ • 1-Click Action & Impact Logging    │
└──────────────────────────────────────┘    └──────────────────────────────────────┘
```

#### Infographic Flow
`Telemetry Data` ➔ `Risk Prediction (XGBoost)` ➔ `TreeSHAP Explanation` ➔ `Advisory Prompt` ➔ `Operator Action` ➔ `Stabilization`

#### 🌟 Unique & Novel Innovations
1. **Explainable Industrial AI**: Removes operator distrust by showing exact % feature attributions.
2. **Global Active Advisory Prompt**: Operates seamlessly across all dashboard tabs for instant 1-click execution.
3. **Dynamic Correlation Discovery Engine**: Finds undocumented process loop lags (e.g. Steam ↔ Moisture delay) using Granger Causality.

---

## 🔹 SLIDE 3: TECHNICAL APPROACH & ARCHITECTURE
*(Slide 3 of 6)*

### 🎨 Visual Layout
* Left 65%: Architecture & Data Pipeline Flowchart | Right 35%: Tech Stack Infographic Badges.

### 📝 Slide Content (Exact Copy)

#### AI System Architecture Diagram

```
[ Sensor Telemetry ] ➔ Stock Flow, Steam Pressure, Speed, Moisture, Ash, Caliper
        │
        ▼
[ Feature Pipeline ] ➔ 15s Rolling Mean, Std, Slope & Recipe Target Errors
        │
        ▼
┌───────────────────┴───────────────────┐
▼                                       ▼
[ XGBoost Risk Classifier ]           [ Granger Correlation Engine ]
Predicts BW Breach (>±2.5%)            Discovers Dynamic Delay Loops
        │                                       │
        └───────────────────┬───────────────────┘
                            ▼
             [ TreeSHAP Explainability ]
             Translates Root Causes to English
                            ▼
           [ Quantified Advisory Engine ]
           "Reduce Stock Flow by 3.5%"
                            ▼
      [ FastAPI WebSockets + ECharts Dashboard ]
      Global Prompt Banner + Impact Verification Log
```

#### Tech Stack Badges
* ⚡ **Backend**: Python 3.12, FastAPI, Uvicorn, WebSockets
* 🧠 **AI/ML**: XGBoost, TreeSHAP, Scikit-Learn, Pandas
* 📊 **Frontend**: Vanilla JS, Tailwind CSS, Apache ECharts
* ☁️ **Deployment**: Docker, Render Blueprint (`render.yaml`)

---

## 🔹 SLIDE 4: FEASIBILITY & CHALLENGES
*(Slide 4 of 6)*

### 🎨 Visual Layout
* 3 Equal Grid Cards (Feasibility, Operational Challenges, Solution Strategy).

### 📝 Slide Content (Exact Copy)

#### Card 1: 100% Software Feasibility ✅
* **Zero Hardware Changes**: Uses existing QCS & DCS sensors (*Stock, Steam, Speed, Moisture, Ash, Caliper*).
* **Non-Disruptive Advisory Layer**: Pure advisory digital twin — zero risk of accidental plant shutdown.
* **Instant Deployment**: Fully containerized with Docker & Render cloud blueprints.

#### Card 2: Key Industry Challenges ⚠️
1. **Dynamic Process Lags**: Thermal steam drying lags sheet moisture by 20–30s.
2. **Highly Correlated Loops**: Machine speed impacts both weight and moisture simultaneously.
3. **Operator Black-Box Resistance**: Operators reject unexplainable ML predictions.

#### Card 3: GradeSense Mitigation Strategy 🛡️
* **Windowed Slopes**: Incorporates 15s rolling rates of change to capture dynamic lags.
* **SHAP Transparency**: Shows plain-English reason behind every recommendation.
* **What-If Digital Twin**: Allows operators to simulate setpoints risk-free before applying.

---

## 🔹 SLIDE 5: LIVE PLATFORM ARTIFACTS & DEMO
*(Slide 5 of 6)*

### 🎨 Visual Layout
* 4 Screenshot Highlight Cards with UI Callouts & Key Performance Metrics.

### 📝 Slide Content (Exact Copy)

```
┌──────────────────────────────────────┐    ┌──────────────────────────────────────┐
│ 1. Real-Time Telemetry & Risk Meter  │    │ 2. TreeSHAP Feature Attributions     │
│ • 0–100% Dynamic Risk Meter          │    │ • Top Contributing Factor Ranking    │
│ • 100-Point Sliding Window ECharts   │    │ • Plain-English Explanation Output   │
│ • Live Basis Weight Deviation Tracking│    │ • "Steam Pressure & Stock Flow High" │
└──────────────────────────────────────┘    └──────────────────────────────────────┘
┌──────────────────────────────────────┐    ┌──────────────────────────────────────┐
│ 3. Global Live Advisory Banner ⚡    │    │ 4. Measured Impact History Log 📜    │
│ • Appears on ANY active tab          │    │ • Measured Risk Drop: 85% ➔ 5%       │
│ • 1-Click [ Accept & Apply Setpoint ]│    │ • BW Deviation Recovery: +3.2% ➔ -0.1%│
│ • Direct Simulator Physics Tuning    │    │ • Verified 28s Machine Recovery      │
└──────────────────────────────────────┘    └──────────────────────────────────────┘
```

#### Key Demonstrated Metric
> **Risk Reduction: 85.0% ➔ 5.0% | BW Deviation Stabilized to -0.1% | Recovery Time: 28s**

---

## 🔹 SLIDE 6: RESEARCH, ROADMAP & CLOSING
*(Slide 6 of 6)*

### 🎨 Visual Layout
* 2 Columns (References & Standards vs Future Roadmap) + Bottom Tagline.

### 📝 Slide Content (Exact Copy)

#### Left Column: References & Standards 📚
* **Honeywell QCS & MD Control Specs**: Multivariable Machine Direction Control standards.
* **SHAP Interpretability Framework**: Lundberg & Lee (2017) *Unified Approach to Model Interpretation*.
* **Granger Causality in Process Loops**: Time-series lead-lag relationship analysis.

#### Right Column: Future Roadmap 🚀
* 🤖 **Reinforcement Learning (RL)**: Self-optimizing ramping trajectories for autonomous shifts.
* ⚡ **Edge AI Integration**: Direct deployment on Honeywell Experion PKS edge nodes.
* 🌐 **Honeywell Forge Integration**: Fleet-wide analytics sync across multi-mill operations.

---

### 🎯 Final Tagline (Bottom Banner)
> # **Predict Earlier. Explain Clearly. Optimize Smarter.**
> **GradeSense AI — Next-Generation Paper Machine Intelligence**
