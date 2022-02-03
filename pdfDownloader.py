import requests as req
from bs4 import BeautifulSoup as soup
import os

class Downloder:

    def fetchUrlContent(self,url):
        try:
            res=req.get(url)
            res=res.content
            return res
        except Exception as e:
            print(f"Some Error Occour : {e}")

    def parseHtml(self,content):
        try:
            html = soup(content, "html.parser")
            return html
        except Exception as e:
            print(e)

    def downloadFile(self,file_url,name,dir="."):
        try:

            if(not os.path.isdir(f"{dir}/files/")):
                os.makedirs(f"{dir}/files")

            res=req.get(file_url,stream=True,allow_redirects=False)

            f=open(f"{dir}/files/{name}","wb")
            for chunk in res.iter_content(chunk_size=1024):
                if(chunk):
                    f.write(chunk)
            f.close()

            print('File SuccessFull Download')

        except Exception as e:
            print(f"Some Error Occour : {e}")


