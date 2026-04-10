FROM python:3.13-slim

WORKDIR /workshop

# System deps for jupyter and native packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ curl && \
    rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency resolution
RUN pip install --no-cache-dir uv

# Install Python dependencies (cached layer - only rebuilds if requirements.txt changes)
COPY requirements.txt .
RUN uv pip install --system --prerelease=allow -r requirements.txt && \
    uv pip install --system jupyterlab

# Copy workshop content
COPY . .

# Install workshop package so custom NAT functions are registered via entry points
RUN pip install --no-cache-dir -e .

# Remove any local env files
RUN rm -f .env

# Jupyter on 8888
EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser", "--ServerApp.token=''"]
