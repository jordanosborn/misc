"""Create pdf from web book. Jordan Osborn 2018."""

import requests, bs4, re, pdfkit
from typing import List
from collections import OrderedDict
from multiprocessing import Pool
from sys import argv
import os
from shutil import rmtree

TMPOUTPUT = "haskellWeboutput"

def download(url: str) -> str:
    """Download url.

    Arguments:
        url {str} -- url to download

    Returns:
        [type] -- contents from url

    """
    print("Downloading " + url)
    text = requests.get(url).text
    print("Downloaded " + url)
    return text

def save(content:tuple) -> None:
    """Save file.

    Arguments:
        content {str} -- file content

    Returns:
        str -- [description]

    """
    print("Saving file " + content[0])
    with open(TMPOUTPUT + "/" + content[0]+".html", "w") as f:
        f.write(content[1])
    print("Saved file " + content[0])

if __name__ == "__main__":
    root = argv[1]
    contentPage = argv[2]
    output = argv[3]

    baseURIReg = re.compile(r"(http|https):\/\/(.+)")
    baseURI = baseURIReg.findall(root)[0][1]

    reg = re.compile(r".+?#.*")
    urls = map(lambda t: t.get("href"),  bs4.BeautifulSoup(download(root + "/" + contentPage), "html.parser").find_all("a"))
    chapters = [contentPage] + list(filter(lambda t: not (t.find("http") == 0 and t.find(baseURI) == -1 or reg.match(t)), urls))
    links: List[str] = list(map(lambda l: (root + "/" + l) if l.find(baseURI) == -1 else (l), chapters))
    order = [str(x) for x in range(0,len(links))]
    try:
        rmtree(TMPOUTPUT)
    except FileNotFoundError:
        print("Created output directory")
    os.mkdir(TMPOUTPUT)
    with Pool(10) as p:
        document = p.map(download, links)
    d = list(zip(order, document))
    with Pool(10) as p:
        p.map(save, d)
    print("\n\nDownloaded all files\n\n")

    print("Creating " + output)
    pdfkit.from_file(["haskellWebOutput/" + x + ".html" for x in order], output)
    print( "Created " + output)

#python3 learnYouAHaskell.py http://learnyouahaskell.com chapters output.pdf