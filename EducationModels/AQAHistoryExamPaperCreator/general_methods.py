import PyPDF2
from EducationModels.openai_calls import OpenAI
import json

def extract_page(start_num, end_num, path):
    with open(path, 'rb') as pdfFileObj:
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        pages_text = []

        for page_num in range(start_num, end_num+1):
            pageObj = pdfReader.pages[page_num]
            pages_text.append(pageObj.extract_text())
            
    return pages_text