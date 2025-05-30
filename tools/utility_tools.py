"""
Utility Agent Tools for analyzing grid conditions and making operational decisions.
"""
from crewai.tools import tool
import re


@tool
def analyze_solar_and_grid_conditions(
    solar_status_report: str, 
    solar_forecast_report: str, 
    current_grid_demand_kw: float, 
    dr_event_active: bool
) -> str:
    """
    Analyzes solar status, forecast, current grid demand, and DR event status 
    to recommend actions for the Utility Agent regarding solar management.
    
    Args:
        solar_status_report (str): Report from solar agent.
        solar_forecast_report (str): Forecast from solar agent.
        current_grid_demand_kw (float): Current grid load in kW.
        dr_event_active (bool): True if a demand response event is active.
    """
    
    # Extract current power from solar status report
    current_power_w = _extract_current_power(solar_status_report)
    current_power_kw = current_power_w / 1000 if current_power_w else 0
    
    # Extract forecast information
    forecast_peak_kw, forecast_avg_kw = _extract_forecast_powers(solar_forecast_report)
    
    # Decision logic
    recommendations = []
    
    # Check if DR event is active
    if dr_event_active:
        if current_power_w and current_power_w > 500:
            # Curtail by at least 30% but not below 200W
            target_power = max(int(current_power_w * 0.7), 200)
            recommendations.append(f"🔴 DR EVENT ACTIVE: Immediate curtailment required")
            recommendations.append(f"   Curtail solar from {current_power_w}W to {target_power}W (30% reduction)")
            recommendations.append(f"   Reason: Demand Response compliance")
        else:
            recommendations.append(f"🟡 DR EVENT ACTIVE: Current output {current_power_w}W is below curtailment threshold")
    
    # Check grid demand vs solar output conditions
    elif current_grid_demand_kw < 1.0 and current_power_w > 1500:
        # Low grid demand with high solar output
        target_power = 1000
        recommendations.append(f"🟠 GRID OVERGENERATION RISK: Low demand ({current_grid_demand_kw:.1f} kW) with high solar ({current_power_kw:.1f} kW)")
        recommendations.append(f"   Curtail solar to {target_power}W to prevent grid instability")
        recommendations.append(f"   Reason: Grid demand below 1000kW threshold")
    
    # Check forecast conditions for proactive management
    elif forecast_peak_kw and forecast_peak_kw > 2.5 and current_grid_demand_kw < 1.5:
        recommendations.append(f"⚠️ FORECAST ALERT: High solar production expected ({forecast_peak_kw:.1f} kW peak)")
        recommendations.append(f"   With moderate grid demand ({current_grid_demand_kw:.1f} kW), prepare for potential curtailment")
        recommendations.append(f"   Consider proactive curtailment if conditions worsen")
    
    # Normal operation
    else:
        recommendations.append(f"✅ NORMAL OPERATION: No immediate action required")
        recommendations.append(f"   Solar: {current_power_kw:.1f} kW, Grid Demand: {current_grid_demand_kw:.1f} kW")
        recommendations.append(f"   System operating within normal parameters")
    
    # Compile final recommendation
    analysis_result = f"""🏭 Grid Operations Analysis:
═══════════════════════════════════════════════════════
📊 Current Conditions:
   • Solar Output: {current_power_kw:.1f} kW ({current_power_w} W)
   • Grid Demand: {current_grid_demand_kw:.1f} kW
   • DR Event Status: {'ACTIVE' if dr_event_active else 'INACTIVE'}
   • Forecast Peak: {forecast_peak_kw:.1f} kW (next 2 hours)

🎯 Analysis Results:"""
    
    for rec in recommendations:
        analysis_result += f"\n{rec}"
    
    # Add operational guidelines
    analysis_result += f"""

📋 Operational Guidelines Applied:
   • DR Event: Curtail by ≥30% if output >500W, min 200W
   • Low Demand: Curtail to 1000W if demand <1000kW and solar >1500W
   • Normal Ops: Monitor and maintain grid stability
═══════════════════════════════════════════════════════"""
    
    return analysis_result


def _extract_current_power(status_report: str) -> int:
    """Extract current power output from solar status report."""
    try:
        # Look for pattern like "Power Output: 2500 W"
        match = re.search(r'Power Output:\s*(\d+)\s*W', status_report)
        if match:
            return int(match.group(1))
    except:
        pass
    return 0


def _extract_forecast_powers(forecast_report: str) -> tuple:
    """Extract peak and average power from forecast report."""
    try:
        peak_power_kw = 0
        avg_power_kw = 0
        
        # Look for peak power pattern
        peak_match = re.search(r'Peak Power:\s*(\d+)\s*W', forecast_report)
        if peak_match:
            peak_power_kw = int(peak_match.group(1)) / 1000
        
        # Look for average power pattern
        avg_match = re.search(r'Average Power:\s*(\d+)\s*W', forecast_report)
        if avg_match:
            avg_power_kw = int(avg_match.group(1)) / 1000
            
        return peak_power_kw, avg_power_kw
    except:
        return 0, 0 