#!/bin/bash

set -e

cd $(dirname $0)/..

docker build -t grpc-ml-service .
echo -e "To run use: 'docker run -p 8080:8080 grpc-ml-service'"