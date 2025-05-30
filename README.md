# CrewAI Solar DER Management System

A sophisticated multi-agent system built with CrewAI for managing solar Distributed Energy Resources (DER) using simulated SunSpec data. The system demonstrates intelligent grid operations through the collaboration of a **Solar Agent** and a **Utility Agent**.

## 🏗️ System Architecture

### Agents
- **Solar Control Agent**: Manages a simulated solar PV inverter using SunSpec Models 701 (AC Measurement) and 704 (AC Controls)
- **Utility Grid Orchestrator Agent**: Oversees grid operations and orchestrates the Solar Agent for optimal performance

### Key Features
- ✅ Real-time solar inverter monitoring and control
- ✅ Power generation forecasting
- ✅ Demand Response (DR) event handling
- ✅ Voltage anomaly detection and alerting
- ✅ Automated curtailment decisions based on grid conditions
- ✅ SunSpec-compliant data simulation

## 📁 Project Structure

```
crewai_der_management/
├── main.py                           # Main execution script
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
├── .env                             # Environment variables (create this)
│
├── agents/                          # Agent definitions
│   ├── __init__.py
│   ├── solar_agent_definition.py    # Solar Control Agent
│   └── utility_agent_definition.py  # Utility Grid Orchestrator Agent
│
├── tools/                           # Agent tools
│   ├── __init__.py
│   ├── solar_tools.py              # Solar inverter management tools
│   └── utility_tools.py            # Grid analysis tools
│
├── mocks/                           # Simulation modules
│   ├── __init__.py
│   └── sunspec_solar_mock.py       # SunSpec data simulation
│
└── tasks/                           # CrewAI task definitions
    ├── __init__.py
    └── der_tasks.py                 # DER management workflow tasks
```

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Google API key for Gemini models

### 2. Installation

```bash
# Clone or download the project
cd crewai_der_management

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```bash
# .env file
GOOGLE_API_KEY=your_google_api_key_here
```

To get a Google API key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### 4. Run the System

```bash
python main.py
```

## 📊 System Operations

The system runs three demonstration scenarios:

### Scenario 1: Normal Grid Operations
- Grid demand: 1200 kW
- No DR event active
- Normal solar operations and monitoring

### Scenario 2: Demand Response Event
- Grid demand: 800 kW  
- DR event active
- Automatic solar curtailment (30% reduction, minimum 200W)

### Scenario 3: Voltage Anomaly Detection
- Simulated over-voltage condition
- Automatic anomaly detection and alerting
- Safety protocol activation

## 🔧 SunSpec Data Models

### Model 701 (AC Measurement)
- **W**: Active Power (Watts)
- **VA**: Apparent Power (VA)
- **Hz**: Frequency (scaled)
- **VL1N**: Voltage L1-N (scaled)
- **A**: Current (scaled)
- **Alrm**: Alarm Bitfield
- **St**: Operating State
- **InvSt**: Inverter State

### Model 704 (AC Controls)
- **WSet**: Active Power Setpoint (Watts)
- **WSetEna**: Setpoint Enable flag
- **WSet_SF**: Scale factor

## 🛠️ Agent Tools

### Solar Agent Tools
- `read_current_ac_measurements()`: Get inverter measurements
- `read_current_control_settings()`: Get control configuration
- `set_active_power_output_limit()`: Apply power limits
- `get_power_generation_forecast()`: Generate forecasts
- `check_for_voltage_anomalies_and_report()`: Monitor voltage

### Utility Agent Tools
- `analyze_solar_and_grid_conditions()`: Grid analysis and decision making

## 📋 Operational Policies

### Demand Response Rules
- **Trigger**: DR event active AND solar output > 500W
- **Action**: Curtail by ≥30% of current output
- **Minimum**: Never curtail below 200W

### Grid Stability Rules
- **Trigger**: Grid demand < 1000kW AND solar output > 1500W
- **Action**: Curtail solar to 1000W
- **Reason**: Prevent overgeneration

### Voltage Anomaly Response
- **Detection**: Alarm bit monitoring (AC_OVER_VOLT, AC_UNDER_VOLT)
- **Action**: Immediate alerting and safety recommendations
- **Threshold**: Outside normal 230-250V range

## 🎯 Sample Output

```
🏭 CrewAI Solar DER Management System
=====================================
✅ Environment configured successfully

📋 System Configuration:
   • Solar Agent: Expert Solar PV Inverter Controller
   • Utility Agent: Intelligent Grid Operations Orchestrator
   • Solar Capacity: 3000 W
   • SunSpec Models: 701 (AC Measurement), 704 (AC Controls)

🔄 SCENARIO 1: Normal Grid Operations
================================================================================
🌞 SOLAR DER MANAGEMENT SYSTEM - NORMAL OPERATIONS
================================================================================
📊 Operational Parameters:
   • Grid Demand: 1200.0 kW
   • DR Event Active: False
   • Solar Capacity: 3000 W

🚀 Starting normal operations workflow...
```

## 🔍 Monitoring and Debugging

### Verbose Logging
The system runs with maximum verbosity (`verbose=2`) to show:
- Agent reasoning processes
- Tool execution details
- Task progression
- Decision-making logic

### Output Files
- `solar_status_report.txt`: Latest status report
- `solar_forecast_report.txt`: Latest forecast data

## 🛡️ Safety Features

- **Voltage Monitoring**: Continuous monitoring for electrical anomalies
- **Curtailment Limits**: Hard limits prevent unsafe operation levels
- **Error Handling**: Graceful handling of system errors
- **State Reset**: Automatic cleanup of simulation states

## 🚨 Troubleshooting

### Common Issues

1. **Missing API Key**
   ```
   ⚠️ WARNING: GOOGLE_API_KEY not found in environment variables.
   ```
   **Solution**: Create `.env` file with valid Google API key

2. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'crewai'
   ```
   **Solution**: Activate virtual environment and install requirements

3. **Agent Errors**
   **Solution**: Check verbose logs for detailed error information

### Support
- Check agent backstories and goals for expected behavior
- Review task descriptions for workflow understanding
- Examine tool outputs for data format issues

## 📈 Extensibility

The system is designed for easy extension:

- **Add new SunSpec models**: Extend `sunspec_solar_mock.py`
- **Create additional tools**: Add to respective `tools/` files
- **Implement new scenarios**: Modify `main.py` scenarios
- **Add more agents**: Create new agent definitions
- **Enhanced policies**: Update decision logic in utility tools

## 📄 License

This project is for demonstration and educational purposes.

---

**🎯 Ready to run? Execute `python main.py` and watch the intelligent grid management in action!** 