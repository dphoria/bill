`bill` provides a web site to split restaurant bills.
It was developed as a personal learning project.

- [Python 3.12](./pyproject.toml)
- [Node.js v22.13.1](./package.json)

## Install

Adjust accordingly.

```shell
pdm sync
nvm use # nvm use 22.13
npm install
```

## Setup

### Environment Variables

- INFERENCE_API_TOKEN = OpenAI API secret key
- FLASK_SECRET_KEY = Used as Flask secret_key

### [Large Language Model](https://platform.openai.com/docs/models)

[o4-mini](./src/bill/receipts.py#L10) = Used for reading bill images

## Run

```shell
npm run build:css
npx tsc
cd src/ui/
PYTHONPATH="../:$PYTHONPATH" python main.py
```
