#Tag: cloudflare-ddns
FROM python:3.12.0rc1-alpine3.17

RUN python3 -m pip install httpx scheduler

COPY dyndns.py /usr/bin/dyndns.py

CMD ["python3", "/usr/bin/dyndns.py"]