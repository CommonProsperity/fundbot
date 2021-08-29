FROM python:3.9.6-alpine

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

RUN python3 -m pip install pipenv

RUN pipenv sync

RUN pipenv run python bot.py