"""
Streamlit UI for CrewAI Solar DER Management System
Interactive demonstration of multi-agent solar asset management
"""
import streamlit as st
import os
import sys
import time
import json
from datetime import datetime
from io import StringIO
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crewai import Crew
from agents.solar_agent_definition import SolarControlAgent
from agents.utility_agent_definition import UtilityGridOrchestratorAgent
from tasks.der_tasks import DER_TASKS
from mocks import sunspec_solar_mock


class StreamlitLogCapture:
    """Capture logs for Streamlit display."""
    
    def __init__(self):
        self.logs = []
        self.current_agent = ""
        self.current_task = ""
    
    def capture_output(self, text):
        """Capture and parse CrewAI output."""
        if "# Agent:" in text:
            # Extract agent name
            agent_line = text.split("# Agent:")[1].split("[00m")[0]
            self.current_agent = agent_line.strip().replace("[1m[95m", "").replace("[1m[92m", "")
        
        if "## Task:" in text:
            # Extract task description  
            task_line = text.split("## Task:")[1].split("[00m")[0]
            self.current_task = task_line.strip().replace("[92m", "")[:100] + "..."
        
        if "## Tool Output:" in text:
            # Extract tool results
            output_line = text.split("## Tool Output:")[1].split("[00m")[0]
            tool_output = output_line.strip().replace("[92m", "")
            self.logs.append({
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "agent": self.current_agent,
                "type": "tool_output",
                "message": tool_output
            })
        
        if "## Final Answer:" in text:
            # Extract final answers
            answer_line = text.split("## Final Answer:")[1].split("[00m")[0]
            final_answer = answer_line.strip().replace("[92m", "")
            self.logs.append({
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "agent": self.current_agent,
                "type": "final_answer",
                "message": final_answer
            })


