FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-extra \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Use PORT environment variable provided by Hugging Face
ENV PORT=8501
EXPOSE $PORT

# Use the PORT variable in the command
CMD streamlit run appMath.py --server.port=$PORT --server.address=0.0.0.0