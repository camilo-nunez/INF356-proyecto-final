# Distributed visualisation of oceanographic data using Apache Spark and LustreFS
Repositorio para el proyecto final del ramo INF-356.

# Introducción
El procesamiento y visualización de datos a través del tiempo y a gran escala es un desafio permanente de la era contemporánea, debido al volumen y rapidez con la cual se genera estos. Este desafio se ha puesto a prueba a lo largo de múltiples disciplinas, como el procesamiento de datos astronómicos o el procesamiento de lenguaje natural para la detección de _fakenews_ en redes sociales.

A medida que la tecnología aumenta y mejora, los datos generados por los instrumentos actuales, demandan un mayor uso de las tecnologías existentes. Unas de las principales fuentes de datos, son los sistemas sensoriales oceanográficos, capaces de captar mediciones de su entorno y transmitirlas en tiempo real, demandando una plataforma capaz de recibir estas grandes cantidades de datos y procesarlos en tiempo real para su visualización y posterior análisis.

Frente a esto, el presente trabajo busca contribuir en el pipeline de almacenamiento y procesamientos de estos datos. Particularmente, la contribución de este trabajo es crear una plataforma distribuida para el procesamiento imágenes en datos oceanográficos, usando (1) _LustreFS_ como filesystem distribuido para su almacenamiento, (2) el framework _Apache Spark_ para el procesamiento distribuido, y (3) _Jupyter Notebook_ para la edición de código.

# Paso a Paso
Para realizar el deploy del proyecto, se necesita 1 nodo principal y 2 nodos workers. En este oportunidad, y por cortecia del proyecto _Chilean Virtual Obserevatory_, se ulizaron las siguientes maquinas para las pruebas:
```
inf356-master-01.chi2ad.local
inf356-slave-01.chi2ad.local
inf356-slave-02.chi2ad.local
```
Cada máquina fue virtualizada por medio de Ovirt 4.1, con una configuración de 4 CPU, 8GM de RAM, y 50 GB en disco local. Las máquinas cuentan con una intefaz de _InfiniBand_ virtualizada usando SR-IOV para tener acceso a la _LNet_ de __LustreFS__. El sistema operativo usado fue Debian 10.

Por otro lado, se proporcionó el acceso a un directorio en el _archive_ del _Chilean Virtual Observatory_, el cual cuenta con __LustreFS__ versión 2.10.

A continuacion se detalla el paso a paso necesario para desplegar el proyecto un cluster.

## Instalación de JAVA 11
> Esta instalación se debe repetir en cada uno de los tres nodos.

1. Descargar el binario de instalación de JAVA 11 desde la pagina oficial de Oracle https://www.oracle.com/Java/technologies/javase-jdk11-downloads.html

2. Instalar las librerias básicas para JAVA:
```
apt install libasound2 libasound2-data
```

3. Instalar el binario de JAVA 11 usando el comando `dpkg`:
```
dpkg -i jdk-11.0.8_linux-x64_bin.deb
```

4. Actualizar los PATH de los ejecutablees de JAVA:
```
update-alternatives --install /usr/bin/java java  /usr/lib/jvm/jdk-11.0.8/bin/java 2
update-alternatives --config java
update-alternatives --install /usr/bin/jar jar /usr/lib/jvm/jdk-11.0.8/bin/jar 2
update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/jdk-11.0.8/bin/javac 2
update-alternatives --set jar /usr/lib/jvm/jdk-11.0.8/bin/jar
update-alternatives --set javac /usr/lib/jvm/jdk-11.0.8/bin/javac
```

5. Finalmente, comprobar la versión con el comando `java --version`.

## Instalación de SCALA
> Esta instalación se debe repetir en cada uno de los tres nodos.

1. Solo basta con utlizar el gestor de paquetes `apt` para instalar SCALA:
```
apt install scala
```
2. Finalmente, comprobar la versión con el comando `scala -version`.

##  Creación de las llaves RSA
> Estos pasos solo se deben hacer en el master.
1. Para crear una llave en el master, se debe ejecutar el comando:
```
ssh-keygen -t rsa
```

