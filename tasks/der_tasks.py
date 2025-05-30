"""
DER (Distributed Energy Resource) Task Definitions for CrewAI.
These tasks orchestrate the interaction between Utility and Solar agents.
"""
from crewai import Task
from agents.solar_agent_definition import SolarControlAgent
from agents.utility_agent_definition import UtilityGridOrchestratorAgent


def create_der_tasks():
    """Create and return all DER management tasks."""
    
    # Task 1: Get comprehensive solar status
    task_get_solar_status = Task(
        description="""Instruct the SolarControlAgent to provide a comprehensive status report 
        of the solar inverter. This should include current AC measurements (power, voltage, 
        current, frequency, alarms) and current control settings (power setpoint, enabled status). 
        Compile the received information into a consolidated report.""",
        
        expected_output="""A comprehensive status report string detailing the solar inverter's 
        current AC measurements and control settings, as reported by the SolarControlAgent. 
        Include power output, voltage, current, frequency, any alarms, and control setpoint status.""",
        
        agent=UtilityGridOrchestratorAgent,
        output_file="solar_status_report.txt"  # Optional: save output to file
    )
    
    # Task 2: Get solar power forecast
    task_get_solar_forecast = Task(
        description="""Instruct the SolarControlAgent to generate and provide a power generation 
        forecast for the next 2 hours. The forecast should include hourly breakdown, total expected 
        energy, and summary statistics (average, peak, minimum power).""",
        
        expected_output="""A detailed string containing the solar power generation forecast for 
        the next 2 hours, as reported by the SolarControlAgent. Include hourly power predictions, 
        total kWh expected, and summary statistics.""",
        
        agent=UtilityGridOrchestratorAgent,
        context=[task_get_solar_status],  # Use status as context
        output_file="solar_forecast_report.txt"
    )
    
    # Task 3: Check for voltage anomalies
    task_check_solar_voltage_alerts = Task(
        description="""Instruct the SolarControlAgent to check for and report any voltage 
        anomalies or alarm conditions. This is a critical safety check that should identify 
        any over-voltage, under-voltage, or other electrical anomalies.""",
        
        expected_output="""A string report from the SolarControlAgent indicating if voltage 
        anomalies are present or if conditions are nominal. If anomalies are present, include 
        detailed alarm information and recommended actions.""",
        
        agent=UtilityGridOrchestratorAgent,
        context=[task_get_solar_status]
    )
    
    # Task 4: Analyze grid conditions and decide on curtailment
    task_decide_solar_curtailment = Task(
        description="""Analyze the provided Solar Status Report, Solar Forecast Report, 
        current grid demand of {mock_grid_demand_kw} kW, and DR event status ({mock_dr_event_active_status}). 
        Based on this comprehensive analysis, decide if solar curtailment is necessary and determine 
        the appropriate action.
        
        Grid operational policies:
        - If DR event is active: Aim to curtail solar by at least 30% of current output if current 
          output is above 500W, but not below 200W minimum
        - If no DR event but grid demand is below 1000kW and solar is producing more than 1500W: 
          Curtail to 1000W to prevent overgeneration
        - Otherwise: Maintain normal operation at maximum capacity
        
        Use your analysis tool to evaluate conditions and provide a clear recommendation.""",
        
        expected_output="""A decision string that either states 'No curtailment needed.' or 
        'Recommended curtailment: Set solar output to [target_watts]W and enable the limit.' 
        Include detailed reasoning based on grid conditions, DR event status, and operational policies.""",
        
        agent=UtilityGridOrchestratorAgent,
        context=[task_get_solar_status, task_get_solar_forecast],
        tools=[UtilityGridOrchestratorAgent.tools[0]]  # Use the analysis tool
    )
    
    # Task 5: Execute solar control command
    task_execute_solar_command = Task(
        description="""Based on the curtailment decision from the previous analysis, instruct 
        the SolarControlAgent to implement the appropriate power control settings. 
        
        If curtailment is recommended: Set the solar inverter to the specified target power limit 
        and enable the control.
        
        If no curtailment is needed: Ensure the solar inverter is operating at its normal maximum 
        capacity ({max_solar_capacity_watts}W) with controls enabled for optimal operation.""",
        
        expected_output="""A confirmation string detailing the command sent to the SolarControlAgent 
        and its reported outcome, including the new operational state of the solar inverter with 
        specific power setpoint and enable status.""",
        
        agent=UtilityGridOrchestratorAgent,
        context=[task_get_solar_status, task_decide_solar_curtailment]
    )
    
    return [
        task_get_solar_status,
        task_get_solar_forecast, 
        task_check_solar_voltage_alerts,
        task_decide_solar_curtailment,
        task_execute_solar_command
    ]


# Create task instances
DER_TASKS = create_der_tasks() 