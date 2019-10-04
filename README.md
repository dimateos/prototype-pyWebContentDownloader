# pyWebContentDownloaderByExt
> Download all files of given extension from a bunch of urls automaticly

* English code, but error logs and usage in spanish atm
* IMO decent code and some error handling but not heavily tested

# You can grab the last release .exe

* ***ENG***: So you dont need python or anything
* ***ESP***: Asi no necesitas ni python ni nada

> done with [PyPI](https://pypi.org/project/auto-py-to-exe/)

# Dependencies (python)

```python
import urllib.request #html requests
#import webbrowser #check htmls
#from bs4 import BeautifulSoup #html soup
import re #regular expresions
import os #working with directories
import datetime #unique folders
```

# ENG
The idea is that sometimes you are not able to just right click save something right away. You have to inspect the html and try to find the url of the content you want to save. And if that is a collection of 64 pictures then... Better use this.

Some pages may have heavy anti-scrapping or just very weird urls (subdomains) and the script wont be able to grab the files.

## Usage
> Execute once the script (or exe) to create the file `url.txt`
* You can download all photos, videos, etc... all the files of a given a extension (`.jpg`)
* Drop all the urls you need in `url.txt` (a simple configuration is also there)
* Run the script. It has some error handling and messages to avoid downloading 1000+ files etc
* It will create a folder for the batch of files

> Atm these logs are actually in spanish but yea

# ESP

La idea es que a veces no se puede guardar todo simplemento haciendo boton derecho-guardar. Tienes que inspeccionar el html y tratar de encontrar la url de lo que quieres guardar. Y si eso es una coleccion de 64 fotos... Mejor usa esto.

Algunas paginas tendran proteccion o simplemente url (subdominios) muy raras y el script no podra obtener los archivos.

## Uso
> Ejectuta una vez el script (o exe) para crear el archivo `url.txt`
* Puedes descargar todas las fotos, videos, etc... todos los archivos de una dada extension (`.jpg`)
* Pon las urls en el archivo `url.txt` (ahi tmb estan unas opciones simples)
* Ejecuta el script. Tiene algo de control de errorer y mensajes para evitar que bajes 1000+ archivos etc
* Creara una carpeta para los archivos descargados
