FROM python:3.9
WORKDIR /usr/local/polarization_mechnisms
COPY requirements.txt requirements.txt
COPY src src
COPY resources resources
#COPY container/entrypoint.sh container/entrypoint.sh
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN chmod +x src/cli.py
#ENTRYPOINT ../entrypoint.sh
WORKDIR src
