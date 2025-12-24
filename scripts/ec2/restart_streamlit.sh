#!/usr/bin/env bash
set -e

IMAGE_NAME="rag-streamlit"
CONTAINER_NAME="rag-streamlit"
ECR_REPO_URI="214777058381.dkr.ecr.us-east-1.amazonaws.com/rag-streamlit"
AWS_REGION="us-east-1"
ENV_FILE="/home/ubuntu/rag-app.env"

echo "Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION \
  | docker login --username AWS --password-stdin $ECR_REPO_URI

echo "Pulling latest Streamlit image..."
docker pull $ECR_REPO_URI:latest

echo "Stopping old Streamlit container (if exists)..."
docker stop $CONTAINER_NAME || true
docker rm $CONTAINER_NAME || true

echo "Starting Streamlit container..."
docker run -d \
  --name $CONTAINER_NAME \
  --env-file $ENV_FILE \
  -p 8501:8501 \
  --restart unless-stopped \
  $ECR_REPO_URI:latest

echo "Streamlit deployed."
