#!/bin/bash

set -e

cd $(dirname $0)/..
[[ ! -f .venv/bin/activate ]] || source .venv/bin/activate

for module in client server; do
    python -m grpc_tools.protoc -I=protos --python_out=$module --grpc_python_out=$module model.proto
done