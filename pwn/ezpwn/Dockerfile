FROM ubuntu:22.04

RUN apt update && apt install -y socat
RUN useradd -m ctf
WORKDIR /home/ctf
COPY src/attachment /home/ctf/attachment
COPY service/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh /home/ctf/attachment && \
    chown ctf:ctf /home/ctf/attachment


ENTRYPOINT ["/docker-entrypoint.sh"]
