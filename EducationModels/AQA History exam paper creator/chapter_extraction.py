import PyPDF2

def extract_page(start_num, end_num, path):
    with open(path, 'rb') as pdfFileObj:
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        pages_text = []

        for page_num in range(start_num, end_num+1):
            pageObj = pdfReader.pages[page_num]
            pages_text.append(pageObj.extract_text())
            
    return pages_text


path = "C:\\Users\\david\\Desktop\\AlgoCo\\Private Education Models\\EdukaiPrivateModels\\AQA History 1st sample.pdf"
path2 = "C:\\Users\\david\\Desktop\\AlgoCo\\Private Education Models\\EdukaiPrivateModels\\AQA History 2nd sample.pdf"
print(extract_page(2, 3, path2))