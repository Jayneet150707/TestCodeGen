# Agent Fabric Setup Guide

This guide will help you set up and deploy the Agent Fabric system using Google ADK for financial services.

## Prerequisites

### System Requirements
- **Python**: 3.11 or higher
- **Docker**: 20.10 or higher
- **Docker Compose**: 2.0 or higher
- **Git**: Latest version
- **Google Cloud SDK**: Latest version

### Google Cloud Setup
1. **Google Cloud Project**
   ```bash
   # Create a new project
   gcloud projects create your-agent-fabric-project
   gcloud config set project your-agent-fabric-project
   ```

2. **Enable Required APIs**
   ```bash
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable pubsub.googleapis.com
   gcloud services enable firestore.googleapis.com
   gcloud services enable storage.googleapis.com
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable run.googleapis.com
   ```

3. **Create Service Account**
   ```bash
   gcloud iam service-accounts create agent-fabric-sa \
     --display-name="Agent Fabric Service Account"
   
   # Grant necessary permissions
   gcloud projects add-iam-policy-binding your-agent-fabric-project \
     --member="serviceAccount:agent-fabric-sa@your-agent-fabric-project.iam.gserviceaccount.com" \
     --role="roles/aiplatform.user"
   
   gcloud projects add-iam-policy-binding your-agent-fabric-project \
     --member="serviceAccount:agent-fabric-sa@your-agent-fabric-project.iam.gserviceaccount.com" \
     --role="roles/pubsub.admin"
   
   gcloud projects add-iam-policy-binding your-agent-fabric-project \
     --member="serviceAccount:agent-fabric-sa@your-agent-fabric-project.iam.gserviceaccount.com" \
     --role="roles/datastore.user"
   
   # Download service account key
   gcloud iam service-accounts keys create ./service-account-key.json \
     --iam-account=agent-fabric-sa@your-agent-fabric-project.iam.gserviceaccount.com
   ```

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/agent-fabric.git
cd agent-fabric
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy configuration template
cp config/config.yaml.example config/config.yaml

# Edit configuration file
nano config/config.yaml
```

Update the configuration with your Google Cloud settings:
```yaml
google_adk:
  project_id: "your-agent-fabric-project"
  region: "us-central1"
  credentials_path: "./service-account-key.json"

database:
  url: "postgresql://user:password@localhost:5432/agent_fabric"

redis:
  host: "localhost"
  port: 6379
```

### 4. Set Up Infrastructure Services

#### ChromaDB (Vector Database)
```bash
# Using Docker
docker run -d --name chromadb -p 8000:8000 chromadb/chroma:latest

# Or install locally
pip install chromadb
```

#### Redis (Caching)
```bash
# Using Docker
docker run -d --name redis -p 6379:6379 redis:alpine

# Or install locally (Ubuntu/Debian)
sudo apt-get install redis-server
```

#### PostgreSQL (Optional - for relational data)
```bash
# Using Docker
docker run -d --name postgres \
  -e POSTGRES_DB=agent_fabric \
  -e POSTGRES_USER=agent_user \
  -e POSTGRES_PASSWORD=secure_password \
  -p 5432:5432 postgres:15
```

## Google Cloud Infrastructure Setup

### 1. Create Firestore Database
```bash
# Create Firestore database in Native mode
gcloud firestore databases create --region=us-central1
```

### 2. Create Pub/Sub Topics and Subscriptions
```bash
# Create topics for each agent
agents=("intake" "kyc" "credit" "fraud" "collections" "ocr" "enrichment")

for agent in "${agents[@]}"; do
  # Create topic
  gcloud pubsub topics create "agent-${agent}"
  
  # Create subscription
  gcloud pubsub subscriptions create "agent-${agent}-sub" \
    --topic="agent-${agent}"
done

# Create orchestrator topic
gcloud pubsub topics create "orchestrator"
gcloud pubsub subscriptions create "orchestrator-sub" --topic="orchestrator"
```

### 3. Create Cloud Storage Buckets
```bash
# Create bucket for document storage
gsutil mb gs://your-agent-fabric-documents

