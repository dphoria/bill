#!/bin/bash
export INFERENCE_API_TOKEN=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
export FLASK_SECRET_KEY=27bd611b8fe2e2a0733a09aa3e2ece29f470f8f1e8d2c64a56aa9acf2220de22
npx tsc
pushd /home/deux/Workspace/bill/src/ui/
PYTHONPATH="/home/deux/Workspace/bill/src:$PYTHONPATH" /home/deux/miniconda3/envs/bill/bin/python main.py $1
popd