"""
Utility Grid Orchestrator Agent Definition for CrewAI.
This agent manages grid operations and orchestrates the Solar Control Agent.
"""
import os
from crewai import Agent
from tools.utility_tools import analyze_solar_and_grid_conditions


def create_utility_grid_orchestrator_agent():
    """Create and configure the Utility Grid Orchestrator Agent."""
    
    utility_agent = Agent(
        role="Intelligent Grid Operations and Solar DER Orchestrator",
        
        goal="""Maintain grid stability and achieve operational objectives by effectively 
        planning, monitoring, and commanding the SolarControlAgent. This includes requesting 
        status and forecasts, issuing curtailment commands based on grid conditions or DR events, 
        and reacting appropriately to alerts from the Solar Agent.""",
        
        backstory="""I am the central AI overseeing a segment of the electrical grid containing 
        a solar PV resource. I communicate with and delegate tasks to the SolarControlAgent to 
        gather critical information and dispatch control actions to ensure optimal grid performance 
        and adherence to programs like Demand Response. I analyze complex grid conditions, balance 
        supply and demand, and make strategic decisions to maintain system reliability while 
        maximizing renewable energy utilization. My approach is methodical, data-driven, and 
        focused on overall system optimization.""",
        
        tools=[
            analyze_solar_and_grid_conditions
        ],
        
        verbose=True,
        allow_delegation=True,  # Crucial - enables delegation to Solar Agent
        
        # Additional behavior configuration
        max_iter=5,   # Allow more iterations for complex orchestration
        memory=True,  # Enable memory for context retention across tasks
        step_callback=None  # Can add custom step callbacks if needed
    )
    
    return utility_agent


# Create the agent instance
UtilityGridOrchestratorAgent = create_utility_grid_orchestrator_agent() 