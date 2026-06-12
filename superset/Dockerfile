FROM apache/superset:6.0.0

USER root

# Superset 6 images use /app/.venv. Install the Trino SQLAlchemy
# dialect into the same virtual environment used by the Superset process.
RUN if command -v uv >/dev/null 2>&1; then \
      uv pip install --python /app/.venv/bin/python --no-cache trino sqlalchemy-trino; \
    else \
      /app/.venv/bin/python -m ensurepip --upgrade && \
      /app/.venv/bin/python -m pip install --no-cache-dir trino sqlalchemy-trino; \
    fi

USER superset
