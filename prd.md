# PRD — Grade Change Intelligence in Paper Making Process

## 1. Problem Statement
Develop an intelligent, automatic **grade change system** for paper-making processes that **predicts process deviation from system specification** occurring during a grade change in the paper-making process.

## 2. Background
Honeywell's Quality Control System (**QCS**) already provides automatic grade-change support for Machine Direction (**MD**) via Multivariable Model Predictive Control — operator displays for selecting/monitoring the grade, target calculation, trajectory calculation, readiness checks, and coordinated ramping of variables such as stock flow, filler flow, dryer steam pressures, and reel/machine speed.

Per internal benchmarks and customer site results, this existing solution already gives significant reductions in grade-change losses and faster grade-change execution vs. manual/previous control methods. **Current capability is therefore a strong control backbone** — the hackathon is not about replacing it, but adding an intelligence layer on top of it.

## 3. Challenges With Current System
- **Grade changes are high-loss events** — even with MD Control outperforming previous methods, transitions still often produce off-spec paper, broke, or culled material while quality variables stabilize.
- **Operators manage many variables simultaneously** — stock flow, filler flow, steam pressure, machine speed, basis weight, moisture, ash, caliper, recipe limits, actuator constraints, and dynamically interacting disturbances.
- **Traditional automation executes but does not learn** — current systems calculate targets/trajectories and execute coordinated ramps, but there's no intelligence layer that learns from similar historical transitions and gives context-aware guidance.
- **Experienced operator knowledge is scarce** — skill shortages and loss of tacit papermaking intuition mean newer operators need guidance that explains *what* is happening and *why* a recommended action is appropriate.
- **Site data is underused** — QCS history, MIS reports, DCS historian trends, operator actions, alarm history, and scanner diagnostics are stored but rarely converted into actionable real-time guidance.

## 4. Hackathon Challenge — Build a System That Can:
1. **Predict** when the system specification for the main variable **Basis Weight** is at risk of going off-spec (deviates more than **±2.5%** from the setpoint) during transition of grades (auto grade/recipe change), and **recommend corrective action** before quality limits are exceeded.
2. **Recommend setpoints** to keep the system in safe operating limits.
3. **Reduce stabilization time** to reach steady state.
4. **Provide rationale** behind every prediction/recommendation (explainability is a major judging criterion).

## 5. Constraints
- Use process limits from the recipe, historical operator action data, historical trends and trajectories during failure and success scenarios.
- Use historical data to find correlations across loops/system parameters: stock flow, filler flow, steam pressure, machine speed, moisture, ash, caliper, recipe limits.
- Find **new correlations** not already defined in the system, but that may have impacted the process, along with the loops defined above.

## 6. Deliverables (submit as PDF/Zip via "Upload Files")
1. A working solution that solves the challenge.
2. Documentation of the building blocks — clearly showing communication between modules, with a brief explanation of each.
3. A **dashboard** showing:
   - New correlations found by the solution and their impact on the system.
   - Future state if deviations in correlated parameters follow the current trend/trajectory.
   - Suggested setpoints to keep the system within operational limits.
4. Dashboard must also show:
   - Loops/parameters causing high impact on stabilization.
   - Suggested setpoints to stabilize the system faster, based on historical data.
5. Every suggestion must be **tagged with its source of inference** (historical data, recipe, etc.).
6. Solution must let a user **accept or reject** a suggestion, and record these responses to evaluate suggestion quality/accuracy over time.
7. A presentation about the solution (using Honeywell's provided template).

## 7. Success Criteria (how judges will likely score this)
| Criterion | What "great" looks like |
|---|---|
| Prediction accuracy | Basis Weight ±2.5% deviation predicted with meaningful lead time (not just after the fact) |
| Recommendation quality | Actionable, quantified setpoint changes (e.g. "reduce stock flow by 3%"), not vague risk flags |
| Explainability | Every prediction/recommendation traceable to specific contributing variables and a data source |
| Correlation discovery | Surfaces *new* relationships beyond the ones already coded into QCS |
| Stabilization impact | Demonstrable reduction in time-to-steady-state vs. historical baseline |
| Feedback loop | Accept/reject captured and shown to influence future suggestions |
| Presentation/demo | Clear narrative: detect → explain → recommend → simulate → learn |

## 8. Non-Goals (for hackathon scope)
- Replacing Honeywell's existing MD Control / MPC trajectory execution.
- Real closed-loop control of actual plant hardware (a **simulated/what-if** environment is acceptable and expected).
- Full production-grade security/auth (basic auth is enough for a demo).

## 9. Target Users
- **Process operators** (need clear, fast, trustworthy guidance during a live transition).
- **Process/quality engineers** (need correlation discovery and root-cause explanations).
- **Shift supervisors** (need dashboard-level visibility and alarm summaries).

## 10. Primary Variable Being Predicted
**Basis Weight** — deviation > **±2.5%** from recipe setpoint = off-spec / failure event.
Secondary monitored variables: Moisture, Ash, Caliper, Stock Flow, Filler Flow, Steam Pressure, Machine Speed.
