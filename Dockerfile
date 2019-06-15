FROM python:3.5-stretch

WORKDIR /app/cryptocracy
COPY install.sh requirements.txt setup.py ./
COPY src src/
RUN chmod +x install.sh
RUN ./install.sh
RUN pip install -r requirements.txt && pip install .

WORKDIR /app/cryptocracy/src/delivery/cli
RUN chmod +x ./cryptocracy

ENV CRYPTOCRACY_OBJECT_STORE_BUCKET_NAME="define me"
ENV CRYPTOCRACY_OBJECT_CACHE_BUCKET_NAME="define me"
ENV CRYPTOCRACY_PROXY_KEY_STORE_TABLE_NAME="define me"
ENV AWS_DEFAULT_REGION="ap-southeast-1"
CMD ["./cryptocracy", "--help"]