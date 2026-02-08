#!/bin/bash
# Build and Push Custom Docker Image with Common Module

# Configuration
IMAGE_NAME="kfpmlflow"
IMAGE_TAG="v1.0.0"
REGISTRY="my-registry"  # Replace with your container registry

# Full image name
FULL_IMAGE_NAME="${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"

echo "Building Docker image: ${FULL_IMAGE_NAME}"
echo "==========================================="

# Build the image
docker build -t ${FULL_IMAGE_NAME} .

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Image built successfully!"
    echo ""
    echo "To push the image to your registry, run:"
    echo "  docker push ${FULL_IMAGE_NAME}"
    echo ""
    echo "Then update the TARGET_IMAGE in pipeline_target_image.py to:"
    echo "  TARGET_IMAGE = \"${FULL_IMAGE_NAME}\""
else
    echo ""
    echo "✗ Image build failed!"
    exit 1
fi

# Optional: Push to registry (uncomment to enable)
# echo ""
# echo "Pushing image to registry..."
# docker push ${FULL_IMAGE_NAME}
# if [ $? -eq 0 ]; then
#     echo "✓ Image pushed successfully!"
# else
#     echo "✗ Push failed!"
#     exit 1
# fi
