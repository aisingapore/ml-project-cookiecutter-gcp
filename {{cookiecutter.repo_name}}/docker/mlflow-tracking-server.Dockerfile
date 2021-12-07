FROM debian:buster-slim

ARG NON_ROOT_USER="aisg"

COPY ./conf/mlflow/mlflow-server-requirements.txt ./requirements.txt

RUN set -x \
    && apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
    python3 python3-pip python3-setuptools python3-pandas supervisor gettext-base nginx apache2-utils \
    && pip3 install wheel \
    && pip3 install -r requirements.txt \
    && apt-get remove --purge --auto-remove -y ca-certificates && rm -rf /var/lib/apt/lists/*

RUN addgroup -gid 2222 $NON_ROOT_USER \
    && adduser -uid 2222 -H -D -s /bin/sh -G $NON_ROOT_USER $NON_ROOT_USER

COPY ./conf/mlflow/nginx.conf.template /app/nginx.conf.template
COPY ./conf/mlflow/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./scripts/mlflow/docker-entry-point.sh /app/scripts/docker-entry-point.sh
COPY ./scripts/mlflow/nginx-webserver.sh /app/scripts/nginx-webserver.sh
COPY ./scripts/mlflow/mlflow-tracking-server.sh /app/scripts/mlflow-tracking-server.sh

RUN chmod -R +x /app/scripts

CMD ["/bin/bash", "/app/scripts/docker-entry-point.sh"]

EXPOSE 5005
