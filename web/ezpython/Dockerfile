FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn \
    --default-timeout=100 \
    -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

RUN touch /flag && \
    chmod 666 /flag && \
    chown root:root /flag && \
    chown -R root:root /app && \
    find /app -type d -exec chmod 755 {} \; && \
    find /app -type f -exec chmod 644 {} \; && \
    chmod +x /app/start.sh

CMD ["bash", "start.sh"]