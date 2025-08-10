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

## Development

### Code Quality Checks

The project uses several tools to maintain code quality. These checks are automatically run on pull requests via GitHub Actions.

#### Local Development

Install development dependencies:
```shell
pdm install --group dev
pdm install --group security
```

Run code quality checks:
```shell
# Linting and formatting
pdm run ruff check
pdm run black --check .

# Testing
INFERENCE_API_TOKEN=dummy_token pdm run pytest

# Security checks
pdm run bandit -r src/
pdm run safety check
```

#### GitHub Actions

The following workflows are configured:

- **CI** (`ci.yml`): Runs tests, linting, and security checks
- **Pull Request Checks** (`pull-request.yml`): Basic quality checks for PRs
- **Security** (`security.yml`): Security scanning and dependency checks

All workflows use PDM for dependency management and run on Python 3.12.
