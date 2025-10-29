# Use a slim Python image for a smaller footprint
FROM python:3.12-slim

# Python env hygiene
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Create app user & dir
WORKDIR /app
RUN useradd -m -u 10001 appuser

# Copy deps and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/pull-events.py ./pull-events.py
COPY src/pull-traffics.py ./pull-traffics.py
COPY src/library ./library

# Drop privileges
USER appuser

# Default command
CMD ["python", "pull-traffics.py"]
