FROM python:3.9-alpine

RUN apk update && \
    adduser -D ctf && \
    pip install bottle==0.13.2 dill==0.4.0

WORKDIR /app

COPY app/app.py ./app.py
COPY uwsgi.ini ./

RUN chown -R root:ctf /app && \
    chmod 751 /app && \
    chmod 000 app.py && \
    chmod o+x app.py
USER ctf

CMD ["python3", "app.py"]