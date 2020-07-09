import sys
import os
import argparse
import requests
from lxml import etree
from contextlib import closing
from tqdm import tqdm


class Scihub:
    def __init__(self):
        self.downloadInfoList = ""
        self.scihubUrl = "https://sci-hub.tw/"
        self.xPath = '''//*[@id="pdf"]/@src'''
        self.downloadPath = "pdf"
        self.proxy = {}

        self.doilist = []
        return

    def setDownloadInfoList(self, downloadInfoList):
        self.downloadInfoList = downloadInfoList

    def setScihubUrl(self, scihubUrl):
        self.scihubUrl = scihubUrl

    def setXPath(self, xPath):
        self.xPath = xPath

    def setDownloadPath(self, downloadPath):
        self.downloadPath = downloadPath

    def setProxy(self, proxy):
        self.proxy["http"] = proxy
        self.proxy["https"] = proxy

    def interactiveShell(self):
        if not os.path.exists(self.downloadPath):
            os.mkdir(self.downloadPath)
        elif os.listdir(self.downloadPath):
            while True:
                choice = input(
                    "Warning: download path existed and not empty, continue?[Y/n]")
                if choice in ["N", "n", "no", "NO", "No"]:
                    sys.exit(1)
                elif choice in ["Y", "y", "yes", "Yes", "YES", ""]:
                    break
                else:
                    print("Invalid input")
        return

    def getFileSize(self, downloadLinkResponse, index, listLength):
        headerDict = dict(downloadLinkResponse.headers)
        contentLength = headerDict.get('Content-Length')
        # print("File (%d/%d) Size: %s"
        #     % (
        #         index+1, listLength,
        #         (str(int(contentLength)/1000000)+" MB" if contentLength else "NA")
        #     )
        #     )
        return int(contentLength)

    def getDoiList(self):
        with open(self.downloadInfoList, "r") as doi:
            self.doilist = doi.readlines()
            self.doilist = list(map(lambda x: x.rstrip("\n"), self.doilist))
        return

    def downLoad(self, indX, doiX):

        if self.proxy:
            req = requests.get(url=self.scihubUrl+doiX, proxies=self.proxy)
            root = etree.HTML(req.content)
            elementDownloadLink = root.xpath(self.xPath)[0]
            reqFile = requests.get(
                url=elementDownloadLink, stream=True, proxies=self.proxy)
        else:
            req = requests.get(url=self.scihubUrl+doiX)
            root = etree.HTML(req.content)
            elementDownloadLink = root.xpath(self.xPath)[0]
            reqFile = requests.get(url=elementDownloadLink, stream=True)

        contentLength = self.getFileSize(reqFile, indX, len(self.doilist))
        fileName = doiX.replace("/", ".")+".pdf"
        with closing(reqFile) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            with open(os.path.join(self.downloadPath, fileName), "wb") as file:
                for data in tqdm(
                    response.iter_content(chunk_size=chunk_size),
                    total=int(contentLength/chunk_size), unit="KiB",
                    leave=False,
                    desc="Current Progress"
                ):
                    file.write(data)
        return

    def scihubQuery(self):
        self.interactiveShell()
        self.getDoiList()
        for indX, doiX in tqdm(
            enumerate(self.doilist),
            desc="Overall Progress",
            total=len(self.doilist),
            unit="paper"
        ):
            try:
                self.downLoad(indX, doiX)
            except:
                print("Error: Connection failed")
                with open("errlog.txt", "a") as errLog:
                    errLog.write(doiX+"\n")
                sys.exit(1)
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='scihub.py is a script written in Python for batch query of research paper in sci-hub accroding to your DOI/PMID list'
    )
    parser.add_argument(
        '--file', '-f', help='[REQUIRED]Your input file, one row for a DOI/PMID', required=True)
    parser.add_argument(
        '--scihuburl', '-u', help='current sci-hub url, default = https://sci-hub.tw/')
    parser.add_argument('--downloadpath', '-d',
                        help='output folder, will be created if not existed')
    parser.add_argument('--proxy', '-p', help='proxy, default = empty')
    parser.add_argument(
        '--xpath', '-x', help='[EXPERIMENTAL]pdf download link xpath selector')
    args = parser.parse_args()
    scihub = Scihub()
    scihub.setDownloadInfoList(args.file)
    if args.scihuburl:
        scihub.setScihubUrl(args.scihuburl)
    if args.downloadpath:
        scihub.setDownloadPath(args.downloadpath)
    if args.proxy:
        scihub.setProxy(args.proxy)
    if args.xpath:
        scihub.setXPath(args.xpath)
    scihub.scihubQuery()
