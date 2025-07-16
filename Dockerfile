# syntax=docker/dockerfile:1.4
ARG PYTHON_BASE=3.12-slim-bullseye

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
RUN rm /bill/src/ui/test_items.json*

ENV PATH="/bill/.venv/bin:$PATH"
ENV PYTHONPATH="/bill/src:$PYTHONPATH"

ENTRYPOINT ["python"]
CMD ["/bill/src/ui/main.py"]
