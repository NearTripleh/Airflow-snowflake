### adhoc ###
FROM ubuntu:18.04
RUN apt-get update && apt-get upgrade -y
ENV TZ=America/Mexico_City
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}
ENV PYTHONIOENCODING=utf-8
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

#docker.sock
USER root
#ARG DOCKER_GROUP_ID

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update -y \
    && apt-get install --assume-yes --no-install-recommends libjemalloc-dev libboost-dev \
    libboost-filesystem-dev \
    libboost-system-dev \
    libboost-regex-dev \
    gpg-agent \
    python3-setuptools \
    python3-dev \
    build-essential \   
    libssl-dev \
    libffi-dev \
    unixodbc-dev \
    autoconf \
    flex \
    curl \
    git \
    gcc \
    bison \
    software-properties-common \
    python3-pip

RUN useradd -ms /bin/bash -d ${AIRFLOW_USER_HOME} airflow \
    && cd ..


#docker.sock
RUN curl -sSL https://get.docker.com/ | sh
ADD ./wrapdocker /usr/local/bin/wrapdocker
RUN chmod +x /usr/local/bin/wrapdocker

RUN pip3 install --upgrade pip

RUN pip3 install -r https://raw.githubusercontent.com/snowflakedb/snowflake-connector-python/v2.4.6/tested_requirements/requirements_36.reqs

RUN pip3 install \
    pyarrow==2.0.0 \
    psutil \
    hurry.filesize \
    Unidecode \
    pytest-timeit \
    docker \
    simple-salesforce \
    typing_extensions \
    setuptools wheel \
    pytz \
    boto3 \
    pysftp \
    pymongo \
    gspread \
    pyathena \
    pyodbc \
    oauth2client \
    dask[complete] \
    cython \
    lxml \
    psycopg2-binary \
    pyOpenSSL \
    ndg-httpsclient \
    redis==3.2 \
    SQLAlchemy==1.3.19 \
    asyncpg \
    pymysql \
    xlrd==1.2.0 \
    snowflake-connector-python==2.4.6 \
    apache-airflow==1.10.10 


COPY script/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg
     

RUN chown -R airflow: ${AIRFLOW_USER_HOME} \
    && chmod +x entrypoint.sh

EXPOSE 8080 5555 8793


RUN usermod -aG docker airflow


USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]