2. Luego, esta llave se debe copiar en todos los nodos, incluyenddo el mismo master; por medio de los comandos:
```
ssh-copy-id root@inf356-master-01.chi2ad.local
ssh-copy-id root@inf356-slave-01.chi2ad.local
ssh-copy-id root@inf356-slave-02.chi2ad.local
```

## Instalación de Apache Spark
> Esta instalación se debe repetir en cada uno de los tres nodos.

1. Descargar la versión 3 de Spark con Hadoop 3.2:
```
wget https://downloads.apache.org/spark/spark-3.0.0/spark-3.0.0-bin-hadoop3.2.tgz
```

2. Descomprimir los paquetes:
```
tar xvf spark-3.0.0-bin-hadoop3.2.tgz
```
3. Mover los ficheros a las carpetas locales:
```
mkdir /usr/local/spark
mv spark-3.0.0-bin-hadoop3.2/* /usr/local/spark
```

4. Actualizar las variables de entorno y el PATH en el archivo `~/.bashrc`, e incluir esta linea:
```
export PATH=$PATH:/usr/local/spark/bin
```
Luego hay que cargarlo de nuevo con el comando `source ~/.bashrc`

## Configurar el nodo maestro para ejecutar Spark
> Estos pasos solo se deben hacer en el master.

1. Copiar los archivos base:
```
cd /usr/local/spark/conf
cp spark-env.sh.template spark-env.sh
cp slaves.template slaves
```

2. Editar el archivo `spark-env.sh`, e ingresar las variables de entorno:
```
export SPARK_MASTER_HOST='inf356-master-01.chi2ad.local'
export JAVA_HOME='/usr/lib/jvm/jdk-11.0.8/'
```
3. Definir los _workers_ a utilizar en el archivo `slaves`, agregando las siguientes lineas:
```
inf356-master-01.chi2ad.local
inf356-slave-01.chi2ad.local
inf356-slave-02.chi2ad.local
```
## Inicio del cluster Spark
> Estos pasos solo se deben hacer en el master.

1. Para iniciar el cluster, debemos dirigirnos a la carpeta `/usr/local/spark` y ejecutar el archivo:
```
./sbin/start-all.sh
```
2. En caso de querer detener el cluster, se debe ejecuta el archivo:
```
./sbin/stop-all.sh
```

## Visualizar dashboard
Para ver el dashboard de Spark, se debe ingresar a la URL `http://inf356-master-01.chi2ad.local:8080/`.

## Instalar pip3 y Jupyter
> Estos pasos solo se deben hacer en el master.
1. Para instalar `pip3`, solo basta con utlizar el gestor de paquetes `apt`:
```
apt install python3-pip
```

2. Para instalar Jupyter y todas las dependencias utilizadas en este proyecto, se debe usar:
```
pip3 install jupyter netCDF4 py4j xray pandas==0.23.4 numpy seaborn matplotlib
```

## Configurar PySpark
> Estos pasos solo se deben hacer en el master.
1. Agregar las siguientes variables de entorno en el `~/.bashrc`:
```
export SPARK_HOME='/usr/local/spark/'
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="notebook"
export PYSPARK_PYTHON=python3
export PATH=$SPARK_HOME:$PATH:~/.local/bin:$JAVA_HOME/bin:$JAVA_HOME/jre/bin
```
Luego hay que cargarlo de nuevo con el comando `source ~/.bashrc`

## Montar el _Archive_ en Lustre
> Estos pasos solo se deben hacer en el master.
1. Para montar el archivo en el master, se debe crear la carpeta:
```
/archive/
```
2. Luego se debe usar el comando `mount` para el filesystem:
```
mount -t lustre 10.10.XXX.XXX@o2ib:10.10.XXX.XXX@o2ib:/chivodp/inf356_sets /archive/
```
> Por motivos de seguridad, se omitieron digitos en las IPs de los MDS.

## Montar el crawler de datos
> Estos pasos solo se deben hacer en el master.
1. Se debe copiar el archivo `lurker.py` en la carpeta `/archive/data/`.

2. Configurar el cron para el master con el commando `crontab -e `, y agregar la siguiente linea:
```
30 15 * * * /usr/bin/python3 /archive/data/lurker.py > /archive/data/lurker.log
```
