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
```

Run code quality checks:
```shell
# Linting and formatting
pdm run ruff check
pdm run black --check .

# Testing
INFERENCE_API_TOKEN=dummy_token pdm run pytest
```

#### GitHub Actions

The project uses a streamlined CI/CD workflow (`ci.yml`) with two main jobs:

- **Quick Checks**: Fast linting and formatting checks for pull requests
- **Testing**: Comprehensive test suite with coverage reporting

The workflow uses conditional job execution to optimize performance:
- Pull requests get quick feedback with essential checks (Ruff + Black)
- Manual triggers run the full test suite with coverage reporting
- All jobs use PDM for dependency management and run on Python 3.12
