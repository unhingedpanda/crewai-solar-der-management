# CrewAI Solar DER Management System

A sophisticated multi-agent system built with CrewAI for managing solar Distributed Energy Resources (DER). This system demonstrates intelligent coordination between utility grid operations and solar inverter control using SunSpec-compliant simulation.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CrewAI Multi-Agent System                    │
├─────────────────────────────────────────────────────────────────┤
│  🏭 Utility Grid Orchestrator Agent                           │
│  ├── Grid demand analysis                                       │
│  ├── Demand response event coordination                         │
│  ├── Solar curtailment decision making                          │
│  └── Agent workflow orchestration                               │
│                                                                 │
│  ⚡ Expert Solar PV Inverter Controller Agent                  │
│  ├── SunSpec Model 701 (AC Measurements)                       │
│  ├── SunSpec Model 704 (AC Controls)                           │
│  ├── Real-time monitoring and control                           │
│  ├── Voltage anomaly detection                                  │
│  └── Power generation forecasting                               │
└─────────────────────────────────────────────────────────────────┘
```

## ✨ Key Features

- **🤖 Multi-Agent Coordination**: Utility and Solar agents working in harmony
- **📊 SunSpec Compliance**: Industry-standard solar inverter communication protocols
- **⚡ Real-time Control**: Dynamic power curtailment and optimization
- **🔍 Anomaly Detection**: Voltage monitoring and alarm handling
- **📈 Predictive Analytics**: 2-hour power generation forecasting
- **📋 Policy Enforcement**: Automated demand response and grid stability rules
- **📁 Comprehensive Logging**: Detailed execution logs for all scenarios

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (preferably 3.11)
- API key from either Google (Gemini) or OpenAI

### API Key Setup

#### Option 1: Google Gemini API (Recommended)
1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Set environment variable:
```bash
export GOOGLE_API_KEY="your_google_api_key_here"
```

#### Option 2: OpenAI API
1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Set environment variable:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

#### Option 3: Using .env file
Create a `.env` file in the project root:
```env
# Choose one of the following:
GOOGLE_API_KEY=your_google_api_key_here
# OR
OPENAI_API_KEY=your_openai_api_key_here
```

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/crewai-solar-der-management.git
cd crewai-solar-der-management

# Create virtual environment (using uv - recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Run the system
python main.py
```

## 🎯 Demonstration Scenarios

The system demonstrates three operational scenarios:

### 1. **Normal Operations** 🌞
- **Grid Demand**: 1,200 kW
- **DR Event**: Inactive
- **Expected Result**: Solar operates at maximum capacity (3,000W)

### 2. **Demand Response Event** 🔴
- **Grid Demand**: 800 kW  
- **DR Event**: Active
- **Expected Result**: Solar curtailed by 30% (2,683W → 1,878W)

### 3. **Voltage Anomaly Detection** ⚡
- **Grid Demand**: 1,100 kW
- **Anomaly**: Simulated over-voltage (265.0V)
- **Expected Result**: Voltage alarm detection and reporting

## 📊 Operational Policies

### Demand Response (DR) Policy
- **Trigger**: Active DR event + solar output >500W
- **Action**: Curtail by ≥30% of current output
- **Minimum**: Maintain at least 200W output
- **Example**: 2,683W → 1,878W (30% reduction)

### Grid Stability Policy  
- **Trigger**: Grid demand <1,000kW + solar >1,500W
- **Action**: Curtail solar to 1,000W to prevent overgeneration
- **Default**: Operate at maximum capacity (3,000W)

### Safety Policy
- **Monitoring**: Continuous voltage anomaly detection
- **Alarms**: SunSpec-compliant alarm codes (e.g., Code 1024 for over-voltage)
- **Range**: Normal voltage 230-250V, alarm at 265.0V

## 🛠️ Tools & Capabilities

### Solar Agent Tools (5 tools)
1. **`read_current_ac_measurements`** - SunSpec Model 701 data
2. **`read_current_control_settings`** - SunSpec Model 704 data
3. **`set_active_power_output_limit`** - Power control commands
4. **`get_power_generation_forecast`** - 2-hour predictions
5. **`check_for_voltage_anomalies_and_report`** - Safety monitoring

### Utility Agent Tools (1 tool)
1. **`analyze_solar_and_grid_conditions`** - Grid analysis and decision engine

## 📁 Project Structure

```
crewai_der_management/
├── main.py                    # Main orchestration script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .gitignore                # Git ignore rules
├── agents/                    # Agent definitions
│   ├── solar_agent_definition.py
│   └── utility_agent_definition.py
├── tools/                     # Tool implementations
│   ├── solar_tools.py
│   └── utility_tools.py
├── tasks/                     # CrewAI task definitions
│   └── der_tasks.py
├── mocks/                     # SunSpec simulation
│   └── sunspec_solar_mock.py
└── logs/                      # Execution logs (example outputs)
    ├── scenario_1_normal_operations_*.log
    ├── scenario_2_dr_event_*.log
    ├── scenario_3_voltage_anomaly_*.log
    ├── scenario_*_summary_*.txt
    └── master_summary_*.txt
```

## 📝 Example Logs

The `logs/` directory contains real execution examples:
- **Full execution logs**: Detailed agent interactions and tool usage
- **Summary files**: Condensed scenario outcomes  
- **Master summary**: Overview of all three scenarios

**Note**: Including logs in the repository allows you to see example system behavior without running it yourself, which is helpful for understanding the multi-agent interactions.

## 🔧 SunSpec Models Used

- **Model 701 (AC Measurement)**: Power, voltage, current, frequency, alarms
- **Model 704 (AC Controls)**: Power setpoint, enable status, capacity limits

## 🚨 What Happens If You Include Logs?

### ✅ Pros of Including Logs:
- **Educational Value**: Others can see exactly how the system behaves
- **Debugging**: Example outputs help understand agent interactions
- **Demonstration**: Shows successful multi-agent coordination
- **Reference**: Real execution examples for learning

### ⚠️ Cons of Including Logs:
- **Repository Size**: Log files can be large (50-60KB each)
- **Frequent Changes**: Logs change with every execution
- **Potential Sensitivity**: Might contain system information
- **Git Noise**: Many small commits when logs update

### 💡 Recommendation:
For this **demonstration/educational repository**, including example logs is beneficial as they showcase the system's capabilities. For production systems, logs should typically be excluded from version control.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent framework
- **SunSpec Alliance**: Solar inverter communication standards
- **Google Gemini/OpenAI**: LLM capabilities for intelligent agents 