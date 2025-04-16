# stage 1
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /build

COPY requirements.txt .

RUN  pip install --upgrade pip && pip wheel --wheel-dir=/wheel -r requirements.txt


# stage 2 
FROM python:3.12-slim-bookworm AS runtime


RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY --from=builder /wheel /wheels



COPY requirements.txt .

RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh  


CMD ["./entrypoint.sh"]    
