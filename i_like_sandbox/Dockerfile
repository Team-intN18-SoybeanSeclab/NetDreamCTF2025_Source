FROM python:3.9-slim

WORKDIR /app

COPY src/chal.py /app/
COPY service/docker-entrypoint.sh /app/
RUN apt update && \
    apt install -y socat && \
    echo "flag{I_dont-L1k3_Pyd0c}" > /flag && \
    chmod 644 /flag && \
    chmod +x docker-entrypoint.sh

EXPOSE 4444
CMD ["/app/docker-entrypoint.sh"]