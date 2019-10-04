# dimateos (github)

# English code, but error logs and usage in spanish
# IMO decent code and some error handling but not heavily tested
# some code leftovers here and there

# exe (yo me he buildeado mi exe)
#https://stackoverflow.com/questions/12059509/create-a-single-executable-from-a-python-project
#https://youtu.be/lOIJIk_maO4
#https://www.youtube.com/watch?v=-W_VsLXmjJU

# bank
#https://www.riojasalud.es/noticias/6524-alrededor-de-1-500-personas-han-participado-en-el-primer-paseo-saludable-de-este-ano-que-ha-discurrido-por-la-pasarela-nueva-sobre-el-iregua
#https://www.larioja.com/la-rioja/paseos-saludables-20180325160932-ga.html
#https://www.larioja.com/multimedia/fotos/local/20140406/cita-paseos-saludables-30890228818-mm.html
#https://www.youtube.com/playlist?list=WL
#https://www.imdb.com/user/ur70447890/lists?sort=name&order=asc

# fixed formats
#https://mynoise.net/NoiseMachines/windSeaRainNoiseGenerator.php
#//mynoise.net/NoiseMachines/windSeaRainNoiseGenerator.php
#/mynoise.net/NoiseMachines/windSeaRainNoiseGenerator.php
#mynoise.net/NoiseMachines/windSeaRainNoiseGenerator.php
#mynoise.net
#/mynoise.net

import urllib.request #html requests
#import webbrowser #check htmls
# from bs4 import BeautifulSoup #html soup
import re #regular expresions
import os #working with directories
import datetime #unique folders

chunk = 128000 * 4; slash = "/"
web = "https:"; web_alt = "http:"; www = "www."
#headers={'User-Agent': 'Mozilla/5.0'}

# avoid scrap blocking on some sites
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
opener = AppURLopener()

# avoid some keywords for chaed images
chacheCrap = [" ", "cache"]

###############################################################################
### initial functions

# first use
urlsFilename = "urls.txt"
def firstUsage():
    try: file=open(urlsFilename,"w")
    except:
        print("Error al crear el archivo", urlsFilename)
        exit("Vuelva a intentarlo, si continua fallando contacte con dimateos")
    file.write("Extension: jpg\nPreguntar para cada link (1 o 0): 1\nIntentar buscar nombre de carpeta (1 o 0): 0\nLinks (uno por linea): ")
    file.close()
    print("Complete el archivo", urlsFilename, "y vuelva a ejecutar el programa")
    exit()

# read stuff from the file
def readLinks(linksFile):
    lines = [line.strip(' \n"') for line in linksFile]
    ext = lines[0][-3:]
    askEachLinkMode = lines[1][-1] == "0"
    findFolderMode = lines[2][-1] == "1"
    return ext, askEachLinkMode, findFolderMode, lines[4:]

###############################################################################
### Early INIT and config

try: urlsFile = open(urlsFilename,"r")
except: firstUsage()
print("Encontrado archivo", urlsFilename)
ext, askEachLinkMode, findFolderMode, urls = readLinks(urlsFile)
urlsFile.close()

# check if any links etc
if (len(urls) == 0):
    print("No se encontraron urls en", urlsFilename)
    firstUsage()
print("Encontradas", len(urls), "urls")
print("Extension:", ext)
print("askEachLinkMode:", askEachLinkMode)
print("findFolderMode:", findFolderMode)
print()

###############################################################################
### html, scraping and re functions

# download html
def getHTML(url):
    fail = False; html = ""

    #req = urllib.request.Request(url, headers=headers)
    #try: html=urllib.request.urlopen(req).read()

    #avoiding blocked scraping (ej: www.riojasalud.es)
    try: html=opener.open(url).read()
    except: fail = True

    if fail: print("Error al descargar html, prueba poniendo o quitando", web)
    else: print("Descargado html con exito")

    # check correct html download
    #outFile = open('outFile.html', 'wb')
    #outFile.write(html)
    #webbrowser.open("outFile.html")
    #webbrowser.open(url)

    return html, fail

#extract the domain
def getDomain(url):
    fail = False; dom = ""
    try: dom = re.search('(www.(.*?)/)', str(url)).group(1).strip(' /"')
    except:
        # some url have no www
        try: dom = re.search('(//.(.*?)/)', str(url)).group(1).strip(' /"')
        except:
            # no www nor https:// then just hope the leftmost is the domain
            if url[0] == slash: url = url[1:]
            f = url.find(slash)
            if f == -1: dom = url
            else: dom = url[:f]

    return dom, fail

"""
#find the soup
lookslikeClass = "voc-figure-container__figure"
def getElements(html):
    soup=BeautifulSoup(html,"html.parser")
    elements = soup.find_all("div", class_=lookslikeClass)

    # finding the soup
    #print(elements)
    #print(len(elements))
    #print(elements[0])
    #print(type(elements[0]))
    #dir(type(elements[0]))
    #print(elements[0].attrs)
    #print(elements[0].attrs["data-voc-image"])
    #for elem in elements[0].attrs:
    #    print("--> ", elem, " : ", elements[0][elem])

    return elements
"""

