#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Start Minikube
echo "--- Starting Minikube ---"
minikube start --driver=docker

# Set up Docker environment
echo "--- Setting up Docker environment ---"
eval $(minikube -p minikube docker-env)

# Build Docker image
echo "--- Building Docker image ---"
docker build -t smarthotel-app:latest .

# Deploy to Kubernetes
echo "--- Deploying to Kubernetes ---"
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl wait --for=condition=ready pod -l app=smarthotel --timeout=120s

# Get the application URL
export APP_URL=$(minikube service smarthotel-service --url)
echo "Application URL: $APP_URL"

# Run tests
echo "--- Running Selenium tests ---"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/test_app.py --junitxml=./TEST-RESULTS.xml

# The post-build steps will be handled by Jenkinsfile\n
