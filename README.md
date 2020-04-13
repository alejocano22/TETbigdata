# Laboratorios de BIG DATA
Alejandro Cano Múnera <br/>
Universidad EAFIT 

# EMR
## Scripts
[Scripts EMR](https://github.com/alejocano22/TETbigdata/tree/master/EMR)

# Programas
## Wordcount

```sh
$ python wordcount-local.py < input file >
$ python wordcount-mr.py -r local < input file >
```

## Stocks
(2) Se tiene un conjunto de acciones de la bolsa, en la cual se reporta a diario el valor promedio por acción <br/>
[Estructura de datos](https://github.com/alejocano22/TETbigdata/blob/master/Datasets/dataempresas.csv) <br/>

### Ejecutables:

[Códigos](https://github.com/alejocano22/TETbigdata/tree/master/Programas/Stocks)

1. Por acción, dia-menor-valor, día-mayor-valor  <br/>
```sh
$ python stocks-maxmin-mr.py -r local < input file >
```

2. Listado de acciones que siempre han subido o se mantienen estables.<br/>
```sh
$ python stocks-risenstable-mr.py -r local < input file >
```

3. DIA NEGRO: Saque el día en el que la mayor cantidad de acciones tienen el menor valor de acción (DESPLOME), suponga una inflación independiente del tiempo.<br/>
```sh
$ python stocks-blackday-mr.py -r local < input file >
```


