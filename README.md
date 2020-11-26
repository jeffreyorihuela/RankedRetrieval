# Ranked Retrieval

Pasos para correr el proyecto:
1. Descargar la data desde https://onedrive.live.com/?authkey=%21ANNEKv7tNdlSSQk&id=C2923DF9F1F816F%2150817&cid=0C2923DF9F1F816F y extraerla en la carpeta data
2. Instalar ntlk (si usas conda -> `conda install nltk`)
3. Instalar Flask y Flask-cors (`pip install flask` y  `pip install flask-cors`)
3. Desplegar el server con `flask run`
4. Desplegar el frontend desde la carpeta `my-app` ejecutar `yarn start`

## Algoritmo

1. Primero hacemos un preprocesamiento de información con el archivo `preprocesor.py` filtrando las 50 palabras más frecuentes. (Este parámetro puede incluso llegar a ser 1000)
2. Creamos para cada palabra del paso anterior un archivo almacenando el índice invertido, este paso se encarga `indexbuilder.py`
3. Vectorizamos cada tweet de la carpeta data usando la técnica tf-idf, cada vector será almacenado en un mismo csv generado por `tfidf.py`
4. Por último levantamos un servidor donde el endpoint principal se encarga de recibir un request. Dicho request será vectorizado de la misma forma que hemos hecho con los anteriores tweets. De esta forma podemos usar *similitud de cosenos* y dar como response el tweet más similar.


