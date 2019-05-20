FROM ubuntu:18.04

ENV APPDIR /opt/project
WORKDIR $APPDIR

RUN apt-get update && \
    apt-get install python3 python3-pip -y && \
    pip3 install cm_client pyyaml

ADD config.yaml $APPDIR

CMD [ "/bin/bash" ]
