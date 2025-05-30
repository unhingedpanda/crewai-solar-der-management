"""
Main script for CrewAI Solar DER Management System.
Orchestrates the Utility Agent and Solar Agent to manage simulated solar assets.
"""
import os
import sys
import logging
from datetime import datetime
from io import StringIO
from dotenv import load_dotenv
from crewai import Crew
from agents.solar_agent_definition import SolarControlAgent
from agents.utility_agent_definition import UtilityGridOrchestratorAgent
from tasks.der_tasks import DER_TASKS
from mocks import sunspec_solar_mock


class LogCapture:
    """Custom log capture to save terminal output to files."""
    
    def __init__(self, log_file):
        self.log_file = log_file
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.log_content = StringIO()
        
    def __enter__(self):
        # Create a tee-like behavior to capture and display
        class TeeOutput:
            def __init__(self, original, capture):
                self.original = original
                self.capture = capture
                
            def write(self, text):
                self.original.write(text)
                self.capture.write(text)
                
            def flush(self):
                self.original.flush()
                self.capture.flush()
        
        self.tee_stdout = TeeOutput(self.original_stdout, self.log_content)
        self.tee_stderr = TeeOutput(self.original_stderr, self.log_content)
        
        sys.stdout = self.tee_stdout
        sys.stderr = self.tee_stderr
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        
        # Save captured content to file
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(self.log_content.getvalue())


def setup_environment():
    """Load environment variables and validate configuration."""
    load_dotenv()
    
    # Check for required API key
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("⚠️ WARNING: No API key found in environment variables.")
        print("Please set either GOOGLE_API_KEY or OPENAI_API_KEY")
        print("export GOOGLE_API_KEY='your_api_key_here'")
        print("or create a .env file with: GOOGLE_API_KEY=your_api_key_here")
        return False
    
    print("✅ Environment configured successfully")
    return True


