#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Ensure K3s is running and kubectl is configured
echo "--- Ensuring K3s is running and kubectl is configured ---"
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# Build Docker image
echo "--- Building Docker image ---"
docker build -t smarthotel-app:latest .

# Load Docker image into K3s's containerd
echo "--- Loading Docker image into K3s ---"
echo '1' | sudo -S k3s ctr images import -

# Deploy to Kubernetes
echo "--- Deploying to Kubernetes ---"
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl wait --for=condition=ready pod -l app=smarthotel --timeout=120s

# Get the application URL
echo "--- Getting Application URL ---"
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
NODE_PORT=$(kubectl get service smarthotel-service -o jsonpath='{.spec.ports[0].nodePort}')
export APP_URL="http://$NODE_IP:$NODE_PORT"
echo "Application URL: $APP_URL"

# Run tests
echo "--- Running Selenium tests ---"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/test_app.py --junitxml=./TEST-RESULTS.xml

# The post-build steps will be handled by Jenkinsfile