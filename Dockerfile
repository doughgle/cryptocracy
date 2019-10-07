FROM python:3.5-slim-buster

WORKDIR /app/cryptocracy
COPY install.sh ./
RUN chmod +x install.sh && \
    ./install.sh

RUN pip install --upgrade cryptocracy

# create user
RUN useradd --create-home cryptocracy
ARG CRYPTOCRACY_USER_HOME="/home/cryptocracy/.cryptocracy"
RUN mkdir -p $CRYPTOCRACY_USER_HOME && \
    chown cryptocracy:cryptocracy $CRYPTOCRACY_USER_HOME && \
    chmod 0700 $CRYPTOCRACY_USER_HOME

WORKDIR /home/cryptocracy
USER cryptocracy

ENV CRYPTOCRACY_OBJECT_STORE_BUCKET_NAME="define me"
ENV CRYPTOCRACY_OBJECT_CACHE_BUCKET_NAME="define me"
ENV CRYPTOCRACY_PROXY_KEY_STORE_TABLE_NAME="define me"
ENV AWS_DEFAULT_REGION="ap-southeast-1"
CMD ["cryptocracy", "--help"]