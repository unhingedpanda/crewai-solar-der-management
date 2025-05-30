"""
Solar Agent Tools for interacting with the mock SunSpec solar inverter data.
These tools provide string-based outputs suitable for LLM agents.
"""
from crewai.tools import tool
from mocks import sunspec_solar_mock


@tool
def read_current_ac_measurements() -> str:
    """
    Reads the current AC electrical measurements from the solar inverter, 
    including power, voltage, current, frequency, and any active alarms. 
    Returns a string summary.
    """
    data = sunspec_solar_mock.get_701_data()
    
    # Convert scaled values to actual values
    power_w = data["W"]
    voltage_v = data["VL1N"] * (10 ** data["V_SF"])
    current_a = data["A"] * (10 ** data["A_SF"])
    frequency_hz = data["Hz"] * (10 ** data["Hz_SF"])
    apparent_power_va = data["VA"]
    alarms = data["Alrm"]
    operating_state = data["St"]
    inverter_state = data["InvSt"]
    
    # Interpret states
    op_state_str = {0: "Off", 1: "Sleeping", 2: "Starting", 3: "MPPT", 4: "Throttled", 5: "Shutting Down", 6: "Fault", 7: "Standby"}.get(operating_state, f"Unknown({operating_state})")
    inv_state_str = {1: "Off", 2: "Sleeping", 3: "Starting", 4: "MPPT", 5: "Running", 6: "Power Limiting", 7: "Shutting Down", 8: "Fault", 9: "Standby"}.get(inverter_state, f"Unknown({inverter_state})")
    
    # Format alarm information
    alarm_info = "None" if alarms == 0 else f"Active (Code: {alarms})"
    if alarms == 1024:
        alarm_info += " - AC Over-Voltage Detected"
    
    summary = f"""Solar Inverter AC Measurements (SunSpec Model 701):
├── Power Output: {power_w} W
├── Apparent Power: {apparent_power_va} VA
├── Voltage (L1-N): {voltage_v:.1f} V
├── Current: {current_a:.2f} A
├── Frequency: {frequency_hz:.2f} Hz
├── Operating State: {op_state_str}
├── Inverter State: {inv_state_str}
└── Alarms: {alarm_info}"""
    
    return summary


@tool
def read_current_control_settings() -> str:
    """
    Reads the current active power control settings from the solar inverter, 
    such as the power setpoint and if it's enabled. Returns a string summary.
    """
    data = sunspec_solar_mock.get_704_state()
    
    power_setpoint = data["WSet"]
    setpoint_enabled = data["WSetEna"]
    max_capacity = sunspec_solar_mock.get_max_capacity()
    
    status = "Enabled" if setpoint_enabled else "Disabled"
    
    summary = f"""Solar Inverter Control Settings (SunSpec Model 704):
├── Power Setpoint: {power_setpoint} W
├── Setpoint Status: {status}
├── Maximum Capacity: {max_capacity} W
└── Current Limit: {power_setpoint if setpoint_enabled else max_capacity} W (Effective)"""
    
    return summary


@tool
def set_active_power_output_limit(target_watts: int, enable: bool) -> str:
    """
    Sets the active power output limit on the solar inverter.
    
    Args:
        target_watts (int): The desired power limit in Watts.
        enable (bool): True to enable the limit, False to disable it.
    """
    result = sunspec_solar_mock.apply_704_control(target_watts, enable)
    
    if result["status"] == "success":
        new_state = result["new_state"]
        confirmation = f"""✅ Solar Inverter Control Command Applied Successfully:
├── Command: Set power limit to {target_watts} W, Enable: {enable}
├── Result: {result['message']}
├── New Power Setpoint: {new_state['WSet']} W
├── New Setpoint Status: {'Enabled' if new_state['WSetEna'] else 'Disabled'}
└── Effective Limit: {new_state['WSet'] if new_state['WSetEna'] else sunspec_solar_mock.get_max_capacity()} W"""
    else:
        confirmation = f"❌ Control command failed: {result.get('message', 'Unknown error')}"
    
    return confirmation


@tool
def get_power_generation_forecast(horizon_hours: int) -> str:
    """
    Generates a power generation forecast for the solar inverter for a 
    specified number of hours ahead.
    
    Args:
        horizon_hours (int): The number of hours into the future to forecast.
    """
    result = sunspec_solar_mock.generate_simple_forecast(horizon_hours)
    
    if result["status"] == "success":
        forecast_data = result["forecast"]
        timeseries = forecast_data["timeseries"]
        total_kwh = forecast_data["total_kwh"]
        generated_at = forecast_data["generated_at"]
        
        forecast_str = f"""📊 Solar Power Generation Forecast:
├── Forecast Period: {horizon_hours} hours
├── Generated At: {generated_at}
├── Total Expected Energy: {total_kwh} kWh
└── Hourly Breakdown:"""
        
        for entry in timeseries:
            forecast_str += f"\n    {entry['timestamp']}: {entry['power_w']} W"
        
        # Add summary statistics
        powers = [entry['power_w'] for entry in timeseries]
        avg_power = sum(powers) / len(powers)
        max_power = max(powers)
        min_power = min(powers)
        
        forecast_str += f"""
├── Average Power: {avg_power:.0f} W
├── Peak Power: {max_power} W
└── Minimum Power: {min_power} W"""
        
    else:
        forecast_str = f"❌ Forecast generation failed: {result.get('message', 'Unknown error')}"
    
    return forecast_str


@tool
def check_for_voltage_anomalies_and_report() -> str:
    """
    Checks the solar inverter for any voltage anomalies based on its alarm status 
    and current voltage readings. Reports if an anomaly is found or if conditions are nominal.
    """
    data = sunspec_solar_mock.get_701_data()
    
    alarms = data["Alrm"]
    voltage_v = data["VL1N"] * (10 ** data["V_SF"])
    
    # Check for voltage-related alarms
    if alarms == 1024:  # AC Over-Voltage (bit 10)
        return f"""🚨 ALERT: Voltage anomaly detected!
├── Alarm Type: AC Over-Voltage
├── Current Voltage: {voltage_v:.1f} V
├── Alarm Code: {alarms}
├── Status: CRITICAL - Immediate attention required
└── Recommendation: Check grid voltage conditions and consider disconnection if unsafe"""
    
    elif alarms & (1 << 11):  # AC Under-Voltage (bit 11)
        return f"""🚨 ALERT: Voltage anomaly detected!
├── Alarm Type: AC Under-Voltage  
├── Current Voltage: {voltage_v:.1f} V
├── Alarm Code: {alarms}
├── Status: WARNING - Monitor closely
└── Recommendation: Check grid stability and inverter connections"""
    
    elif alarms != 0:
        return f"""⚠️ Non-voltage alarm detected:
├── Current Voltage: {voltage_v:.1f} V (Normal)
├── Alarm Code: {alarms}
└── Status: Other system alarm active - investigate further"""
    
    else:
        return f"""✅ No voltage anomalies detected. System nominal.
├── Current Voltage: {voltage_v:.1f} V
├── Voltage Range: Normal (typically 230-250V)
├── Alarm Status: Clear
└── System Status: Operating normally""" 