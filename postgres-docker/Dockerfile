FROM postgis/postgis

ENV PG_MAJOR 12
ENV TZ America/Chicago

# add addressing dictionary
RUN mkdir -p /opt/apps
COPY ./pgsql-addressing-dictionary.zip /opt/apps/pgsql-addressing-dictionary.zip

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  postgresql-$PG_MAJOR-pgrouting \
  postgresql-$PG_MAJOR-pgrouting-scripts \
  postgresql-server-dev-$PG_MAJOR \
  unzip \
  make \
  && cd /opt/apps \
  && unzip pgsql-addressing-dictionary.zip \
  && cd pgsql-addressing-dictionary \
  && make install \
  && apt-get purge -y --auto-remove postgresql-server-dev-$PG_MAJOR make unzip

# set time zone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# add backup job
RUN mkdir -p /opt/backups
COPY ./pgbackup.sh /opt/pgbackup.sh
RUN chmod +x /opt/pgbackup.sh

# add init script
RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initdb-postgis.sh /docker-entrypoint-initdb.d/postgis.sh

# create volume for backups
VOLUME ["/opt/backups"]
