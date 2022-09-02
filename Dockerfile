FROM python:slim

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN python -m venv venv && \
    /app/venv/bin/pip install ldap3 fastapi uvicorn[standard] python-dotenv

ENTRYPOINT [ "/app/venv/bin/python", "/app/main.py" ]
