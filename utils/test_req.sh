#!/bin/bash

set -e

cd $(dirname $0)/..

echo "Sending request to /health..."
docker run -it --rm --network="host" fullstorydev/grpcurl -plaintext localhost:50051 mlservice.v1.PredictionService.Health
echo "Running client.py..."
python3 client/client.py