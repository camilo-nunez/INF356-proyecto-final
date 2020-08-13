# INF356-proyecto-final

inf356-master-01.chi2ad.local
inf356-slave-01.chi2ad.local
inf356-slave-02.chi2ad.local

install java 11(EN TODOS)
--------------------------
https://www.oracle.com/Java/technologies/javase-jdk11-downloads.html

apt install libasound2 libasound2-data

dpkg -i jdk-11.0.8_linux-x64_bin.deb

update-alternatives --install /usr/bin/java java  /usr/lib/jvm/jdk-11.0.8/bin/java 2
update-alternatives --config java
update-alternatives --install /usr/bin/jar jar /usr/lib/jvm/jdk-11.0.8/bin/jar 2
update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/jdk-11.0.8/bin/javac 2
update-alternatives --set jar /usr/lib/jvm/jdk-11.0.8/bin/jar
update-alternatives --set javac /usr/lib/jvm/jdk-11.0.8/bin/javac

 java --version

install scala (EN TODOS)
-------------------------
 apt install scala
 scala -version

 

rsa key (SOLO EN EL MASTER)(GAvMJOg5)
-------------------------
ssh-keygen -t rsa

ssh-copy-id root@inf356-master-01.chi2ad.local
ssh-copy-id root@inf356-slave-01.chi2ad.local
ssh-copy-id root@inf356-slave-02.chi2ad.local

install spark (EN TODOS)
-------------------------
wget https://downloads.apache.org/spark/spark-3.0.0/spark-3.0.0-bin-hadoop3.2.tgz

tar xvf spark-3.0.0-bin-hadoop3.2.tgz

mkdir /usr/local/spark
mv spark-3.0.0-bin-hadoop3.2/* /usr/local/spark

nano ~/.bashrc
export PATH=$PATH:/usr/local/spark/bin
source ~/.bashrc

config spark master (SOLO EN EL MASTER)
---------------------------------------
cd /usr/local/spark/conf
cp spark-env.sh.template spark-env.sh
cp slaves.template slaves

nano spark-env.sh
export SPARK_MASTER_HOST='inf356-master-01.chi2ad.local'
export JAVA_HOME='/usr/lib/jvm/jdk-11.0.8/'

nano slaves
inf356-master-01.chi2ad.local
inf356-slave-01.chi2ad.local
inf356-slave-02.chi2ad.local


start cluster (SOLO EN EL MASTER)
---------------------------------
cd /usr/local/spark
./sbin/start-all.sh

SOLO PARA PARAR ------_> ./sbin/stop-all.sh

ingresar al dashboard
------------------------
http://inf356-master-01.chi2ad.local:8080/




----------------------------------(SOLO MASTER)-----------------------------------

instalar jupyter
----------------
apt install python3-pip
pip3 install jupyter
pip3 install py4j



configuracion final en nano ~/.bashrc
---------------------
nano ~/.bashrc

export SPARK_HOME='/usr/local/spark/'
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="notebook"
export PYSPARK_PYTHON=python3
export PATH=$SPARK_HOME:$PATH:~/.local/bin:$JAVA_HOME/bin:$JAVA_HOME/jre/bin




-------------- MODIFICAR EL CRONTAB ----------------
crontab -e 

30 15 * * * /usr/bin/python3 /archive/data/lurker.py > /archive/data/lurker.log