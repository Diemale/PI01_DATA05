# <h1 align=center><span style="color:blue"> **PROYECTO INDIVIDUAL Nº1** </span></h1>

## **Introducción**
<p>
Este proyecto forma parte de las prácticas de laboratorios de Henry. En esta instancia de evaluación se nos propuso: "realizar una ingesta de datos desde diversas fuentes, posteriormente aplicar las transformaciones que consideren pertinentes, y luego disponibilizar los datos limpios para su consulta a través de una API. Esta API deberán construirla en un entorno virtual dockerizado."
</p>
<hr>  

## **Desarrollo del proyecto**

### **EDA y ETL**

Para comenzar, contábamos con cuatro datasets de distintas plataformas de entretenimiento(Amazon Prime, Disney, Hulu y Netflix). Tres de estos datasets estaban en formato .csv y uno en .json.

<p>En primer lugar, se optó por convertir el archivo json a formato csv, para eso se utilizó una función creada en una jupyter notebook (archivo fileConverter) .
Luego, se procedió a realizar el trabajo de ingeniería necesario para limpiar, normalizar y almacenar los datos. Esta tarea se ve reflejada en otra jupyter notbook de nombre EDA_ETL. </p>

<p> En el archivo EDA_ETL se realizó el análisis exploratorio de datos, utilizando principalmente pandas y en menor medida la librería seaborn. Después, se llevó a cabo la limpieza de cada uno de los datasets, para luego concatenarlos y finalmente, guardar este dataframe como un archivo csv que serviría de insumo para la puesta en marcha de nuestra API. Cabe destacar que, en un primer momento, se pensó realizar la tarea utilizando una base de datos para el almacenamiento. Sin embargo, algunas de las consultas que se debían realizar se hacían sobre columnas que contenían demasiados datos múltiples. La tarea parecía simplificarse utilizando el método get_dummies de pandas. Por lo tanto, se optó por trabajar sin una base de datos. </p>

### **Creación de la API**

El objetivo de este paso era realizar cuatro queries desde una web API.
Para cumplir con este punto se escogió FASTAPI.
La creación de la API consta de un solo archivo .py, a saber main.py. Debido a que no se utilizó una base de datos, no fue necesario crear archivos para el manejo de esta, ni para los modelos de algún ORM que mapeara las tablas relacionales, ni tampoco para los clásicos schemas de PYDANTIC. Las librerías utilizadas
en el script main.py fueron, fastapi, pandas y uvicorn. La última, fue importada para explicitar
en el mismo script la actualización automática del server(en lugar de indicarse por la terminal con el comando uvicorn --reload).
Esto permitió crear la imagen de docker a través de un Dockerfile de una manera más simple.

Las consultas a realizar fueron:

**1) Máxima duración según tipo de film (película/serie), por plataforma y por año:
    El request debe ser: get_max_duration(año, plataforma, [min o season])**

Para esta query se creó la función `get_max_duration(year: int, company: str, category: str)` que recive el año, la plataforma y la categoría(serie o película) y retorna una string informando cual es la serie con más temporadas o la película de mayor duración para la plataforma y el año pedidos.

**2) Cantidad de películas y series (separado) por plataforma
    El request debe ser: get_count_plataform(plataforma)**
    
Esta query se realiza gracias a la función `show_count_two(company: str)` que recibe el nombre  de la compañia (plataforma) como parámetro y devuelve una string que señala cuantas series y cuantas películas tiene listadas la plataforma ingresada como parámetro.
  
**3) Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.
    El request debe ser: get_listedin('genero')**
    
La función encargada de llevar a cabo esta query es `get_genre_qt(genre: str)` que recibe una string(genre) como parámetro y devuelve otra string que muestra la cantidad de títulos que pertenecen a este género en nuestro dataset y además, cual es la plataforma con mayor oferta del género solicitado.
    
**4) Actor que más se repite según plataforma y año. 
    El request debe ser: get_actor(plataforma, año)**
  
 Esta query fue aborda con la función `max_performer(company: str, year: int)` que recibe una string (company) y un int (year) como parámetros y devuelve una string que informa cual es la persona que tiene mayor cantidad de apariciones en la compañía y año solicitados.
    
    
### **Containerización de la API**

El paso final de nuestro proyecto constó de containerizar la API creada. Para esto se utilizó Docker Desktop. En primer lugar, se creó la imagen a través de un Dockerfile utilizando Pycharm. Los pasos descriptos en el script de docker son los siguientes:

**1) Especificar una imagen base**

`FROM python:3.8.2`

**2) Crear un directorio que funcione como punto de partida en el container**


`WORKDIR /fastapi-app`

**3) Copiar todas las dependencias utilizadas en la API**

`COPY requirements.txt .`


**4) Instalar todas esas dependencias en el container objetivo**

`RUN pip install -r requirements.txt`

**5) Copiar en el container el directorio padre de mi archivo main**

`COPY /PI01_DATA05 ./PI01_DATA05`

**6) Exponer un puerto para el container**

`EXPOSE 8000`

**7) Copiar el dataset en el container**

`COPY PI01_DATA05/all_shows.csv ./`

**8) Especificar un punto de entrada para el contenedor**

`CMD ["python", "./PI01_DATA05/main.py", "--host=0.0.0.0", "--reload"]`

Por último, desde la terminal, se mapearon los puertos del sistema operativo y del contenedor para que hubiese conectividad entre estos.

<hr>

## **Puntos a mejorar en este proyecto**

Debido al corto tiempo en el que se debió realizar este proyecto, quedaron varios puntos de mejora a futuro. Entre estos podemos mencionar:

1) Normalizar los géneros de las distintas plataformas de manera que un mismo género no tenga diferencias según la plataforma en la que se encuentra.

2) Mejorar las restricciones de los inputs de FASTAPI, solo están restringidos por el tipo de dato.

3) Mejorar la organización de directorios. Sería ideal que el script main.py acceda al dataset estando este en otro directorio. Se decidió hacerlo de esta manera para simplificar la creación del DockerFile.

