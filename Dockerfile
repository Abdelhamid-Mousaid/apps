# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-extra \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Launch application
CMD ["streamlit", "run", "appMath.py", "--server.port=8501", "--server.address=192.168.1.207"]
