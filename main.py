import pdfDownloader

download=pdfDownloader.Downloder()

url="https://www.screener.in/company/526727/#documents"

html=download.parseHtml(download.fetchUrlContent(url))

main_box=html.find_all("div",class_="annual-reports")[0]


f=open("annualReports.html","w")

f.write(str(main_box))

f.close()