# extract the links
lookslikeAttr = "data-voc-image"
def getLinks(elements):
    links = []
    for div in elements:
        link = div.attrs[lookslikeAttr]
        links.append(web + link)

    return links

# format link for less possible issues
def getCleanedLink(link, dom):
    link = link.replace(web_alt, web).replace("/./", slash)

    #first find dom
    dom_i = link.find(dom.replace(www, ""))
    if dom_i == -1: #(-1 means not found)

        #now find https
        web_i = link.find(web)
        if web_i == -1: return web + "//" + dom + link
        elif web_i != 0: return link[web_i:]
        else: return link

    else:
        web_i = link.find(web)
        if web_i == -1:
            #remove any / at leftmost
            while link[0] == slash: link = link[1:]
            return web + "//" + link
        elif web_i != 0: return link[web_i:]
        else: return link

# extract the links using regular expresions
# ((\"|\'|=)((?!(\"|\'|=)).)*?extension) looks fine af
rexpr= '(("|\'|=)((?!("|\'|=)).)*?{})'
def getLinksByExt(html, ext, dom):
    #find the tuples
    tuples = re.findall(rexpr.format(ext), str(html))
    #strip and filter them
    links = [t[0].strip('\n"\'=') for t in tuples if not any(s in t[0] for s in chacheCrap)]
    #clean / format them
    return [getCleanedLink(l, dom) for l in links]

# extract filenames
findChar = slash;
def getFilenames(links):
    filenames = []
    for l in links:
        for n in range(len(l)):
            if l[-n] == findChar:
                # unqote url chars to normal string
                filenames.append(urllib.request.unquote(l[-n+1:]))
                break

    return filenames

###############################################################################
### files and downloading functions

# create folder
def createFolder(linkSample, dom, ext):
    #date + domain + extension
    foldername = str(datetime.datetime.now())[:-5] + " " + dom + " " + ext.upper()
    foldername = foldername.replace(":", ".").strip('\//*?"<>|')

    if findFolderMode:
        firstChar = -1
        for n in range(len(linkSample)):
            if linkSample[-n] == findChar:
                if firstChar == -1: firstChar = -n-1
                else:
                    foldername = linkSample[-n+1:firstChar] + " " + foldername
                    break

    fail = False
    try: os.makedirs(foldername, exist_ok=True)
    except: fail = True

    if fail: print("Error al crear carpeta >", foldername)
    else: print("Carpeta >", foldername, "< creada")
    return foldername, fail

# download
def downloadImage(link, foldername, filename, n, m):
    error = False

    #descargar imagen
    try: image=opener.open(link)
    except: print("Error al descargar la imagen", link); error = True; return

    #crear archivo
    name = foldername + slash + filename
    try: file=open(name, "wb")
    except: print("Error al crear el archivo", name); error = True; return

    while True:
        try: data=image.read(chunk)
        except: print("Error durante la copia del archivo", name); error = True; return
        if len(data)<1: break

        try: file.write(data)
        except: print("Error durante la copia del archivo", name); error = True; return

    file.close()
    print(n, slash, m, ">", filename)

###############################################################################
### script EXECUTION

done_url = "\ndone url...\n\n"
for url in urls:
    print("Procesando url", url)

    #extract domain for the best getLinks possible
    dom, fail = getDomain(url)
    if fail: print(done_url); continue

    #html sometimes times out so restart
    html, fail = getHTML(url)
    if fail: print(done_url); continue

    #soup way (dropped)
    #elements = getElements(html)
    #if len(elements) == 0:
    #    print("No elements found...")
    #    print(done_url)
    #    continue
    #links = getLinks(elements)
    #filenames = getFilenames(links)

    #regular expresion
    links = getLinksByExt(html, ext, dom)
    if len(links) == 0:
        print("No elements found...")
        print(done_url)
        continue
    links = list(set(links))
    filenames = getFilenames(links)

    #login info obtained
    print()
    for l in links: print(l)
    print()
    sorted_filenames = sorted(list(set(filenames)))
    for n in sorted_filenames: print(n)

    print()
    print("Encontrados {} links".format(len(links)))
    print("Encontrados {} links unicos (algunos quizas no perfectos)".format(len(links)))
    print("Encontrados {} filenames (ordenados y perfectos)".format(len(sorted_filenames)))
    print()

    #ask user
    print("Se creara una carpeta para descargar las posibles", len(links), "imagenes...")
    num = -1
    if not askEachLinkMode:
        num = int(input("Escriba el numero de imagenes que quiere descargar (-1 es todas): ").strip())

    #ask user
    if num == 0: print(done_url); continue

    foldername, fail = createFolder(links[0], dom, ext)
    print()
    if fail: print(done_url); continue

    #download
    if num == -1: num = len(links)
    print("Descargando imagenes...")
    for n in range(num): downloadImage(links[n], foldername, filenames[n], n, num)

    print(done_url)

# close
print()
exit("No hay mas urls...")
