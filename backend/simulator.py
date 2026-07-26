import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional

# Recipe Specifications for Grades
GRADES = {
    1: {
        "name": "Cardboard Light (120g)",
        "basis_weight": 120.0,
        "moisture": 6.8,
        "ash": 8.0,
        "machine_speed": 500.0,
        "stock_flow": 2500.0,
        "filler_flow": 200.0,
        "steam_pressure": 30.0,
        "caliper": 150.0
    },
    2: {
        "name": "Standard Packaging (150g)",
        "basis_weight": 150.0,
        "moisture": 7.2,
        "ash": 10.0,
        "machine_speed": 450.0,
        "stock_flow": 3100.0,
        "filler_flow": 310.0,
        "steam_pressure": 35.0,
        "caliper": 185.0
    },
    3: {
        "name": "Heavy Duty Kraft (200g)",
        "basis_weight": 200.0,
        "moisture": 6.5,
        "ash": 12.0,
        "machine_speed": 380.0,
        "stock_flow": 4100.0,
        "filler_flow": 490.0,
        "steam_pressure": 42.0,
        "caliper": 240.0
    }
}

class GradeChangeSimulator:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.current_grade_id = 1
        self.target_grade_id = 1
        self.in_transition = False
        self.transition_time = 0
        self.transition_duration = 300  # seconds
        
        # Initialize state with Grade 1
        g = GRADES[1]
        self.state = {
            "timestamp": 0,
            "recipe_id": 1,
            "basis_weight": g["basis_weight"],
            "moisture": g["moisture"],
            "ash": g["ash"],
            "machine_speed": g["machine_speed"],
            "stock_flow": g["stock_flow"],
            "filler_flow": g["filler_flow"],
            "steam_pressure": g["steam_pressure"],
            "caliper": g["caliper"],
            
            # Target setpoints (from QCS)
            "basis_weight_sp": g["basis_weight"],
            "moisture_sp": g["moisture"],
            "ash_sp": g["ash"],
            "machine_speed_sp": g["machine_speed"],
            "stock_flow_sp": g["stock_flow"],
            "filler_flow_sp": g["filler_flow"],
            "steam_pressure_sp": g["steam_pressure"],
            
            # Anomaly status
            "anomaly_type": None,  # None, "steam_lag", "excessive_stock", "speed_surge"
            "alarm_count": 0,
            "operator_action": "Stable operation"
        }
        
        # History log for dashboard replay
        self.history: List[Dict[str, Any]] = [self.state.copy()]
        
    def start_transition(self, target_id: int, anomaly_type: Optional[str] = None):
        if target_id not in GRADES:
            return False
        self.target_grade_id = target_id
        self.in_transition = True
        self.transition_time = 0
        self.state["anomaly_type"] = anomaly_type
        self.state["operator_action"] = f"Initiated transition to Grade {target_id}"
        return True

    def step(self) -> Dict[str, Any]:
        self.state["timestamp"] += 1
        
        g_start = GRADES[self.current_grade_id]
        g_target = GRADES[self.target_grade_id]
        
        if self.in_transition:
            self.transition_time += 1
            progress = min(1.0, self.transition_time / self.transition_duration)
            
            # Setpoints ramp smoothly following QCS MD control trajectory
            self.state["basis_weight_sp"] = g_start["basis_weight"] + progress * (g_target["basis_weight"] - g_start["basis_weight"])
            self.state["moisture_sp"] = g_start["moisture"] + progress * (g_target["moisture"] - g_start["moisture"])
            self.state["ash_sp"] = g_start["ash"] + progress * (g_target["ash"] - g_start["ash"])
            self.state["machine_speed_sp"] = g_start["machine_speed"] + progress * (g_target["machine_speed"] - g_start["machine_speed"])
            self.state["stock_flow_sp"] = g_start["stock_flow"] + progress * (g_target["stock_flow"] - g_start["stock_flow"])
            self.state["filler_flow_sp"] = g_start["filler_flow"] + progress * (g_target["filler_flow"] - g_start["filler_flow"])
            self.state["steam_pressure_sp"] = g_start["steam_pressure"] + progress * (g_target["steam_pressure"] - g_start["steam_pressure"])
            
            # Dynamic simulation of actuator physical values with lags
            # Define time constants (tau) and delays (dead time)
            # 1. Machine Speed (fast response)
            self.state["machine_speed"] += (self.state["machine_speed_sp"] - self.state["machine_speed"]) * 0.05 + np.random.normal(0, 0.2)
            
            # 2. Stock Flow (medium response)
            sf_target = self.state["stock_flow_sp"]
            if self.state["anomaly_type"] == "excessive_stock":
                # Stock flow ramps faster than target to cause overshoot
                sf_target += (g_target["stock_flow"] - g_start["stock_flow"]) * 0.15
            self.state["stock_flow"] += (sf_target - self.state["stock_flow"]) * 0.04 + np.random.normal(0, 1.0)
            
            # 3. Filler Flow (medium response)
            self.state["filler_flow"] += (self.state["filler_flow_sp"] - self.state["filler_flow"]) * 0.04 + np.random.normal(0, 0.5)
            
            # 4. Steam Pressure (slow thermal response)
            steam_target = self.state["steam_pressure_sp"]
            if self.state["anomaly_type"] == "steam_lag":
                # Steam lag: steam pressure response is extremely slow
                self.state["steam_pressure"] += (steam_target - self.state["steam_pressure"]) * 0.005 + np.random.normal(0, 0.05)
            else:
                self.state["steam_pressure"] += (steam_target - self.state["steam_pressure"]) * 0.02 + np.random.normal(0, 0.05)
                
            # Physics equations for quality parameters (Basis Weight, Moisture, Ash, Caliper)
            base_bw = self.state["basis_weight_sp"] * (self.state["stock_flow"] / self.state["stock_flow_sp"]) / (self.state["machine_speed"] / self.state["machine_speed_sp"])
            self.state["basis_weight"] += (base_bw - self.state["basis_weight"]) * 0.1 + np.random.normal(0, 0.05)
            
            # Ash content: driven by filler flow
            base_ash = self.state["ash_sp"] * (self.state["filler_flow"] / self.state["filler_flow_sp"]) / (self.state["stock_flow"] / self.state["stock_flow_sp"])
            self.state["ash"] += (base_ash - self.state["ash"]) * 0.05 + np.random.normal(0, 0.02)
            
            # Moisture: affected by drying (steam pressure) and stock flow (water load)
            base_moisture = self.state["moisture_sp"] + 0.002 * (self.state["stock_flow"] - self.state["stock_flow_sp"]) - 0.25 * (self.state["steam_pressure"] - self.state["steam_pressure_sp"]) + 0.005 * (self.state["machine_speed"] - self.state["machine_speed_sp"])
            self.state["moisture"] += (base_moisture - self.state["moisture"]) * 0.08 + np.random.normal(0, 0.01)
            
            # Caliper: proportional to basis weight
            base_caliper = self.state["basis_weight"] * (g_target["caliper"] / g_target["basis_weight"])
            self.state["caliper"] += (base_caliper - self.state["caliper"]) * 0.1
            
            # Check if transition complete
            if progress >= 1.0:
                # Wait for values to stabilize
                deviation = abs(self.state["basis_weight"] - g_target["basis_weight"]) / g_target["basis_weight"]
                if deviation < 0.01:
                    self.in_transition = False
                    self.current_grade_id = self.target_grade_id
                    self.state["recipe_id"] = self.target_grade_id
                    self.state["operator_action"] = f"Completed transition to Grade {self.target_grade_id}"
                    
        else:
            # Steady state - small noise and corrections
            g = GRADES[self.current_grade_id]
            self.state["machine_speed"] += (g["machine_speed"] - self.state["machine_speed"]) * 0.1 + np.random.normal(0, 0.1)
            self.state["stock_flow"] += (g["stock_flow"] - self.state["stock_flow"]) * 0.1 + np.random.normal(0, 0.5)
            self.state["filler_flow"] += (g["filler_flow"] - self.state["filler_flow"]) * 0.1 + np.random.normal(0, 0.2)
            self.state["steam_pressure"] += (g["steam_pressure"] - self.state["steam_pressure"]) * 0.1 + np.random.normal(0, 0.02)
            
            base_bw = g["basis_weight"] * (self.state["stock_flow"] / g["stock_flow"]) / (self.state["machine_speed"] / g["machine_speed"])
            self.state["basis_weight"] += (base_bw - self.state["basis_weight"]) * 0.2 + np.random.normal(0, 0.02)
            
            base_ash = g["ash"] * (self.state["filler_flow"] / g["filler_flow"]) / (self.state["stock_flow"] / g["stock_flow"])
            self.state["ash"] += (base_ash - self.state["ash"]) * 0.1 + np.random.normal(0, 0.01)
            
            base_moisture = g["moisture"] + 0.002 * (self.state["stock_flow"] - g["stock_flow"]) - 0.25 * (self.state["steam_pressure"] - g["steam_pressure"]) + 0.005 * (self.state["machine_speed"] - g["machine_speed"])
            self.state["moisture"] += (base_moisture - self.state["moisture"]) * 0.1 + np.random.normal(0, 0.01)
            
            base_caliper = self.state["basis_weight"] * (g["caliper"] / g["basis_weight"])
            self.state["caliper"] += (base_caliper - self.state["caliper"]) * 0.1
            
        # Detect breaches (> ±2.5% Basis Weight deviation from setpoint)
        bw_dev = (self.state["basis_weight"] - self.state["basis_weight_sp"]) / self.state["basis_weight_sp"]
        if abs(bw_dev) > 0.025:
            self.state["alarm_count"] = min(5, self.state["alarm_count"] + 1)
        else:
            self.state["alarm_count"] = max(0, self.state["alarm_count"] - 1)
            
        self.state["in_transition"] = self.in_transition
        self.state["transition_time"] = self.transition_time
        self.state["transition_duration"] = self.transition_duration
        self.state["target_grade_id"] = self.target_grade_id
            
        self.history.append(self.state.copy())
        return self.state

    def get_history_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.history)
        
    def generate_training_runs(self, count: int = 10) -> pd.DataFrame:
        """Generate multiple transition runs (some successful, some failures) for model training."""
        all_data = []
        for run_idx in range(count):
            self.reset()
            # Randomize start/end grades
            start_g = np.random.choice([1, 2, 3])
            end_g = np.random.choice([g for g in [1, 2, 3] if g != start_g])
            
            # Setup start state
            self.current_grade_id = start_g
            self.target_grade_id = start_g
            g = GRADES[start_g]
            self.state.update({
                "recipe_id": start_g,
                "basis_weight": g["basis_weight"],
                "moisture": g["moisture"],
                "ash": g["ash"],
                "machine_speed": g["machine_speed"],
                "stock_flow": g["stock_flow"],
                "filler_flow": g["filler_flow"],
                "steam_pressure": g["steam_pressure"],
                "caliper": g["caliper"],
                "basis_weight_sp": g["basis_weight"],
                "moisture_sp": g["moisture"],
                "ash_sp": g["ash"],
                "machine_speed_sp": g["machine_speed"],
                "stock_flow_sp": g["stock_flow"],
                "filler_flow_sp": g["filler_flow"],
                "steam_pressure_sp": g["steam_pressure"],
            })
            
            # Determine anomaly
            anomaly = None
            if np.random.rand() > 0.4:
                anomaly = np.random.choice(["steam_lag", "excessive_stock", "speed_surge"])
                
            self.start_transition(end_g, anomaly)
            
            # Run simulation for 350 steps
            for step_idx in range(350):
                row = self.step()
                row_copy = row.copy()
                row_copy["run_id"] = run_idx
                row_copy["anomaly_type_label"] = anomaly if anomaly else "normal"
                all_data.append(row_copy)
                
        self.reset()  # Restore to clean state
        return pd.DataFrame(all_data)
