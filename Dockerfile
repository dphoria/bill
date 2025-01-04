# syntax=docker/dockerfile:1.4
ARG PYTHON_BASE=3.12-slim-bullseye

# build stage
FROM python:$PYTHON_BASE AS builder

# install PDM
RUN pip install -U pdm
# disable update check
ENV PDM_CHECK_UPDATE=false
# copy files
COPY pyproject.toml pdm.lock /bill/
# COPY src/ /bill/src

# install dependencies and project into the local packages directory
WORKDIR /bill
RUN pdm install --check --prod --no-editable

# run app
FROM python:$PYTHON_BASE

# retrieve packages from build stage
COPY --from=builder /bill/.venv/ /bill/.venv/
COPY src/ /bill/src

ENV PATH="/bill/.venv/bin:$PATH"
ENV PYTHONPATH="/bill/src:$PYTHONPATH"

ENTRYPOINT ["python"]
CMD ["/bill/src/ui/main.py"]
