# Agent Fabric - Financial Services Platform

A comprehensive multi-agent system built with Google ADK for financial services, replacing LangGraph with Google's Agent Development Kit.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Fabric (Python)                    │
├─────────────────────────────────────────────────────────────┤
│  Orchestrator (Google ADK)                                  │
│  ├── Workflow Manager                                       │
│  ├── State Manager                                          │
│  └── Agent Registry                                         │
├─────────────────────────────────────────────────────────────┤
│  Financial Agents:                                          │
│  ├── Intake Agent      (Application Processing)             │
│  ├── KYC Agent         (Identity Verification)              │
│  ├── Credit Agent      (Credit Assessment)                  │
│  ├── Fraud Agent       (Fraud Detection)                    │
│  └── Collections Agent (Debt Recovery)                      │
├─────────────────────────────────────────────────────────────┤
│  Processing Agents:                                         │
│  ├── OCR Agent         (Document Processing)                │
│  └── Enrichment Agent  (Data Enhancement)                   │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure Services:                                   │
│  ├── Vector DB         (Retrieval & Search)                 │
│  ├── Policy Guardrails (Compliance & Rules)                 │
│  └── HiTL Router       (Human-in-the-Loop)                  │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Key Features

- **Google ADK Integration**: Native Google Agent Development Kit orchestration
- **Financial Services Focus**: Purpose-built for lending and financial workflows
- **Compliance Ready**: Built-in policy guardrails and audit trails
- **Human-in-the-Loop**: Seamless human intervention for complex decisions
- **Scalable Architecture**: Microservices-ready agent design
- **Vector-Powered**: Advanced retrieval and similarity search capabilities

## 📋 Components

### Core Orchestrator
- **Workflow Manager**: Coordinates agent execution sequences
- **State Manager**: Maintains application state across agents
- **Agent Registry**: Dynamic agent discovery and routing

### Financial Agents
- **Intake**: Processes loan applications and initial data collection
- **KYC**: Performs identity verification and compliance checks
- **Credit**: Assesses creditworthiness and risk scoring
- **Fraud**: Detects fraudulent patterns and suspicious activities
- **Collections**: Manages debt recovery and payment processing

### Processing Agents
- **OCR**: Extracts text and data from documents
- **Enrichment**: Enhances data with external sources and validation

### Infrastructure Services
- **Vector DB**: Semantic search and document retrieval
- **Policy Guardrails**: Ensures regulatory compliance
- **HiTL Router**: Routes complex cases to human reviewers

## 🛠️ Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp config/config.example.yaml config/config.yaml
   # Edit config.yaml with your settings
   ```

3. **Run Demo Workflow**
   ```bash
   python examples/demo_runner.py
   ```

4. **Process Sample Loan Application**
   ```bash
   python examples/loan_application_workflow.py
   ```

## 📚 Documentation

- [Architecture Guide](docs/architecture.md)
- [Setup Instructions](docs/setup.md)
- [API Reference](docs/api_reference.md)

## 🔧 Configuration

The system uses YAML configuration files in the `config/` directory:
- `config.yaml`: Main system configuration
- `agents.yaml`: Agent-specific settings
- `policies.yaml`: Compliance and business rules

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific workflow test
python -m pytest tests/test_workflow.py
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📈 Monitoring

The system includes built-in monitoring and logging:
- Agent performance metrics
- Workflow execution traces
- Compliance audit logs
- Error tracking and alerting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