# Create bucket for model artifacts
gsutil mb gs://your-agent-fabric-models

# Set appropriate permissions
gsutil iam ch serviceAccount:agent-fabric-sa@your-agent-fabric-project.iam.gserviceaccount.com:objectAdmin gs://your-agent-fabric-documents
gsutil iam ch serviceAccount:agent-fabric-sa@your-agent-fabric-project.iam.gserviceaccount.com:objectAdmin gs://your-agent-fabric-models
```

## Database Setup

### 1. Initialize Firestore Collections
```bash
# Run the database initialization script
python scripts/init_firestore.py
```

### 2. Set Up PostgreSQL (if using)
```bash
# Create database schema
python scripts/init_postgres.py

# Run migrations
alembic upgrade head
```

## Agent Deployment

### 1. Local Development Setup
```bash
# Start all infrastructure services
docker-compose up -d

# Initialize the system
python scripts/init_system.py

# Start the orchestrator
python orchestrator/main_orchestrator.py &

# Start individual agents
python -m agents.intake_agent &
python -m agents.kyc_agent &
python -m agents.credit_agent &
python -m agents.fraud_agent &
python -m agents.collections_agent &
python -m agents.ocr_agent &
python -m agents.enrichment_agent &
```

### 2. Production Deployment with Docker

#### Build Images
```bash
# Build all agent images
docker-compose build

# Or build individual images
docker build -t agent-fabric/orchestrator -f docker/Dockerfile.orchestrator .
docker build -t agent-fabric/intake-agent -f docker/Dockerfile.intake .
# ... repeat for other agents
```

#### Deploy with Docker Compose
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Kubernetes Deployment

#### Create Namespace
```bash
kubectl create namespace agent-fabric
```

#### Deploy Configuration
```bash
# Create ConfigMap
kubectl create configmap agent-fabric-config \
  --from-file=config/config.yaml \
  -n agent-fabric

# Create Secret for service account
kubectl create secret generic gcp-credentials \
  --from-file=service-account-key.json \
  -n agent-fabric
```

#### Deploy Services
```bash
# Deploy all services
kubectl apply -f k8s/ -n agent-fabric

# Check deployment status
kubectl get pods -n agent-fabric
```

## Configuration

### 1. Agent Configuration
Edit `config/agents.yaml`:
```yaml
agents:
  intake:
    instances: 2
    resources:
      cpu: "500m"
      memory: "1Gi"
    
  kyc:
    instances: 1
    resources:
      cpu: "1000m"
      memory: "2Gi"
    verification_levels:
      basic: 0.6
      enhanced: 0.8
      premium: 0.95
```

### 2. Policy Configuration
Edit `config/policies.yaml`:
```yaml
compliance:
  kyc:
    required_documents: 2
    verification_threshold: 0.8
    sanctions_screening: true
  
  credit:
    minimum_score: 600
    maximum_dti_ratio: 0.43
    income_verification: true
  
  fraud:
    risk_threshold: 0.7
    velocity_checks: true
    device_fingerprinting: true
```

### 3. External Service Configuration
```yaml
external_services:
  credit_bureau:
    provider: "experian"
    api_key: "${CREDIT_BUREAU_API_KEY}"
    endpoint: "https://api.experian.com"
  
  identity_verification:
    provider: "jumio"
    api_key: "${IDENTITY_API_KEY}"
    endpoint: "https://api.jumio.com"
```

## Testing

### 1. Unit Tests
```bash
# Run all unit tests
python -m pytest tests/unit/

# Run specific agent tests
python -m pytest tests/unit/test_intake_agent.py -v
```

### 2. Integration Tests
```bash
# Start test infrastructure
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
python -m pytest tests/integration/ -v

# Clean up
docker-compose -f docker-compose.test.yml down
```

### 3. End-to-End Tests
```bash
# Run complete workflow tests
python -m pytest tests/e2e/test_loan_workflow.py -v
```

### 4. Load Testing
```bash
# Install load testing tools
pip install locust

