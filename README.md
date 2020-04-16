# Laboratorios de BIG DATA
Alejandro Cano Múnera <br/>
Universidad EAFIT 

# EMR
## Scripts
[Scripts EMR](https://github.com/alejocano22/TETbigdata/tree/master/EMR)

# Programas
## Wordcount
### Ejecutables:
[Códigos](https://github.com/alejocano22/TETbigdata/tree/master/Programas/Wordcount) <br/>
Local: <br/>
```sh
$ python wordcount-local.py < input >
$ python wordcount-mr.py -r local < input > -o < output >
```

EMR:  <br/>
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

### Ejecutables:

[Códigos](https://github.com/alejocano22/TETbigdata/tree/master/Programas/Stocks)

### 1. Día de menor valor - Día de mayor valor
Por acción, dia-menor-valor, día-mayor-valor  <br/>
Local: <br/>
```sh
$ python stocks-maxmin-mr.py -r local < input file >
```
EMR:  <br/>
Se deben actualizar las credenciales de aws en el archivo `mrjob.conf`   <br/>

Datos de entrada en s3: 
```sh
python stocks-maxmin-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/otros/dataempresas2.txt
```
Datos de entrada y de salida en s3: 
```sh
python stocks-maxmin-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/otros/dataempresas2.txt -o s3://acanomoutputs/stocks-maxmin-outputs/
```
Output: 
```sh
compañía, [[min, fecha_min], [max, fecha_max]]
```
Donde `compañia` es el nombre de la compañia, `min` es el precio mínimo que alcanzo la acción en la fecha `fecha_min` y `max` es el precio máximo que alcanzo la acción en la fecha `fecha_max`. <br/>

### 2. Acciones que siempre han subido o se mantienen estables
Listado de acciones que siempre han subido o se mantienen estables.<br/>
Local: <br/>
```sh
$ python stocks-risenstable-mr.py -r local < input file >
```
EMR: <br/>
Se deben actualizar las credenciales de aws en el archivo `mrjob.conf`    <br/>

Datos de entrada en s3:
```sh
python stocks-risenstable-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/otros/dataempresas2.txt
```
Datos de entrada y de salida en s3:
```sh
python stocks-risenstable-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/otros/dataempresas2.txt -o s3://acanomoutputs/stocks-risenstable-outputs/
```
Output:
```sh
compañía, mensaje
```
Donde `compañia` es el nombre de la compañia y `mensaje` es "Raise or stable all time." Que indica que el precio de la acción ha subido o se ha mantenido estable en el historico de datos. <br/>

### 3. Día negro
DIA NEGRO: Saque el día en el que la mayor cantidad de acciones tienen el menor valor de acción (DESPLOME), suponga una inflación independiente del tiempo.<br/>
Local: <br/>
```sh
$ python stocks-blackday-mr.py -r local < input file >
```
EMR: <br/>
Se deben actualizar las credenciales de aws en el archivo `mrjob.conf`    <br/>

Datos de entrada en s3:
```sh
python stocks-blackfriday-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/otros/dataempresas2.txt
```
Datos de entrada y de salida en s3:
```sh
python stocks-blackday-mr.py -c mrjob.conf -r emr s3://acanomdatasets/datasets/otros/dataempresas2.txt -o s3://acanomoutputs/stocks-blackday-outputs/
```

Output:
```sh
[mensaje, conteo], fecha
```
Donde `mensaje` es "Black Friday" y `conteo` es el número de compañias que registrarón la acción más baja en `fecha`. <br/>
