FROM python:3.8-slim

RUN apt-get update && apt-get install -y iputils-ping

WORKDIR mtu_test
COPY mtu_test.py .
ENTRYPOINT ["python3", "mtu_test.py"]