# Run load tests
locust -f tests/load/test_intake_load.py --host=http://localhost:8000
```

## Monitoring Setup

### 1. Prometheus & Grafana
```bash
# Deploy monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Access Grafana at http://localhost:3000
# Default credentials: admin/admin
```

### 2. Google Cloud Monitoring
```bash
# Enable monitoring API
gcloud services enable monitoring.googleapis.com

# Create custom metrics
python scripts/setup_monitoring.py
```

### 3. Logging Configuration
```bash
# Configure structured logging
export LOG_LEVEL=INFO
export LOG_FORMAT=json

# Set up log aggregation
gcloud logging sinks create agent-fabric-sink \
  bigquery.googleapis.com/projects/your-project/datasets/agent_fabric_logs
```

## Security Setup

### 1. Network Security
```bash
# Create VPC network
gcloud compute networks create agent-fabric-vpc --subnet-mode=custom

# Create subnet
gcloud compute networks subnets create agent-fabric-subnet \
  --network=agent-fabric-vpc \
  --range=10.0.0.0/24 \
  --region=us-central1
```

### 2. Firewall Rules
```bash
# Allow internal communication
gcloud compute firewall-rules create allow-agent-fabric-internal \
  --network=agent-fabric-vpc \
  --allow=tcp:8000-9000 \
  --source-ranges=10.0.0.0/24

# Allow external API access
gcloud compute firewall-rules create allow-agent-fabric-api \
  --network=agent-fabric-vpc \
  --allow=tcp:80,443 \
  --source-ranges=0.0.0.0/0
```

### 3. Secret Management
```bash
# Store secrets in Google Secret Manager
echo -n "your-api-key" | gcloud secrets create credit-bureau-api-key --data-file=-
echo -n "your-db-password" | gcloud secrets create database-password --data-file=-

# Grant access to service account
gcloud secrets add-iam-policy-binding credit-bureau-api-key \
  --member="serviceAccount:agent-fabric-sa@your-project.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

## Troubleshooting

### Common Issues

#### 1. Agent Registration Failures
```bash
# Check Firestore permissions
gcloud projects get-iam-policy your-project

# Verify service account key
python -c "from google.cloud import firestore; client = firestore.Client(); print('Connection successful')"
```

#### 2. Pub/Sub Message Delivery Issues
```bash
# Check topic and subscription status
gcloud pubsub topics list
gcloud pubsub subscriptions list

# Monitor message flow
gcloud pubsub subscriptions pull agent-intake-sub --limit=5
```

#### 3. Performance Issues
```bash
# Check agent health
curl http://localhost:8000/health

# Monitor resource usage
docker stats

# Check logs
docker logs agent-fabric-intake-1
```

### Debugging Tools

#### 1. Agent Status Dashboard
```bash
# Start monitoring dashboard
python tools/agent_monitor.py
# Access at http://localhost:8080
```

#### 2. Message Tracing
```bash
# Enable message tracing
export TRACE_MESSAGES=true

# View message flow
python tools/message_tracer.py
```

#### 3. Performance Profiling
```bash
# Profile agent performance
python -m cProfile -o profile.stats agents/intake_agent.py
python tools/profile_analyzer.py profile.stats
```

## Maintenance

### 1. Regular Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Update Docker images
docker-compose pull
docker-compose up -d
```

### 2. Database Maintenance
```bash
# Backup Firestore
gcloud firestore export gs://your-backup-bucket/firestore-backup

# Clean up old data
python scripts/cleanup_old_data.py --days=90
```

### 3. Log Rotation
```bash
# Configure log rotation
sudo logrotate -f /etc/logrotate.d/agent-fabric
```

## Support

For additional support:
- **Documentation**: [docs/](docs/)
- **API Reference**: [docs/api_reference.md](docs/api_reference.md)
- **Issues**: Create an issue in the repository
- **Community**: Join our Slack channel

## Next Steps

After successful setup:
1. Run the demo workflow: `python examples/demo_runner.py`
2. Process a sample application: `python examples/loan_application_workflow.py`
3. Explore the monitoring dashboard
4. Review the API documentation
5. Customize agents for your specific use case

