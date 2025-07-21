# syntax=docker/dockerfile:1.4
ARG PYTHON_BASE=3.12-slim-bullseye
ARG NODE_BASE=22-slim

FROM node:$NODE_BASE AS frontend-builder

WORKDIR /bill
COPY package.json package-lock.json ./
RUN npm ci

COPY tsconfig.json tailwind.config.js ./
COPY src/ui/*.ts ./src/ui/
COPY src/ui/templates/ ./src/ui/templates/
COPY src/ui/static/input.css ./src/ui/static/

RUN npx tsc
RUN npx @tailwindcss/cli -i ./src/ui/static/input.css -o ./src/ui/static/output.css

FROM python:$PYTHON_BASE AS builder

RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false
COPY pyproject.toml pdm.lock /bill/
# COPY src/ /bill/src

WORKDIR /bill
RUN pdm install --check --prod --no-editable

FROM python:$PYTHON_BASE

COPY --from=builder /bill/.venv/ /bill/.venv/
COPY src/ /bill/src
COPY --from=frontend-builder /bill/src/ui/static/ /bill/src/ui/static/
# RUN rm /bill/src/ui/test_items.json*

ENV PATH="/bill/.venv/bin:$PATH"
ENV PYTHONPATH="/bill/src:$PYTHONPATH"

ENTRYPOINT ["python"]
CMD ["/bill/src/ui/main.py"]