def create_log_directory():
    """Create logs directory if it doesn't exist."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir


def run_normal_operations():
    """Run the normal DER management workflow."""
    print("\n" + "="*80)
    print("🌞 SOLAR DER MANAGEMENT SYSTEM - NORMAL OPERATIONS")
    print("="*80)
    
    # Define operational parameters
    inputs = {
        'mock_grid_demand_kw': 1200.0,  # Normal grid demand
        'mock_dr_event_active_status': False,  # No DR event
        'max_solar_capacity_watts': 3000
    }
    
    # Create and configure the crew
    crew = Crew(
        agents=[UtilityGridOrchestratorAgent, SolarControlAgent],
        tasks=DER_TASKS,
        verbose=True,  # Fixed: Changed from verbose=2 to verbose=True
        process="sequential"  # Tasks executed in sequence
    )
    
    print(f"📊 Operational Parameters:")
    print(f"   • Grid Demand: {inputs['mock_grid_demand_kw']} kW")
    print(f"   • DR Event Active: {inputs['mock_dr_event_active_status']}")
    print(f"   • Solar Capacity: {inputs['max_solar_capacity_watts']} W")
    print("\n🚀 Starting normal operations workflow...\n")
    
    # Capture output to log file
    log_dir = create_log_directory()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/scenario_1_normal_operations_{timestamp}.log"
    
    try:
        with LogCapture(log_file):
            result = crew.kickoff(inputs=inputs)
        
        print("\n" + "="*80)
        print("✅ NORMAL OPERATIONS COMPLETED SUCCESSFULLY")
        print("="*80)
        print(f"📁 Full execution log saved to: {log_file}")
        print(f"Final Result:\n{result}")
        
        # Save summary to separate file
        summary_file = f"{log_dir}/scenario_1_summary_{timestamp}.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"SCENARIO 1: NORMAL OPERATIONS SUMMARY\n")
            f.write(f"{'='*50}\n")
            f.write(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Grid Demand: {inputs['mock_grid_demand_kw']} kW\n")
            f.write(f"DR Event: {inputs['mock_dr_event_active_status']}\n")
            f.write(f"Solar Capacity: {inputs['max_solar_capacity_watts']} W\n")
            f.write(f"Status: SUCCESS\n\n")
            f.write(f"Final Result:\n{result}\n")
        
        return result
    
    except Exception as e:
        print(f"\n❌ Error during normal operations: {str(e)}")
        return None


def run_dr_event_simulation():
    """Run a Demand Response event simulation."""
    print("\n" + "="*80)
    print("🔴 SOLAR DER MANAGEMENT SYSTEM - DR EVENT SIMULATION")
    print("="*80)
    
    # Define DR event parameters
    inputs = {
        'mock_grid_demand_kw': 800.0,   # Lower grid demand during DR event
        'mock_dr_event_active_status': True,  # DR event active
        'max_solar_capacity_watts': 3000
    }
    
    # Create and configure the crew
    crew = Crew(
        agents=[UtilityGridOrchestratorAgent, SolarControlAgent],
        tasks=DER_TASKS,
        verbose=True,
        process="sequential"
    )
    
    print(f"📊 DR Event Parameters:")
    print(f"   • Grid Demand: {inputs['mock_grid_demand_kw']} kW")
    print(f"   • DR Event Active: {inputs['mock_dr_event_active_status']}")
    print(f"   • Solar Capacity: {inputs['max_solar_capacity_watts']} W")
    print("\n🚀 Starting DR event response workflow...\n")
    
    # Capture output to log file
    log_dir = create_log_directory()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/scenario_2_dr_event_{timestamp}.log"
    
    try:
        with LogCapture(log_file):
            result = crew.kickoff(inputs=inputs)
        
        print("\n" + "="*80)
        print("✅ DR EVENT SIMULATION COMPLETED SUCCESSFULLY")
        print("="*80)
        print(f"📁 Full execution log saved to: {log_file}")
        print(f"Final Result:\n{result}")
        
        # Save summary to separate file
        summary_file = f"{log_dir}/scenario_2_summary_{timestamp}.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"SCENARIO 2: DEMAND RESPONSE EVENT SUMMARY\n")
            f.write(f"{'='*50}\n")
            f.write(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Grid Demand: {inputs['mock_grid_demand_kw']} kW\n")
            f.write(f"DR Event: {inputs['mock_dr_event_active_status']}\n")
            f.write(f"Solar Capacity: {inputs['max_solar_capacity_watts']} W\n")
            f.write(f"Status: SUCCESS\n\n")
            f.write(f"Final Result:\n{result}\n")
        
        return result
    
    except Exception as e:
        print(f"\n❌ Error during DR event simulation: {str(e)}")
        return None


def run_voltage_anomaly_simulation():
    """Run a voltage anomaly detection and response simulation."""
    print("\n" + "="*80)
    print("⚡ SOLAR DER MANAGEMENT SYSTEM - VOLTAGE ANOMALY SIMULATION")
    print("="*80)
    
    # Enable voltage anomaly simulation
    print("🔧 Triggering voltage anomaly simulation...")
    anomaly_state = sunspec_solar_mock.toggle_voltage_anomaly_simulation()
    print(f"   Voltage anomaly simulation: {'ENABLED' if anomaly_state else 'DISABLED'}")
    
    # Define operational parameters for anomaly detection
    inputs = {
        'mock_grid_demand_kw': 1100.0,
        'mock_dr_event_active_status': False,
        'max_solar_capacity_watts': 3000
    }
    
    # Create and configure the crew
    crew = Crew(
        agents=[UtilityGridOrchestratorAgent, SolarControlAgent],
        tasks=DER_TASKS,
        verbose=True,
        process="sequential"
    )
    
    print(f"📊 Anomaly Detection Parameters:")
    print(f"   • Grid Demand: {inputs['mock_grid_demand_kw']} kW")
    print(f"   • DR Event Active: {inputs['mock_dr_event_active_status']}")
    print(f"   • Voltage Anomaly: SIMULATED")
    print("\n🚀 Starting voltage anomaly detection workflow...\n")
    
    # Capture output to log file
    log_dir = create_log_directory()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/scenario_3_voltage_anomaly_{timestamp}.log"
    
    try:
        with LogCapture(log_file):
            result = crew.kickoff(inputs=inputs)
        
        print("\n" + "="*80)
        print("✅ VOLTAGE ANOMALY SIMULATION COMPLETED")
        print("="*80)
        print(f"📁 Full execution log saved to: {log_file}")
        print(f"Final Result:\n{result}")
        
        # Reset voltage anomaly simulation
        print("\n🔧 Resetting voltage anomaly simulation...")
        sunspec_solar_mock.toggle_voltage_anomaly_simulation()
        print("   Voltage anomaly simulation: DISABLED")
        
        # Save summary to separate file
        summary_file = f"{log_dir}/scenario_3_summary_{timestamp}.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"SCENARIO 3: VOLTAGE ANOMALY DETECTION SUMMARY\n")
            f.write(f"{'='*50}\n")
            f.write(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Grid Demand: {inputs['mock_grid_demand_kw']} kW\n")
            f.write(f"DR Event: {inputs['mock_dr_event_active_status']}\n")
            f.write(f"Voltage Anomaly: SIMULATED\n")
            f.write(f"Solar Capacity: {inputs['max_solar_capacity_watts']} W\n")
            f.write(f"Status: SUCCESS\n\n")
            f.write(f"Final Result:\n{result}\n")
        
        return result
    
    except Exception as e:
        print(f"\n❌ Error during voltage anomaly simulation: {str(e)}")
        # Ensure anomaly simulation is reset even on error
        sunspec_solar_mock.toggle_voltage_anomaly_simulation()
        return None


def create_master_summary(normal_result, dr_result, anomaly_result):
    """Create a master summary file with all scenario results."""
    log_dir = create_log_directory()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    master_file = f"{log_dir}/master_summary_{timestamp}.txt"
    
    with open(master_file, 'w', encoding='utf-8') as f:
        f.write("CREWAI SOLAR DER MANAGEMENT SYSTEM - MASTER SUMMARY\n")
        f.write("="*60 + "\n")
        f.write(f"Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"System: Solar Agent + Utility Agent Multi-Agent System\n")
        f.write(f"Framework: CrewAI with SunSpec Solar Simulation\n\n")
        
        f.write("SCENARIO RESULTS:\n")
        f.write("-" * 20 + "\n")
        f.write(f"✅ Normal Operations: {'SUCCESS' if normal_result else 'FAILED'}\n")
        f.write(f"✅ DR Event Response: {'SUCCESS' if dr_result else 'FAILED'}\n")
        f.write(f"✅ Anomaly Detection: {'SUCCESS' if anomaly_result else 'FAILED'}\n\n")
        
        if normal_result:
            f.write("NORMAL OPERATIONS OUTCOME:\n")
            f.write(f"{normal_result}\n\n")
            
        if dr_result:
            f.write("DR EVENT RESPONSE OUTCOME:\n")
            f.write(f"{dr_result}\n\n")
            
        if anomaly_result:
            f.write("ANOMALY DETECTION OUTCOME:\n")
            f.write(f"{anomaly_result}\n\n")
        
        f.write("SYSTEM CAPABILITIES DEMONSTRATED:\n")
        f.write("-" * 35 + "\n")
        f.write("• Real-time solar inverter monitoring and control\n")
        f.write("• Power generation forecasting\n")
        f.write("• Demand Response event handling\n")
        f.write("• Voltage anomaly detection and alerting\n")
        f.write("• Automated curtailment decisions\n")
        f.write("• Agent delegation and coordination\n")
        f.write("• SunSpec-compliant data simulation\n")
    
    return master_file


def main():
    """Main execution function."""
    print("🏭 CrewAI Solar DER Management System")
    print("=====================================")
    
    # Setup environment
    if not setup_environment():
        return
    
    # Create logs directory
    log_dir = create_log_directory()
    print(f"📁 Logs will be saved to: {log_dir}/")
    
    # Display system information
    print(f"\n📋 System Configuration:")
    print(f"   • Solar Agent: Expert Solar PV Inverter Controller")
    print(f"   • Utility Agent: Intelligent Grid Operations Orchestrator")
    print(f"   • Solar Capacity: {sunspec_solar_mock.get_max_capacity()} W")
    print(f"   • SunSpec Models: 701 (AC Measurement), 704 (AC Controls)")
    
    try:
        # Scenario 1: Normal Operations
        print("\n" + "🔄 SCENARIO 1: Normal Grid Operations")
        normal_result = run_normal_operations()
        
        # Small delay between scenarios
        import time
        time.sleep(2)
        
        # Scenario 2: DR Event Response
        print("\n" + "🔄 SCENARIO 2: Demand Response Event")
        dr_result = run_dr_event_simulation()
        
        # Small delay between scenarios
        time.sleep(2)
        
        # Scenario 3: Voltage Anomaly Detection
        print("\n" + "🔄 SCENARIO 3: Voltage Anomaly Detection")
        anomaly_result = run_voltage_anomaly_simulation()
        
        # Create master summary
        master_file = create_master_summary(normal_result, dr_result, anomaly_result)
        
        # Summary
        print("\n" + "="*80)
        print("📊 SIMULATION SUMMARY")
        print("="*80)
        print("✅ Normal Operations:", "SUCCESS" if normal_result else "FAILED")
        print("✅ DR Event Response:", "SUCCESS" if dr_result else "FAILED") 
        print("✅ Anomaly Detection:", "SUCCESS" if anomaly_result else "FAILED")
        print(f"\n📁 Master summary saved to: {master_file}")
        print(f"📁 All scenario logs saved to: {log_dir}/")
        print("\n🎯 All scenarios completed. System demonstration finished.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Simulation interrupted by user. Exiting gracefully...")
    except Exception as e:
        print(f"\n\n❌ Unexpected error in main execution: {str(e)}")
    finally:
        # Ensure any simulations are reset
        try:
            sunspec_solar_mock.toggle_voltage_anomaly_simulation()
        except:
            pass


if __name__ == "__main__":
    main() 