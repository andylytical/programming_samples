FROM python:3

ARG TIMEZONE
ENV TIMEZONE=${TIMEZONE}

RUN ln -snf /usr/share/zoneinfo/$TIMEZONE /etc/localtime \
    && echo $TIMEZONE > /etc/timezone \
    && apt update \
    && apt install -y sqlite3 vim dos2unix bsdmainutils

COPY . /srv
WORKDIR /srv

CMD ["bash"]
