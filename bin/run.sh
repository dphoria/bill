#!/bin/bash

# Source environment variables from .env file
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Error: .env file not found. Please create one with your environment variables."
    exit 1
fi

npx tsc
pushd src/ui/
PYTHONPATH="../:$PYTHONPATH" python main.py $1
popd