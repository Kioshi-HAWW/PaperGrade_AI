# GradeSense AI — Grade Change Intelligence in Paper Making Process

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)

**GradeSense AI** is an intelligent advisory layer built on top of Honeywell's Quality Control System (**QCS**) and Machine Direction (**MD**) Multivariable Control. During paper machine grade transitions (recipe changes), the platform predicts **Basis Weight deviation risk (>±2.5%)** in advance, explains *why* using TreeSHAP feature attributions, recommends quantified corrective setpoints, and captures operator feedback to evaluate suggestion accuracy over time.

---

## 📸 Dashboard Screenshots & User Interface

> *Place your actual dashboard screenshots inside the `docs/screenshots/` directory.*

### 1. Dashboard Overview & Real-Time Telemetry
![Dashboard Overview](docs/screenshots/overview.png)
*Real-time multi-variable trend charts, active grade regime status, animated KPIs (Basis Weight, Moisture, Speed, Steam), and live prediction risk gauge.*

---

### 2. AI Predictions & TreeSHAP Feature Attributions
![AI Predictions & SHAP Explanation](docs/screenshots/predictions.png)
*Large 0–100% risk gauge, target breach margins (±2.5%), SHAP contribution percentages, and plain-language explanation sentences.*

---

### 3. Actionable Operational Advisory & Prompt Banner
![Actionable Operational Advisory](docs/screenshots/advisory.png)
*Quantified setpoint changes (e.g., "Reduce Stock Flow by 3.5%"), source of inference tags, Accept/Reject controls, and the floating live prompt banner.*

---

### 4. What-if Scenario Simulator (Digital Twin)
![What-if Simulator](docs/screenshots/simulator.png)
*Interactive sliders for Stock Flow, Steam Pressure, and Machine Speed allowing operators to simulate control setpoint deltas and observe projected risk reductions in real-time.*

---

### 5. Dynamic Correlation Explorer
![Correlation Explorer](docs/screenshots/correlations.png)
*Interactive process loop network SVG graph displaying newly discovered Granger causality and Pearson linear associations between process parameters.*

---

## 🎯 Key Features & Requirements Compliance

* **Predictive Risk Modeling**: Predicts Basis Weight setpoint breaches (>±2.5%) up to 120 seconds in advance using an XGBoost classifier.
* **Explainable AI (SHAP)**: Explains every prediction with feature contributions and plain-language summaries (e.g., *"Risk is driven by high steam drying pressure and stock flow deviation"*).
* **Quantified Advisory Setpoints**: Recommends explicit numerical setpoint deltas tagged with their source of inference (`Physical Material Balance Recipe Rule`, `Thermal Drying Loop Granger Discovery`).
* **Global Live Advisory Banner**: Prompts operators directly on whatever tab they are currently viewing (Overview, Live Monitoring, etc.) with a 1-click **Accept & Apply Setpoint** action.
* **Operator Feedback Loop**: Captures Accept/Reject responses and records execution history with measured quality evaluation metrics.
* **Dynamic Correlation Discovery**: Surfaces undocumented loop relationships (e.g. Steam Pressure ↔ Moisture delay) beyond pre-coded QCS loops.
* **Non-Disruptive Advisory Layer**: Pure simulated/what-if intelligence layer — no closed-loop plant overrides.

---

## 🏗 System Architecture & Data Flow

```
Historical / Simulated Sensor Telemetry (Stock, Steam, Speed, Moisture, Ash, Caliper)
        │
        ▼
Data Ingestion & Cleaning Layer
        │
        ▼
Windowed Feature Engineering (15s Rolling Mean, Std, Slope & Recipe Errors)
        │
        ▼
Correlation Engine (Granger Causality & Pearson Pairwise Associations)
        │
        ▼
Prediction Engine (XGBoost Classifier ──► Basis Weight ±2.5% Breach Probability)
        │
        ▼
Explainability Layer (TreeSHAP Attributions ──► Plain-Language Explanation String)
        │
        ▼
Quantified Recommendation Engine (Setpoint Deltas + Source-of-Inference Tag)
        │
        ▼
WebSockets / REST API (FastAPI Backend Server)
        │
        ▼
Interactive Dashboard (HTML5 + Tailwind CSS + ECharts SPA)
        │
        ▼
Operator Feedback Capture (Accept / Reject ──► Quality Evaluation Log)
```

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend API** | Python 3.12, FastAPI, Uvicorn |
| **Real-time Streaming** | WebSockets |
| **Machine Learning** | XGBoost, Scikit-learn, Pandas, NumPy, SciPy |
| **Explainable AI** | SHAP (TreeExplainer) |
| **Frontend UI** | Vanilla JavaScript, Tailwind CSS (CDN), Lucide Icons |
| **Charts & Network Graph** | Apache ECharts, SVG Network Renderer |
| **Containerization** | Docker, Render.yaml Blueprint |

---

## 🚀 Quickstart & Local Setup

### Prerequisites
* Python 3.10 or higher installed.

### Installation
1. Clone repository:
   ```bash
   git clone https://github.com/Kioshi-HAWW/PaperGrade_AI.git
   cd PaperGrade_AI
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Train the XGBoost breach prediction model:
   ```bash
   python ml/train_model.py
   ```

4. Launch the FastAPI server:
   ```bash
   python backend/main.py
   ```

5. Open your browser and navigate to:
   ```text
   http://localhost:8000/
   ```

---

## ☁️ Deployment on Render.com

This repository includes a pre-configured `Dockerfile` and `render.yaml` blueprint.

1. Push code to GitHub.
2. Log in to [Render Dashboard](https://dashboard.render.com).
3. Click **New +** > **Blueprint** and connect this repository.
4. Render will automatically build the container and deploy your live HTTPS web service.

---

## 📜 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
