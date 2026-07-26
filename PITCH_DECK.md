# 📊 GradeSense AI — 6-Slide Canva Presentation Pitch Deck

This blueprint contains the exact text, diagrams, metrics, visual layout guidelines, and callouts to build your presentation in Canva or PowerPoint.

---

## 🎨 Global Design System & Styling Guide

* **Background**: Dark Navy (`#0F172A`)
* **Primary Color**: Honeywell Red (`#EE3124` / `#E2231A`)
* **Secondary / Accent**: Electric Neon Blue (`#00AEEF` / `#38BDF8`) & Emerald Green (`#10B981`)
* **Card Container Style**: Glassmorphic dark panels with subtle border (`border border-slate-700/50`) and rounded corners (`16px`).
* **Typography**:
  * **Headings**: `Inter` / `Outfit` / `Poppins` (Bold, White `#FFFFFF`)
  * **Subtitles**: `Roboto Mono` / `Inter` (Neon Blue `#38BDF8` or Slate `#94A3B8`)
  * **Body Text**: `Inter` (Light/Regular `#CBD5E1`)

---

## 🔹 Slide 1: Title & Overview

### 📌 Layout & Visual Concept
* **Background Image**: Darkened, high-tech paper mill cylinder roll with semi-transparent neon network overlays.
* **Layout**: Centered title with Honeywell red accent badge and glowing callouts.

### 📝 Slide Content

#### Badge Header
> `HONEYWELL HACKATHON 2026 — PAPER GRADE CHANGE INTELLIGENCE`

#### Main Title
# **GradeSense AI**
### **AI-Powered Decision Intelligence for Paper Grade Transitions**

#### Subtitle
> **Predicting Basis Weight Quality Breaches 120s Ahead with Explainable AI & Closed-Loop Operator Advisory**

---