def setup_page():
    """Configure Streamlit page."""
    st.set_page_config(
        page_title="CrewAI Solar DER Management",
        page_icon="🌞",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🌞 CrewAI Solar DER Management System")
    st.markdown("**Interactive Multi-Agent Solar Asset Management Demonstration**")
    
    # Load environment variables
    load_dotenv()


def display_system_status():
    """Display current system configuration."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🏭 Utility Agent",
            value="Active",
            help="Intelligent Grid Operations Orchestrator"
        )
    
    with col2:
        st.metric(
            label="⚡ Solar Agent", 
            value="Active",
            help="Expert Solar PV Inverter Controller"
        )
    
    with col3:
        st.metric(
            label="☀️ Solar Capacity",
            value="3,000 W",
            help="Maximum solar inverter capacity"
        )


def display_solar_data():
    """Display current solar inverter data."""
    try:
        # Get current measurements from SunSpec Model 701
        model_701_data = sunspec_solar_mock.get_701_data()
        current_power = model_701_data["W"]  # Power in Watts
        current_voltage = model_701_data["VL1N"] * (10 ** model_701_data["V_SF"])  # Scale voltage
        max_capacity = sunspec_solar_mock.get_max_capacity()
        
        # Check for alarms
        alarm_status = model_701_data["Alrm"]
        has_alarm = alarm_status > 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🔋 Power Output",
                value=f"{current_power:,.0f} W",
                delta=f"{(current_power/max_capacity)*100:.1f}% of capacity"
            )
        
        with col2:
            voltage_status = "Alert" if has_alarm else ("Normal" if 230 <= current_voltage <= 250 else "Warning")
            st.metric(
                label="⚡ Voltage",
                value=f"{current_voltage:.1f} V",
                delta=voltage_status
            )
        
        with col3:
            st.metric(
                label="📊 Efficiency",
                value=f"{(current_power/max_capacity)*100:.1f}%",
                help="Current output vs maximum capacity"
            )
        
        with col4:
            status_value = "Alarm" if has_alarm else "Operational"
            st.metric(
                label="🎯 Status",
                value=status_value,
                help="System operational status"
            )
        
        # Display alarm details if present
        if has_alarm:
            if alarm_status == 1024:  # AC Over-Voltage alarm
                st.warning("⚠️ **VOLTAGE ANOMALY DETECTED**: AC Over-Voltage condition (Code: 1024)")
            else:
                st.warning(f"⚠️ **ALARM ACTIVE**: Alarm code {alarm_status}")
        
        # Power output chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = current_power,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Solar Power Output (W)"},
            delta = {'reference': max_capacity},
            gauge = {
                'axis': {'range': [None, max_capacity]},
                'bar': {'color': "red" if has_alarm else "gold"},
                'steps': [
                    {'range': [0, max_capacity*0.3], 'color': "lightgray"},
                    {'range': [max_capacity*0.3, max_capacity*0.7], 'color': "yellow"},
                    {'range': [max_capacity*0.7, max_capacity], 'color': "orange"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_capacity*0.9
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional technical details in an expander
        with st.expander("🔧 Technical Details"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**SunSpec Model 701 (AC Measurements):**")
                st.text(f"Power (W): {current_power}")
                st.text(f"Apparent Power (VA): {model_701_data['VA']}")
                st.text(f"Current (A): {model_701_data['A'] * (10 ** model_701_data['A_SF']):.2f}")
                st.text(f"Frequency (Hz): {model_701_data['Hz'] * (10 ** model_701_data['Hz_SF']):.2f}")
            
            with col2:
                st.markdown("**System State:**")
                st.text(f"Operating State: {model_701_data['St']}")
                st.text(f"Inverter State: {model_701_data['InvSt']}")
                st.text(f"Alarm Bitfield: {model_701_data['Alrm']}")
                if has_alarm:
                    st.text("⚠️ ANOMALY DETECTED")
        
    except Exception as e:
        st.error(f"Error fetching solar data: {str(e)}")
        st.info("💡 Tip: Make sure all dependencies are installed and the mock data is properly initialized.")


def run_scenario(scenario_name, inputs):
    """Execute a selected scenario with real-time updates."""
    st.subheader(f"🚀 Executing: {scenario_name}")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Create log capture
    log_capture = StreamlitLogCapture()
    
    # Execution container
    execution_container = st.container()
    
    try:
        status_text.text("Initializing CrewAI agents...")
        progress_bar.progress(10)
        
        # Create and configure the crew
        crew = Crew(
            agents=[UtilityGridOrchestratorAgent, SolarControlAgent],
            tasks=DER_TASKS,
            verbose=True,
            process="sequential"
        )
        
        status_text.text("Starting multi-agent execution...")
        progress_bar.progress(25)
        
        # Capture stdout for real-time display
        old_stdout = sys.stdout
        captured_output = StringIO()
        
        # Execute with output capture
        class TeeOutput:
            def __init__(self, file1, file2):
                self.file1 = file1
                self.file2 = file2
                
            def write(self, text):
                self.file1.write(text)
                self.file2.write(text)
                log_capture.capture_output(text)
                
            def flush(self):
                self.file1.flush()
                self.file2.flush()
        
        sys.stdout = TeeOutput(old_stdout, captured_output)
        
        progress_bar.progress(40)
        status_text.text("Agents are analyzing conditions...")
        
        # Execute the crew
        result = crew.kickoff(inputs=inputs)
        
        progress_bar.progress(100)
        status_text.text("✅ Execution completed successfully!")
        
        # Restore stdout
        sys.stdout = old_stdout
        
        return result, log_capture.logs, captured_output.getvalue()
        
    except Exception as e:
        sys.stdout = old_stdout
        st.error(f"Execution failed: {str(e)}")
        return None, [], ""


def display_agent_interactions(logs):
    """Display agent interactions in real-time."""
    st.subheader("🤖 Agent Interactions")
    
    if not logs:
        st.info("No agent interactions captured yet. Run a scenario to see live agent communications.")
        return
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["💬 Conversation", "📊 Activity Timeline"])
    
    with tab1:
        for log in logs[-10:]:  # Show last 10 interactions
            agent_emoji = "🏭" if "Utility" in log["agent"] else "⚡"
            
            with st.chat_message(log["agent"], avatar=agent_emoji):
                st.markdown(f"**{log['timestamp']}** - {log['type'].replace('_', ' ').title()}")
                st.markdown(log["message"][:500] + ("..." if len(log["message"]) > 500 else ""))
    
    with tab2:
        if logs:
            # Create timeline visualization
            timeline_data = []
            for i, log in enumerate(logs):
                timeline_data.append({
                    'Time': log['timestamp'],
                    'Agent': log['agent'],
                    'Action': log['type'].replace('_', ' ').title(),
                    'Order': i
                })
            
            if timeline_data:
                fig = px.scatter(
                    timeline_data, 
                    x='Order', 
                    y='Agent',
                    color='Action',
                    title="Agent Activity Timeline",
                    hover_data=['Time']
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)


def main():
    """Main Streamlit application."""
    setup_page()
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ No API key found! Please set GOOGLE_API_KEY or OPENAI_API_KEY in your environment.")
        st.info("Add your API key to a .env file or set it as an environment variable.")
        return
    
    # Sidebar configuration
    with st.sidebar:
        st.header("🎛️ System Configuration")
        
        # Scenario selection
        scenario = st.selectbox(
            "Select Demonstration Scenario:",
            [
                "Normal Operations",
                "Demand Response Event", 
                "Voltage Anomaly Detection"
            ]
        )
        
        st.markdown("---")
        
        # Scenario parameters
        if scenario == "Normal Operations":
            st.markdown("**📊 Normal Operations**")
            grid_demand = st.slider("Grid Demand (kW)", 800, 1500, 1200)
            dr_event = False
            st.success("Normal grid conditions")
            
        elif scenario == "Demand Response Event":
            st.markdown("**🔴 Demand Response Event**")
            grid_demand = st.slider("Grid Demand (kW)", 600, 1000, 800)
            dr_event = True
            st.warning("DR event active - curtailment expected")
            
        else:  # Voltage Anomaly
            st.markdown("**⚡ Voltage Anomaly Detection**")
            grid_demand = st.slider("Grid Demand (kW)", 900, 1300, 1100)
            dr_event = False
            st.error("Voltage anomaly simulation enabled")
        
        st.markdown("---")
        
        # System info
        st.markdown("**🔧 System Info**")
        st.text(f"Solar Capacity: 3,000 W")
        st.text(f"SunSpec Models: 701, 704")
        st.text(f"Agents: Utility + Solar")
        
        # Execution button
        execute_button = st.button(
            f"🚀 Execute {scenario}",
            type="primary",
            use_container_width=True
        )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 System Dashboard")
        display_system_status()
        
        st.markdown("---")
        display_solar_data()
        
    with col2:
        st.header("🎯 Scenario Details")
        
        # Scenario information
        if scenario == "Normal Operations":
            st.markdown("""
            **🌞 Normal Operations Scenario**
            - Grid demand: High (1,200 kW)
            - DR event: Inactive
            - Expected: Maximum solar output
            - Policy: Operate at full capacity
            """)
            
        elif scenario == "Demand Response Event":
            st.markdown("""
            **🔴 Demand Response Scenario**
            - Grid demand: Reduced (800 kW)
            - DR event: Active
            - Expected: 30% curtailment
            - Policy: Curtail solar to reduce load
            """)
            
        else:
            st.markdown("""
            **⚡ Voltage Anomaly Scenario**
            - Grid demand: Moderate (1,100 kW)
            - Anomaly: Over-voltage (265V)
            - Expected: Alarm detection
            - Policy: Safety monitoring active
            """)
    
    # Execution section
    if execute_button:
        # Prepare inputs
        inputs = {
            'mock_grid_demand_kw': float(grid_demand),
            'mock_dr_event_active_status': dr_event,
            'max_solar_capacity_watts': 3000
        }
        
        # Enable voltage anomaly simulation if selected
        if scenario == "Voltage Anomaly Detection":
            sunspec_solar_mock.toggle_voltage_anomaly_simulation()
        
        # Execute scenario
        result, logs, raw_output = run_scenario(scenario, inputs)
        
        if result:
            # Display results
            st.success("🎉 Scenario execution completed successfully!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Execution Result")
                st.markdown(f"**Final Decision:** {result}")
                
                # Display key metrics
                if "1878" in str(result):
                    st.metric("🔻 Curtailment Applied", "1,878 W", "-30%")
                elif "3000" in str(result):
                    st.metric("📈 Solar Output", "3,000 W", "Maximum")
            
            with col2:
                st.subheader("⏱️ Execution Summary")
                st.markdown(f"**Scenario:** {scenario}")
                st.markdown(f"**Grid Demand:** {grid_demand} kW")
                st.markdown(f"**DR Event:** {'Active' if dr_event else 'Inactive'}")
                st.markdown(f"**Timestamp:** {datetime.now().strftime('%H:%M:%S')}")
            
            # Agent interactions
            st.markdown("---")
            display_agent_interactions(logs)
            
            # Raw output (expandable)
            with st.expander("🔍 View Raw Agent Output"):
                st.code(raw_output, language="text")
        
        # Reset voltage anomaly if it was enabled
        if scenario == "Voltage Anomaly Detection":
            sunspec_solar_mock.toggle_voltage_anomaly_simulation()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🌞 CrewAI Solar DER Management System | 
            Built with <a href='https://streamlit.io'>Streamlit</a> & 
            <a href='https://crewai.com'>CrewAI</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main() 