"""
Mock SunSpec data and functionality for simulating a solar inverter.
Implements SunSpec Model 701 (AC Measurement) and Model 704 (AC Controls).
"""
import random
import time
from typing import Dict, Any

# State Variables
_solar_model_701_data = {
    "ID": 701,  # SunSpec Model 701 - AC Measurement
    "L": 50,    # Length
    "W": 2500,  # Active Power (Watts) - base value, will be randomized
    "VA": 2600, # Apparent Power (VA)
    "Hz": 6000, # Frequency (scaled by Hz_SF)
    "VL1N": 2400, # Voltage L1-N (scaled by V_SF)
    "A": 1042,  # Current (scaled by A_SF)
    "Alrm": 0,  # Alarm Bitfield
    "St": 1,    # Operating State (1 = On)
    "InvSt": 3, # Inverter State (3 = Running)
    "W_SF": 0,  # Scale factor for Watts
    "V_SF": -1, # Scale factor for Voltage (240.0V)
    "Hz_SF": -2, # Scale factor for Frequency (60.00Hz)
    "A_SF": -2,  # Scale factor for Current (10.42A)
    "VA_SF": 0   # Scale factor for Apparent Power
}

_solar_model_704_state = {
    "ID": 704,     # SunSpec Model 704 - AC Controls
    "L": 8,        # Length
    "WSet": 3000,  # Active Power Setpoint (Watts)
    "WSetEna": True, # Setpoint Enable
    "WSet_SF": 0   # Scale factor for WSet
}

_max_capacity_watts = 3000
_simulated_voltage_anomaly = False
_base_power_output = 2500  # Base power for randomization


def get_701_data() -> Dict[str, Any]:
    """
    Get current AC measurement data from SunSpec Model 701.
    Randomizes power output and updates related values.
    """
    global _solar_model_701_data, _simulated_voltage_anomaly
    
    # Randomize power output within +/- 10% of base value
    variation = random.uniform(-0.1, 0.1)
    new_power = int(_base_power_output * (1 + variation))
    
    # Ensure power doesn't exceed the current setpoint from Model 704
    max_allowed = _solar_model_704_state["WSet"] if _solar_model_704_state["WSetEna"] else _max_capacity_watts
    new_power = min(new_power, max_allowed)
    
    _solar_model_701_data["W"] = new_power
    
    # Update apparent power (assume power factor of ~0.96)
    _solar_model_701_data["VA"] = int(new_power / 0.96)
    
    # Update current based on power and voltage (P = V * I)
    voltage_actual = _solar_model_701_data["VL1N"] * (10 ** _solar_model_701_data["V_SF"])
    if voltage_actual > 0:
        current_actual = new_power / voltage_actual
        _solar_model_701_data["A"] = int(current_actual * (10 ** (-_solar_model_701_data["A_SF"])))
    
    # Handle voltage anomaly simulation
    if _simulated_voltage_anomaly:
        # Set alarm bit for voltage anomaly (bit 10 for AC_OVER_VOLT)
        _solar_model_701_data["Alrm"] = 1024  # 2^10
        # Simulate over-voltage condition
        _solar_model_701_data["VL1N"] = 2650  # 265.0V when scaled
    else:
        _solar_model_701_data["Alrm"] = 0
        _solar_model_701_data["VL1N"] = 2400  # Normal 240.0V when scaled
    
    return _solar_model_701_data.copy()


def get_704_state() -> Dict[str, Any]:
    """Get current AC control state from SunSpec Model 704."""
    return _solar_model_704_state.copy()


def apply_704_control(target_w_set: int, enable_w_set: bool) -> Dict[str, Any]:
    """
    Apply control settings to SunSpec Model 704.
    
    Args:
        target_w_set: Desired power setpoint in Watts
        enable_w_set: Whether to enable the power setpoint
    
    Returns:
        Dictionary with status and new state
    """
    global _solar_model_704_state
    
    # Clamp target between 0 and max capacity
    clamped_target = max(0, min(target_w_set, _max_capacity_watts))
    
    _solar_model_704_state["WSet"] = clamped_target
    _solar_model_704_state["WSetEna"] = enable_w_set
    
    return {
        "status": "success",
        "message": f"Control applied. Power setpoint: {clamped_target}W, Enabled: {enable_w_set}",
        "new_state": _solar_model_704_state.copy()
    }


def generate_simple_forecast(horizon_hours: int) -> Dict[str, Any]:
    """
    Generate a simple power generation forecast.
    
    Args:
        horizon_hours: Number of hours to forecast
    
    Returns:
        Dictionary with forecast data
    """
    current_data = get_701_data()
    current_power = current_data["W"]
    
    # Simple forecast: assume current output with some variation
    timeseries = []
    total_kwh = 0
    
    for hour in range(horizon_hours):
        # Simulate natural variation and solar curve
        if hour < horizon_hours / 2:
            # First half: slight increase (morning ramp)
            factor = 1.0 + (hour * 0.05)
        else:
            # Second half: gradual decrease (afternoon decline)
            factor = 1.0 + ((horizon_hours - hour) * 0.05)
        
        # Add some randomness
        factor *= random.uniform(0.9, 1.1)
        forecast_power = min(int(current_power * factor), _max_capacity_watts)
        
        timeseries.append({
            "hour": hour + 1,
            "power_w": forecast_power,
            "timestamp": f"T+{hour+1:02d}:00"
        })
        
        total_kwh += forecast_power / 1000  # Convert to kWh
    
    return {
        "status": "success",
        "forecast": {
            "timeseries": timeseries,
            "total_kwh": round(total_kwh, 2),
            "horizon_hours": horizon_hours,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    }


def toggle_voltage_anomaly_simulation() -> bool:
    """
    Toggle the voltage anomaly simulation flag.
    
    Returns:
        New state of the voltage anomaly flag
    """
    global _simulated_voltage_anomaly
    _simulated_voltage_anomaly = not _simulated_voltage_anomaly
    return _simulated_voltage_anomaly


def get_max_capacity() -> int:
    """Get the maximum capacity of the solar system in Watts."""
    return _max_capacity_watts 