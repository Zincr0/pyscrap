Framework “pyscrap”

Inspirado en “scrapy”; uno de los frameworks de webscraping más avanzados existentes a la fecha, pero más simple y ajustado a necesidades específicas, a saber:
*Scripts de extracción instalables como paquetes
**Compatible entre sistemas basados en unix
*Módulos ejecutables
*Separación completa entre la capa de extracción y la de base de datos.
*Ejecución como proceso normal.

Enfocado en el desarrollo rápido, una vez instalado, se usa el comando “wscrap” para crear un proyecto nuevo con un demo funcional. 


*: A diferencia de scrapy.
**: Incluye mac, excluye windows.
La estructura de cada proyecto “wscrap” corresponde a:

ejemplo/
├── ejemplo
│   ├── exampleSpider.py
│   ├── __init__.py
│   ├── item.py
│   ├── pipeline.py
│   └── settings.py
├── MANIFEST.in
├── README.txt
└── setup.py

Donde:
“exampleSpider.py” corresponde al script de extracción. 
“item.py” corresponde a la definición de cada item a extraer y a cada conjunto de items con sus campos respectivos; un item por ejemplo podría ser un comentario que contenga su texto y autor y el conjunto de comentarios podría contener la url desde donde se extrayeron.
 “pipeline.py
” contiene las funciones que se usarán para almacenar o procesar cada item o cada conjunto de items definidos en “item.py”, además de una función pensada para obtener urls invocable desde dentro del script del script de extración como método estático (getUrls) sin importarla.
“settings.py” contiene las relaciones sobre qué función de “pipeline.py” se usará con qué item o conjunto de items de “item.py” además de los headers que se usarán por defecto al descargar una url.
“README.txt
” puede contener una descripción del proyecto.
“setup.py
” es el script estándar usado en python para empaquetar o instalar proyectos, aquí se definen las dependencias entre otras cosas.
Los demás archivos son necesarios para el empaquetamiento y en general no necesitan ser modificados.

Un proyecto puede instalarse con:

python setup.py install

O instalarse como una referencia para seguir desarrollandolo sin moverlo con:

python setup.py develop


Funcionamiento: 

Cada clase de extracción debe heredar desde la clase “spider” del framework, donde cada item retornado por la función “parse” de dicha clase será procesado de acuerdo a la configuración establecida en “settings.py” usando las funciones definidas en “pipeline.py
”. El proceso es transparente para el programador y se consigue gracias a la metaclase especial que usa “spider”. 

En a práctica, esto significa que no es necesario importar nada fuera del archivo “item.py” en el script de extracción; vale decir, la capa de extracción es independiente de la de almacenamiento.