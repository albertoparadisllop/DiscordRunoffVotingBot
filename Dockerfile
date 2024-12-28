FROM python:3.9.4

COPY . /opt/bot
WORKDIR /opt/bot
RUN python -m pip install -U discord.py==2.3.2