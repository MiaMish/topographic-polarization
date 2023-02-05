#!/bin/bash

REGISTRY="886354586566.dkr.ecr.eu-central-1.amazonaws.com"
IMAGE="${REGISTRY}/mia-another-poc"
IMAGE_TAG="1.0.0.0"

echo "Login to ECR..." && \
aws ecr get-login-password --region eu-central-1 --profile ping-poc | docker login --username AWS --password-stdin "$REGISTRY" && \
echo "Building image..." && \
docker build -t "$IMAGE:$IMAGE_TAG" ../ && \
echo "Pushing image to ECR : $IMAGE:$IMAGE_TAG..." && \
docker push "$IMAGE:$IMAGE_TAG"
