# Case Closed - Tron Agent Dockerfile
# Base image includes CPU-only PyTorch
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY agent.py .
COPY *.py ./

# Set Python path
ENV PYTHONPATH=/app

# Run agent (game engine will call agent.py)
CMD ["python", "-c", "import agent; print('Agent loaded successfully')"]

