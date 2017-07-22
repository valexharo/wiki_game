# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 19:28:09 2017

@author: valex
"""

from graphs import Graph
import re
from bs4 import BeautifulSoup
import requests
from urllib import parse


#Return HTLM content as a string object of a URL
def get_URL(url):
    try:
        # Web request
        req = requests.get(url)
        html = BeautifulSoup(req.text, "html.parser")
        # Validation of URL request
        status_code = req.status_code
        if status_code == 200:
            # Get only the content of div call bodyContent to discard html valueless
            content = html.find('div', id='bodyContent')
            return str(content)
    except Exception:
        return None

#Return valid links found in HTML content
def get_links(html, abs_URL):
    links = []
    for url in re.findall('''<a[^>]+href=["'](.[^"']+)["']''', html, re.I):
        link = url.split("#", 1)[0]
        #complete the URL
        if not url.startswith("http"):
            # is not absolute
            link = '{uri.scheme}://{uri.netloc}'.format(uri=parse.urlparse(abs_URL)) + link
        #Filter valid links    
        if (url.find("File:") == -1) and (url.find("Wikipedia:") == -1) and (url.find("Special:") == -1) and (url.find("Category:") == -1) and (url.find("Help:") == -1) and (link not in links) and ("wikipedia.org/wiki/" in link):   
            links.append(link)
    return links

#Return a list of links
def crawler(urlInicial, urlFin, maxPages):
    pagVisitar =[urlInicial]
    visitadas=0
    enlaces = {}
    #Flag to stop the algorithm if the target url is found
    band = False     
    while visitadas < maxPages and pagVisitar != []:
        visitadas=visitadas+1
        url=pagVisitar[0]
        pagVisitar=pagVisitar[1:]
        try: 
            #print (visitadas,"Visitada:",url )
            parser=get_URL(url)
            links=get_links(parser,url)
            pagVisitar=pagVisitar+links
            enlaces[url] = links[2:]
            #Previous analysis of the target URL in html-string object
            if (urlFin.split(".org/")[1] in parser):
                if band:
                    pagVisitar=[]                    
                else:
                    band = True
                    pagVisitar=[urlFin]                    
        except:
            print("Failed")
    return enlaces

#Returns the best path of links
def wikiGame(urlInicial, urlFinal, maxPages):
    datos= crawler(urlInicial,urlFinal,1000)
    graph = Graph(datos)
    responds = []
    #Verify that the target url has been found
    if (urlFinal in datos):
        paths=graph.find_all_paths(urlInicial, urlFin)
        min_path = 0
        #Analyzes the shortest path between solutions
        for path in paths:
            len_path = len(path)
            if min_path == 0:
                min_path= len_path
                path_return = path
            elif len_path < min_path:
                min_path= len_path
                path_return = path
        #Prepares the structure of the response
        for link in path_return:
            title = link.split("/wiki/")[1]
            responds.append({"title" : title, "url": link})
        return responds
    else: 
        return responds


if __name__ == "__main__":
    urlInicio = "https://en.wikipedia.org/wiki/Fyodor_Dostoyevsky"
    urlFin = "https://en.wikipedia.org/wiki/Medieval"
    links = wikiGame(urlInicio,urlFin,50)
    print (links)