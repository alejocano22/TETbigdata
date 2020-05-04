# Laboratorios de BIG DATA
Alejandro Cano Múnera <br/>
Universidad EAFIT 

# DCA
### Conectar
```sh
ssh acanom@192.168.10.116 
```

### Datasets
```sh
hdfs dfs -copyFromLocal bigdata/datasets/* /user/acanom/datasets
```
# EMR
### Scripts
[Scripts EMR](https://github.com/alejocano22/TETbigdata/tree/master/EMR)

# Programas
## Wordcount
### Ejecutables
[Códigos](https://github.com/alejocano22/TETbigdata/tree/master/Programas/Wordcount) <br/>
#### Local
```sh
python wordcount-local.py < input >
python wordcount-mr.py -r local < input > [ -o < output > ]
```

#### EMR
Se deben actualizar las credenciales de aws en el archivo `mrjob.conf`   <br/>
Datos de entrada en s3:
```sh
python wordcount-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/gutenberg-small/*.txt
```
Datos de entrada y de salida en s3:
```sh
python wordcount-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/gutenberg-small/*.txt -o s3://acanomoutputs/wordcount-outputs/
```
## Stocks
(2) Se tiene un conjunto de acciones de la bolsa, en la cual se reporta a diario el valor promedio por acción <br/>
[Estructura de datos](https://github.com/alejocano22/TETbigdata/blob/master/Datasets/dataempresas.csv) <br/>

### Ejecutables

[Códigos](https://github.com/alejocano22/TETbigdata/tree/master/Programas/Stocks)

### 1. Día de menor valor - Día de mayor valor
Por acción, dia-menor-valor, día-mayor-valor  <br/>
#### Local
```sh
python stocks-maxmin-mr.py -r local < input > [ -o < output > ]
```
#### EMR
Se deben actualizar las credenciales de aws en el archivo `mrjob.conf`   <br/>

Datos de entrada en s3: 
```sh
python stocks-maxmin-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/otros/dataempresas2.txt
```
Datos de entrada y de salida en s3: 
```sh
python stocks-maxmin-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/otros/dataempresas2.txt -o s3://acanomoutputs/stocks-maxmin-outputs/
```
#### Output 
```sh
compañía, [[min, fecha_min], [max, fecha_max]]
```
Donde `compañia` es el nombre de la compañia, `min` es el precio mínimo que alcanzo la acción en la fecha `fecha_min` y `max` es el precio máximo que alcanzo la acción en la fecha `fecha_max`. <br/>

### 2. Acciones que siempre han subido o se mantienen estables
Listado de acciones que siempre han subido o se mantienen estables.<br/>
#### Local
```sh
python stocks-risenstable-mr.py -r local < input > [ -o < output > ]
```
#### EMR
Se deben actualizar las credenciales de aws en el archivo `mrjob.conf`    <br/>

Datos de entrada en s3:
```sh
python stocks-risenstable-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/otros/dataempresas2.txt
```
Datos de entrada y de salida en s3:
```sh
python stocks-risenstable-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/otros/dataempresas2.txt -o s3://acanomoutputs/stocks-risenstable-outputs/
```
#### Output
```sh
compañía, mensaje
```
Donde `compañia` es el nombre de la compañia y `mensaje` es "Raise or stable all time." Que indica que el precio de la acción ha subido o se ha mantenido estable en el historico de datos. <br/>

### 3. Día negro
DIA NEGRO: Saque el día en el que la mayor cantidad de acciones tienen el menor valor de acción (DESPLOME), suponga una inflación independiente del tiempo.<br/>
#### Local
```sh
python stocks-blackday-mr.py -r local < input > [ -o < output > ]
```
#### EMR
Se deben actualizar las credenciales de aws en el archivo `mrjob.conf`    <br/>

Datos de entrada en s3:
```sh
python stocks-blackfriday-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/otros/dataempresas2.txt
```
Datos de entrada y de salida en s3:
```sh
python stocks-blackday-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/otros/dataempresas2.txt -o s3://acanomoutputs/stocks-blackday-outputs/
```

#### Output
```sh
[mensaje, conteo], fecha
```
Donde `mensaje` es "Black Friday" y `conteo` es el número de compañias que registrarón la acción más baja en `fecha`. <br/>

# HIVE caso de estudio Retail
Es una tienda de venta de artículos deportivos, que tiene tiendas físicas/presenciales, pero que también tiene sitio de ventas por web. <br/>
Ej: Nike, Adidas, Sportline, Foot Locker, etc. <br/>

### Preguntas de negocio
1. ¿Son los productos más visitados en el sitio web los más vendidos? <br/>
2. ¿Son los productos más visitados los que hacen parte de los de mayor rentabilidad?

### Scripts
[settings-emr](https://github.com/alejocano22/TETbigdata/blob/master/EMR/settings-emr.txt) <br/>
[sql-scripts](https://github.com/alejocano22/TETbigdata/blob/master/rdbms) <br/>

### Base de Datos RDS
```sh
CREATE DATABASE retail_db;
USE retail_db;
CREATE USER 'retail_dba'@'%' IDENTIFIED BY 'retail_dba';
GRANT ALL PRIVILEGES ON retail_db.* TO 'retail_dba'@'%';
```
Correr script de datos:
```sh
source TETbigdata/rdbms/retail_db-data.sql
```
### Hive - Sqoop
Base de datos: 
```sh
create database retail_db;
use retail_db;
```
Importar datos via sqoop por Terminal:
```sh
sqoop import-all-tables --connect jdbc:mysql://<database>.rds.amazonaws.com:3306/retail_db --username=retail_dba --password=retail_dba --hive-database retail_db --hive-overwrite --hive-import --warehouse-dir=/tmp/retail_dbtmp -m 1 --mysql-delimiters
```

Importar datos via sqoop por HUE:
```sh
import-all-tables --connect jdbc:mysql://<database>.rds.amazonaws.com:3306/retail_db --username=retail_dba --password=retail_dba --hive-database retail_db --hive-overwrite --hive-import --warehouse-dir=/tmp/retail_dbtmp -m 1 --mysql-delimiters
```

#### Categorias más populares de productos
```sh
SELECT c.category_name, count(order_item_quantity) as count
FROM order_items oi
inner join products p on oi.order_item_product_id = p.product_id
inner join categories c on c.category_id = p.product_category_id
group by c.category_name
order by count desc
limit 10
```
Tabla de resultados
![Tabla1](https://github.com/alejocano22/TETbigdata/blob/master/Imagenes/Categor%C3%ADas%20m%C3%A1s%20populares%20de%20productos%20-%20Tabla.png)

Gráfica (X: Nombre de la categoría, Y: Contador)
![Gráfica1](https://github.com/alejocano22/TETbigdata/blob/master/Imagenes/Categor%C3%ADas%20m%C3%A1s%20populares%20de%20productos%20-%20Gr%C3%A1fica.png)

#### Top 10 de productos que generan más ganancias
```sh
SELECT p.product_id, p.product_name, r.revenue
FROM products p inner join
(select oi.order_item_product_id, sum(cast(oi.order_item_subtotal as float)) as revenue
from order_items oi inner join orders o
on oi.order_item_order_id = o.order_id
where o.order_status <> 'CANCELED'
and o.order_status <> 'SUSPECTED_FRAUD'
group by order_item_product_id) r
on p.product_id = r.order_item_product_id
order by r.revenue desc
limit 10
```

Tabla de resultados
![Tabla2](https://github.com/alejocano22/TETbigdata/blob/master/Imagenes/Productos%20que%20generan%20ganancias%20-%20Tabla.png)

Gráfica (X: Nombre de la categoría, Y: Contador)
![Gráfica2](https://github.com/alejocano22/TETbigdata/blob/master/Imagenes/Productos%20que%20generan%20ganancias%20-%20Gr%C3%A1fica.png)

### LOGS
Subir los logs al hdfs:
```sh
hdfs dfs -mkdir /user/<username>/datasets/retail_logs/
```
Nota: Clonar el repositorio:
```sh
hdfs dfs -put TETbigdata/Datasets/retail_logs/access.log /user/<username>/datasets/retail_logs/
```
Crear tablas ETL - Intermedia
```sh
USE <username>;
CREATE EXTERNAL TABLE tmp_access_logs (
        ip STRING,
        fecha STRING,
        method STRING,
        url STRING,
        http_version STRING,
        code1 STRING,
        code2 STRING,
        dash STRING,
        user_agent STRING)
    ROW FORMAT SERDE 'org.apache.hadoop.hive.contrib.serde2.RegexSerDe'
    WITH SERDEPROPERTIES (
        'input.regex' = '([^ ]*) - - \\[([^\\]]*)\\] "([^\ ]*) ([^\ ]*) ([^\ ]*)" (\\d*) (\\d*) "([^"]*)" "([^"]*)"',
        'output.format.string' = "%1$$s %2$$s %3$$s %4$$s %5$$s %6$$s %7$$s %8$$s %9$$s")
    LOCATION '/user/<username>/datasets/retail_logs/';
```
Crear directorio para tabla externa con ETL:
```sh
hdfs dfs -mkdir /user/<usernme>/warehouse/access_logs_etl
```
Crear tablas ETL - Final
```sh
CREATE EXTERNAL TABLE etl_access_logs (
        ip STRING,
        fecha STRING,
        method STRING,
        url STRING,
        http_version STRING,
        code1 STRING,
        code2 STRING,
        dash STRING,
        user_agent STRING)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/user/<username>/warehouse/access_logs_etl/';
```
Procesar ETL:
```sh
ADD JAR /usr/lib/hive/lib/hive-contrib.jar;
```
```sh
INSERT OVERWRITE TABLE etl_access_logs SELECT * FROM tmp_access_logs;
```
### Productos más visitados
```sh
SELECT count(*) as contador,url FROM etl_access_logs
WHERE url LIKE '%\/product\/%'
GROUP BY url ORDER BY contador DESC LIMIT 10;
```

### Guardar outputs en S3
Categorías más populares: 
```sh
CREATE EXTERNAL TABLE popular_categories (categorie_name STRING, count Bigint) 
LOCATION 's3://<bucket>/popular_categories/'
```
```sh
INSERT INTO popular_categories
SELECT c.category_name, count(order_item_quantity) as count
FROM order_items oi
inner join products p on oi.order_item_product_id = p.product_id
inner join categories c on c.category_id = p.product_category_id
group by c.category_name
order by count desc
limit 10
```
Productos que genran más ganancia:
```sh
CREATE EXTERNAL TABLE more_profit_products (product_id INT, product_name STRING, revenue DOUBLE) 
LOCATION 's3://<bucket>/more_profit_products/'
```
```sh
INSERT INTO more_profit_products
SELECT p.product_id, p.product_name, r.revenue
FROM products p inner join
(select oi.order_item_product_id, sum(cast(oi.order_item_subtotal as float)) as revenue
from order_items oi inner join orders o
on oi.order_item_order_id = o.order_id
where o.order_status <> 'CANCELED'
and o.order_status <> 'SUSPECTED_FRAUD'
group by order_item_product_id) r
on p.product_id = r.order_item_product_id
order by r.revenue desc
limit 10
```
Productos más visitados:
```sh
CREATE EXTERNAL TABLE most_visited (count Bigint, url STRING) 
LOCATION 's3://<bucket>/most_visited/'
```
```sh
INSERT INTO most_visited
SELECT count(*) as contador,url FROM etl_access_logs
WHERE url LIKE '%\/product\/%'
GROUP BY url ORDER BY contador DESC LIMIT 10;
```

Tabla de resultados
![Tabla3](https://github.com/alejocano22/TETbigdata/blob/master/Imagenes/Productos%20m%C3%A1s%20visitados%20(URL)%20-Tabla.png)

Gráfica - Distribución (X: Contador)
![Gráfica3](https://github.com/alejocano22/TETbigdata/blob/master/Imagenes/Productos%20m%C3%A1s%20visitados%20(URL)%20-%20Gr%C3%A1fica.png)

# SPARK
### Wordcount pyspark
```sh
spark-submit --master yarn --deploy-mode cluster wordcount-pyspark.py 
```
[Código](https://github.com/alejocano22/TETbigdata/blob/master/Programas/Spark/wordcount-pyspark.py)

## COVID
[Notebook](https://github.com/alejocano22/TETbigdata/blob/master/Programas/Spark/Notebooks/Jupyter/COVID_Spark_Lab.ipynb)<br/>
[outputs](https://github.com/alejocano22/TETbigdata/blob/master/Programas/Spark/Notebooks/Jupyter/outputs/COVID_Spark_Lab.ipynb)<br/>
[Data](https://github.com/alejocano22/TETbigdata/tree/master/Programas/Spark/Notebooks/Jupyter/covid-data)<br/>
Actualización: Mayo 3 del 2020

### Notebooks
#### Jupyter
[Jupyter](https://github.com/alejocano22/TETbigdata/tree/master/Programas/Spark/Notebooks/Jupyter)

#### Zeppeline
[Zeppeline](https://github.com/alejocano22/TETbigdata/tree/master/Programas/Spark/Notebooks/Zeppeline)
##### Wordcount
```sh
%spark.pyspark
files = sc.textFile("s3://acanomdatasets/datasets/gutenberg-small/*.txt")
wc = files.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
wc.coalesce(1).saveAsTextFile("s3://acanomoutputs/wordcount-spark/output4")
```
##### Wordcount en spark.sql
```sh
# Crear base de datos
%spark.sql    
CREATE DATABASE wordcountdb

# Mostrar bases de datos
%spark.sql
SHOW DATABASES

# Usar base de datos
%spark.sql
USE wordcountdb

# Crear tabla externa
%spark.sql
CREATE EXTERNAL TABLE gutenberg_small (line STRING) stored as textfile location 's3://acanomdatasets/datasets/gutenberg-small/*.txt'

# Mostrar tablas
%spark.sql
SHOW tables

# Wordcount ordenado por palabra
%spark.sql
SELECT word, count(1) AS count FROM (SELECT explode(split(line,' ')) AS word FROM gutenberg_small) w GROUP BY word ORDER BY word

# Wordcount ordenado por contador de mayor a menor
%spark.sql
SELECT word, count(1) AS count FROM (SELECT explode(split(line,' ')) AS word FROM gutenberg_small) w GROUP BY word ORDER BY count DESC
```
