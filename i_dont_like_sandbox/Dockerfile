FROM python:3.9-slim

WORKDIR /app

COPY src/chal.py /app/
COPY service/docker-entrypoint.sh /app/
ENV FLAG="flag{Welcome_to_netdreamCTF_2025!}"

RUN apt update && \
    apt install -y socat && \
    chmod +x docker-entrypoint.sh

EXPOSE 5555
CMD ["/app/docker-entrypoint.sh"]