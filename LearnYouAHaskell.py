"""Create pdf from web book. Jordan Osborn 2018."""

import requests, bs4, re, pdfkit
from collections import OrderedDict
from multiprocessing import Pool
from sys import argv

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

if __name__ == "__main__":
    root = argv[1]
    contentPage = argv[2]
    output = argv[3]

    baseURIReg = re.compile(r"(http|https):\/\/(.+)")
    baseURI = baseURIReg.findall(root)[0][1]

    reg = re.compile(r".+?#.*")
    urls = map(lambda t: t.get("href"),  bs4.BeautifulSoup(download(root + "/" + contentPage), "html.parser").find_all("a"))
    chapters = [contentPage] + list(filter(lambda t: not (t.find("http") == 0 and t.find(baseURI) == -1 or reg.match(t)), urls))
    links = list(map(lambda l: (root + "/" + l) if l.find(baseURI) == -1 else (l), chapters))

    with Pool(10) as p:
        document = p.map(download, links)
    print("\n\nDownloaded all files\n\n")
    pdfkit.from_string("\n".join(document), output)
    
    print("PDF created")
