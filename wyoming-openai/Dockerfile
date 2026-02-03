ARG BUILD_FROM
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy Python package files
COPY pyproject.toml README.md LICENSE ./
COPY src ./src

# Install Wyoming OpenAI and dependencies
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir .

# Copy run script
COPY run.sh /
RUN chmod a+x /run.sh

# Run script
CMD [ "/run.sh" ]
