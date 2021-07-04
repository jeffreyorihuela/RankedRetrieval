# Ranked Retrieval

Pasos para correr el proyecto:
1. Descargar la data desde https://onedrive.live.com/?authkey=%21ANNEKv7tNdlSSQk&id=C2923DF9F1F816F%2150817&cid=0C2923DF9F1F816F y extraerla en la carpeta data
2. Instalar ntlk (si usas conda -> `conda install nltk`)
3. Instalar Flask y Flask-cors (`pip install flask` y  `pip install flask-cors`)
4. Crear la carpeta block a nivel del archivo `app.py`
3. Desplegar el server con `flask run`
4. Desplegar el frontend desde la carpeta `my-app` ejecutar `yarn start`

## Construcción del Indice Invertido

1. Se empieza leyendo cada tweet y se va almacenando los cada termino en un bloque. 
2. Cuando un bloque ha ocupado su máxima capacidad se procede a crear un nuevo bloque continuando la inserción de términos por cada bloque.
3. Al finalizar la indexación de todos los terminos reducimos la cantidad n de bloques a un super bloque. Esta técnica es llamada Block Sorting Based Index (BSBI)

## Manejo de Memoria Secundaria

El BSBI almacena en disco un grupo de terminos en un bloque . En nuestro proyecto usamos archivos extensión txt. Se crea por último un super bloque el cúal es un diccionario de todos los términos de los tweets. Este super índice invertido ordenado mantiene la estructura de par (DOCID: TWEETID).

## Ejecución óptima de consultas

Gracias a la construcción del índice invertido podemos crear una matriz de pesos TF - IDF para optimizar las consultas. Construimos la matriz a través de resultado del BSBI por cada termino podemos calcular TF en el tweet y también debido a que sabemos todas las ocurrencias del termino en la colección podemos calcular tambien el IDF. Almacenamos esta matriz en disco, cada vez que hagamos una consulta. Iteramos por cada termino de la consulta y vamos buscando el score de los documentos que contienen dicho termino a través de la similitud de cosenos. Ordenamos por orden descendente el score de los documentos y los que alcancen mayor puntaje serán retornados como respuesta a la consulta.
