from flask import Flask
import requests
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO

app=Flask(__name__)


 
def pdf_from_url_to_txt(data):
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Open the url provided as an argument to the function and read the content
    # Cast to StringIO object
    fp = BytesIO(data)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # password = ""
    # maxpages = 0
    # caching = True
    # pagenos = set()
    for page in PDFPage.get_pages(fp,
                                #   pagenos,
                                #   maxpages=maxpages,
                                #   password=password,
                                #   caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


@app.route('/')
def hello(pdfpath):
    html = "把pdf文件的地址加在这个地址后面。"
    return html

@app.route('/<path:pdfpath>')
def hello(pdfpath):
    pdfpath = pdfpath.split(':/',1)
    pdfpath = "http://"+pdfpath[1]
    print(pdfpath,flush=True)
    data = requests.get(pdfpath).content
    html = pdf_from_url_to_txt(data)
    return html

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True,port='80')