#### 👤 Presenter Details (Bottom Card)
* **Team Name**: Kioshi-HAWW
* **Repository**: [github.com/Kioshi-HAWW/PaperGrade_AI](https://github.com/Kioshi-HAWW/PaperGrade_AI)
* **Platform Live**: `http://localhost:8000/` (Render Cloud Deployment Ready)

---

## 🔹 Slide 2: Problem Statement & Proposed Solution

### 📌 Layout & Visual Concept
* **Layout**: 2-Column Comparison Layout (Red "Current Challenges" vs Green "GradeSense Solution") with an innovation banner at the bottom.

---

### 📝 Left Column: Current Transition Challenges 🔴

| Challenge | Impact on Mill Performance |
|---|---|
| 🔴 **Off-Spec Quality Loss** | Basis Weight strays >±2.5% from setpoint during grade shifts. |
| 🔴 **Paper Web Breaks** | Uncoordinated speed & stock ramping causes costly sheet tears. |
| 🔴 **Slow Recovery Times** | Long stabilization lag (20–45 min per grade change). |
| 🔴 **Reactive Operator Control** | Operators act *after* quality limits are breached. |

---

### 📝 Right Column: GradeSense AI Solution 🟢

* ⚡ **120-Second Predictive Lead Time**: XGBoost model predicts Basis Weight breaches *before* they occur.
* 🧠 **TreeSHAP Explainability**: Translates complex ML factors into plain-language root causes.
* 🎯 **Quantified Actionable Setpoints**: Advises explicit deltas (e.g. *"Reduce Stock Flow by 3.5%"*).
* 🔄 **Closed-Loop Feedback & Impact Log**: Records operator acceptance and tracks real-time machine recovery.

---

### 💡 Bottom Banner: Core Innovation
> **Shift from Reactive QCS Tuning → Proactive Decision Intelligence: Predict ➔ Explain ➔ Advise ➔ Stabilize.**

---

## 🔹 Slide 3: System Architecture & Technical Approach

### 📌 Layout & Visual Concept
* **Layout**: Left 60% Process Diagram Flow | Right 40% Technology Stack Cards.

---

### 📝 Left Section: Process Data Flow Diagram

```
QCS / Sensor Data (Stock, Steam, Speed, Moisture, Ash, Caliper)
                         │
                         ▼
             Data Cleaning & Feature Pipeline
          (15s Rolling Mean, Std, Slope & Errors)
                         │
                         ▼
        ┌────────────────┴────────────────┐
        ▼                                 ▼
XGBoost Risk Classifier       Granger Correlation Engine
(Predicts BW Breach >±2.5%)   (Discovers Dynamic Loop Lags)
        │                                 │
        └────────────────┬────────────────┘
                         ▼
             TreeSHAP Explainability
            ("Why" Feature Attribution)
                         │
                         ▼
          Quantified Advisory Engine
         (Setpoint Deltas + Source Tags)
                         │
                         ▼
       FastAPI WebSockets + ECharts UI
        (Live Global Prompt & Impact Log)
```

---

### 📝 Right Section: Production Tech Stack

* ⚡ **Backend Engine**: `Python 3.12` • `FastAPI` • `Uvicorn`
* 📡 **Real-Time Pipeline**: `WebSockets` (1s live streaming telemetry)
* 🧠 **Machine Learning**: `XGBoost` (Classifier) • `TreeSHAP` (Feature Attribution)
* 📊 **Frontend UI**: `Vanilla JS` • `Tailwind CSS` • `Apache ECharts`
* ☁️ **Deployment**: `Docker` • `Render.yaml Blueprint`

---

## 🔹 Slide 4: Feasibility & Implementation Strategy

### 📌 Layout & Visual Concept
* **Layout**: 3 Grid Cards (Hardware Feasibility, Operational Challenges, Mitigations).

---

### 📝 Card 1: 100% Software-Only Feasibility ✅
* **Zero New Hardware Required**: Integrates seamlessly with existing QCS/DCS sensors (*Stock Flow, Steam Pressure, Machine Speed, Moisture, Ash, Caliper*).
* **Non-Disruptive Advisory Layer**: Runs alongside existing QCS loops without risk of plant shutdowns.

---

### 📝 Card 2: Key Operational Challenges ⚠️
1. **Dynamic Process Lags**: Thermal steam drying lags sheet moisture by 20–30 seconds.
2. **Highly Correlated Multivariable Loops**: Speed changes affect both weight and moisture simultaneously.
3. **Operator Trust**: Closed-box ML models are rejected by mill operators.

---

### 📝 Card 3: GradeSense AI Solution Strategies 🛡️
* **Feature Engineering**: Incorporates 15s rolling slopes and dynamic lag matrices.
* **Explainable AI (TreeSHAP)**: Provides full transparency into *why* an advisory is generated.
* **What-if Digital Twin Simulator**: Allows operators to test setpoints risk-free before applying.

---

## 🔹 Slide 5: Key Platform Artifacts & Live Features ⭐

### 📌 Layout & Visual Concept
* **Layout**: 4 Feature Highlight Cards with actual application metrics and visual callouts.

---

### 📝 Feature 1: Live Telemetry & Risk Gauge 📈
* **0–100% Dynamic Risk Meter**: Pulsing visual alert when breach risk exceeds >25%.
* **Live ECharts Buffering**: 100-point sliding window for Basis Weight, Steam, and Machine Speed.

---

### 📝 Feature 2: TreeSHAP Explainability & Root Cause 🧠
* **Feature Contributions**: Ranks parameters by % impact on breach risk.
* **Human-Readable Output**: *"Risk is driven by high steam drying pressure and stock flow deviation."*

---

### 📝 Feature 3: Global Live Advisory Prompt Banner ⚡
* **Cross-Tab Banner**: Prompts operators on **any tab** (Overview, Live Monitoring, etc.).
* **1-Click Execution**: **`[ Accept & Apply Setpoint ]`** button instantly adjusts simulator state and recovers machine stability.

---

### 📝 Feature 4: Measured Impact History Log 📜
* **Stabilization Metrics**: Logs initial vs final risk (`85% → 5%`) and BW deviation (`+3.2% → -0.1%`).
* **Recovery Benchmark**: Proves recovery completion within **28 seconds**.

---

## 🔹 Slide 6: Research, Future Scope & Closing

### 📌 Layout & Visual Concept
* **Layout**: 2 Columns (References vs Future Roadmap) + Bold Closing Tagline.

---

### 📝 Left Column: References & Industry Standards 📚
* **Honeywell QCS & MD Control Specs**: Multi-variable cross-directional and machine-direction control standards.
* **XGBoost & TreeSHAP Literature**: Lundberg & Lee (2017) *A Unified Approach to Interpreting Model Predictions*.
* **Granger Causality in Process Control**: Identification of dynamic delays in industrial process loops.

---

### 📝 Right Column: Future Roadmap 🚀
* **Reinforcement Learning (RL)**: Self-optimizing ramping trajectories for autonomous grade transitions.
* **Edge AI Integration**: Deployment directly on Honeywell Experion PKS edge nodes.
* **Digital Twin Expansion**: Full 3D wet-end to reel physical simulation.
* **Honeywell Forge Integration**: Enterprise cloud analytics sync across multi-mill fleets.

---

### 🎯 Closing Tagline
> # **Predict Earlier. Explain Clearly. Optimize Smarter.**
> **GradeSense AI — Next-Generation Paper Machine Intelligence**
