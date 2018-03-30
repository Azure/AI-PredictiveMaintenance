#!/bin/bash

# This custom script only works on images where jupyter is pre-installed on the Docker image
#
# This custom script has been tested to work on the following docker images:
#  - aztk/python:spark2.2.0-python3.6.2-base
#  - aztk/python:spark2.2.0-python3.6.2-gpu
#  - aztk/python:spark2.1.0-python3.6.2-base
#  - aztk/python:spark2.1.0-python3.6.2-gpu

if  [ "$IS_MASTER" = "1" ]; then
    pip install jupyter --upgrade
    pip install notebook --upgrade
    pip install azureml
    pip install azureml-model-management-sdk

    PYSPARK_DRIVER_PYTHON="/.pyenv/versions/${USER_PYTHON_VERSION}/bin/jupyter"
    JUPYTER_KERNELS="/.pyenv/versions/${USER_PYTHON_VERSION}/share/jupyter/kernels"

    # disable password/token on jupyter notebook
    jupyter notebook --generate-config --allow-root
    JUPYTER_CONFIG='/.jupyter/jupyter_notebook_config.py'
    echo >> $JUPYTER_CONFIG
    echo -e 'c.NotebookApp.token=""' >> $JUPYTER_CONFIG
    echo -e 'c.NotebookApp.password=""' >> $JUPYTER_CONFIG

    # get master ip
    MASTER_IP=$(hostname -i)

    # remove existing kernels
    rm -rf $JUPYTER_KERNELS/*

    # set up jupyter to use pyspark
    mkdir $JUPYTER_KERNELS/pyspark
    touch $JUPYTER_KERNELS/pyspark/kernel.json
    cat << EOF > $JUPYTER_KERNELS/pyspark/kernel.json
{
    "display_name": "PySpark",
    "language": "python",
    "argv": [
        "python",
        "-m",
        "ipykernel",
        "-f",
        "{connection_file}"
    ],
    "env": {
        "SPARK_HOME": "$SPARK_HOME",
        "PYSPARK_PYTHON": "python",
        "PYSPARK_SUBMIT_ARGS": "--master spark://$MASTER_IP:7077 pyspark-shell"
    }
}
EOF


    cat << EOF > $SPARK_HOME/conf/hive-site.xml
<configuration>
    <property>
        <name>javax.jdo.option.ConnectionURL</name>
        <value>jdbc:postgresql://localhost:5432/hive_metastore</value>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionDriverName</name>
        <value>org.postgresql.Driver</value>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionUserName</name>
        <value>hive</value>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionPassword</name>
        <value>mypassword</value>
    </property>
</configuration>

EOF

 apt-get -y install postgresql postgresql-contrib
    cat << EOF > /etc/postgresql/$(ls /etc/postgresql)/main/pg_hba.conf
local    postgres     postgres     trust

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     md5
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
# Allow replication connections from localhost, by a user with the
# replication privilege.
#local   replication     postgres                                peer
#host    replication     postgres        127.0.0.1/32            md5
#host    replication     postgres        ::1/128                 md5

EOF

    service postgresql restart

    psql -U 'postgres' -c "CREATE USER hive;ALTER ROLE hive WITH PASSWORD 'mypassword';"
    psql -U 'postgres' -c "CREATE DATABASE hive_metastore;"
    psql -U 'postgres' -c "GRANT ALL PRIVILEGES ON DATABASE hive_metastore TO hive";

    # start jupyter notebook from /mnt - this is where we recommend you put your azure files mount point as well
    cd /mnt/notebooks
    (PYSPARK_DRIVER_PYTHON=$PYSPARK_DRIVER_PYTHON PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --port=8888 --allow-root" pyspark &)
fi
