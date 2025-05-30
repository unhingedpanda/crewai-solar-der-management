"""
Solar Control Agent Definition for CrewAI.
This agent manages a simulated solar PV inverter using SunSpec-like data.
"""
import os
from crewai import Agent
from tools.solar_tools import (
    read_current_ac_measurements,
    read_current_control_settings,
    set_active_power_output_limit,
    get_power_generation_forecast,
    check_for_voltage_anomalies_and_report
)


def create_solar_control_agent():
    """Create and configure the Solar Control Agent."""
    
    solar_agent = Agent(
        role="Expert Solar PV Inverter Controller",
        
        goal="""Accurately monitor, control, and forecast for a solar PV inverter based on 
        direct instructions and internal status, using provided SunSpec-like data tools. 
        Proactively report critical voltage anomalies and execute control commands precisely.""",
        
        backstory="""I am an AI directly managing a simulated solar PV inverter. I use my 
        specialized tools to interact with its SunSpec-compliant controller, execute commands 
        precisely, and provide detailed status reports and forecasts. I continuously monitor 
        for voltage issues and other anomalies that could affect grid stability or equipment 
        safety. My responses are technical, accurate, and focused on operational efficiency.""",
        
        tools=[
            read_current_ac_measurements,
            read_current_control_settings, 
            set_active_power_output_limit,
            get_power_generation_forecast,
            check_for_voltage_anomalies_and_report
        ],
        
        verbose=True,
        allow_delegation=False,  # This agent executes its own tools directly
        
        # Additional behavior configuration
        max_iter=3,  # Limit iterations to prevent infinite loops
        memory=True   # Enable memory for context retention
    )
    
    return solar_agent


# Create the agent instance
SolarControlAgent = create_solar_control_agent() 