import requests
import re
import sys

SCIHUB_URL = "https://sci-hub.tw/"

with open("dl_links.txt", "w") as output:
    with open("./doilist.txt", "r") as doi:
        doilist = doi.readlines()
        doilist = list(map(lambda x: x.rstrip("\n"), doilist))
        for doiX in doilist:
            try:
                pattern = re.compile(r'''<iframe src = ".*" id = "pdf"></iframe>''')
                req = requests.get(url=SCIHUB_URL+doiX)
                dl_url = (pattern.findall(req.text)[0].replace('''<iframe src = "''', "").replace('''" id = "pdf"></iframe>''', ""))
                output.write(dl_url+"\n")
            except:
                output.write(doiX+"\n")


