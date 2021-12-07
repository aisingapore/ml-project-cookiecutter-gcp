FROM python:3.7-slim

RUN groupadd --gid 1000 scout && \
    useradd --uid 1000 --gid 1000 -ms /bin/bash scout

COPY --chown=scout . /app
WORKDIR /app
RUN pip install -r requirements.txt

USER scout

EXPOSE 5000
EXPOSE 9000

ENV MODEL_NAME SeldonWrapper
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

CMD bash run.sh
