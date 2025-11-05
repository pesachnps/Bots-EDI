# Use Python 3.13 slim base image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BOTSENV=docker \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Bots EDI
RUN pip install --no-cache-dir bots-ediint

# Create Bots environment structure
RUN mkdir -p /app/bots_env/{config,usersys,botssys} && \
    mkdir -p /app/bots_env/usersys/{grammars,mappings,routescripts,partners,communicationscripts,envelopescripts,charsets} && \
    mkdir -p /app/bots_env/botssys/{infile,outfile,sqlitedb,logs,archive}

# Copy configuration files
COPY config/bots.ini /app/bots_env/config/
COPY config/settings.py /app/bots_env/config/

# Copy installed plugins (if pre-installed)
COPY usersys/ /app/bots_env/usersys/
COPY botssys/ /app/bots_env/botssys/

# Set permissions
RUN chmod +x /app/bots_env/config/bots.ini

# Create startup script
RUN echo '#!/bin/bash\n\
cd /app/bots_env\n\
python -c "import bots.botsinit; bots.botsinit.generalinit(); from bots import webserver; webserver.run(host=\"0.0.0.0\", port=8080)"\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Start Bots
CMD ["/app/start.sh"]