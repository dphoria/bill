#!/bin/bash
pushd ~/Workspace/bill
npx @tailwindcss/cli -i ./src/ui/static/input.css -o ./src/ui/static/output.css --watch
popd
