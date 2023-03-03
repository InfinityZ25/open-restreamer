#!/bin/bash
set -e
# Build the container
docker build -t jcedeno/open-restreamer:latest .
# Push the container
docker push jcedeno/open-restreamer:latest