import fitz
import PyPDF2
import os
from pytesseract import pytesseract
from PIL import Image
pytesseract.tesseract_cmd="C:/Program Files/Tesseract-OCR/tesseract.exe"
def add(d,i,obj):
    for item in d:
        if(d[item]):
            obj.addPage(i)
            return
def analysis(dir,obj):
    d={"balance sheet":False,"profit and loss":False,"cash flow":False,"notes":False}
    f=open(f"./files/{dir}","rb")
    other=PyPDF2.PdfFileReader(f)
    pdf_file=fitz.open(f"./files/{dir}")
    for page_index in range(10,(len(pdf_file))):
        page=pdf_file[page_index]
        image_list=page.get_images()
        if(len(image_list)==1):
            xref=image_list[0][0]
            base_image=pdf_file.extract_image(xref)
            img_bytes=base_image["image"]
            f=open(f"image.jpg",'wb')
            f.write(img_bytes)
            f.close()
            img=Image.open("image.jpg")
            text=pytesseract.image_to_string(img)
        else:
            text=other.getPage(page_index).extractText()
            # print(text.split())
        text=" ".join(text.replace("\n"," ").lower().split())
        t1=text.find("balance sheet as at")
        t2=text.find("statement of profit and loss for the year")
        t3=text.find("cash flow statement for the year")
        t4=text.find("note")
        if((t1<=20 and t1!=-1)  or "balance sheet asat" in text):
            d["balance sheet"]=True
        elif( (t2<=20 and t2!=-1) or "statement ofprofit and loss for the year" in text):
            d["profit and loss"]=True
            d["balance sheet"]=False
        elif((t3<=20 and t3!=-1) or "cash flow statement" in text):
            d["profit and loss"]=False
            d["cash flow"]=True
        elif((t4<=20 and t4!=-1) or "notes" in text):
            d["cash flow"]=False
            d["notes"]=True
        else:
            pass
        add(d,other.getPage(page_index),obj)

list_dir=os.listdir("./files/")
try:
    os.makedirs("./outputfiles")
except:
    pass
files={}
for dir in list_dir:
    try:
        company=dir.rsplit(maxsplit=1)[0]
        if(company not in files):
            f1=PyPDF2.PdfFileWriter()
            files[company]=f1
        analysis(dir,files[company])
    except Exception as e:
        print(e)

for company in files:
    try:
        f=open(f"./outputfiles/{company}.pdf","wb")
        files[company].write(f)
        f.close()
    except Exception as e :
        print(e)
try:
    os.remove("./image.jpg")
except:
    pass