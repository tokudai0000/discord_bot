FROM python
LABEL version="1.0.0"
USER root
WORKDIR /app
COPY ./fastapi /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    python3-setuptools \
    python3-venv \
    python3-wheel \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    mime-support \
    && rm -rf /var/lib/apt/lists/*
EXPOSE 8080
CMD ["/bin/bash"]