FROM python:3.13-slim

WORKDIR /workshop

# curl for healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install uv for fast dependency resolution
RUN pip install --no-cache-dir uv

# Create venv (isolates workshop deps from system Python)
RUN python -m venv /workshop/.venv
ENV PATH="/workshop/.venv/bin:$PATH"

# Install Python dependencies (cached layer - only rebuilds if requirements.txt changes)
COPY requirements.txt .
RUN uv pip install --prerelease=allow -r requirements.txt && \
    uv pip install jupyterlab

# Copy workshop content
COPY . .

# Register custom NAT functions via entry points (non-editable install)
RUN pip install --no-cache-dir .

# Jupyter on 8888 (token disabled for workshop convenience)
EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser", "--ServerApp.token=''"]
