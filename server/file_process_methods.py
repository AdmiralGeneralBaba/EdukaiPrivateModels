import os
import shutil
import tempfile
from langchain.document_loaders import UnstructuredPowerPointLoader, Docx2txtLoader, UnstructuredWordDocumentLoader
from fastapi import UploadFile

def process_file(file: UploadFile):
    temp_path = tempfile.mkdtemp()
    filename = os.path.join(temp_path, file.filename)

    # Save the uploaded file
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return filename

def process_powerpoint(directory_path): 
    loader = UnstructuredPowerPointLoader(directory_path)
    data = loader.load()

    combined_content = ""
    for document in data:
        combined_content += document.page_content + "\n"
    
    return combined_content



def word_document_translation(word_document_file_directory: str):
    loader = UnstructuredWordDocumentLoader(word_document_file_directory)
    data = loader.load()
    
    combined_content = ""
    for document in data:
        combined_content += document.page_content + "\n"
    
    return combined_content

def choose_file_process_type(filetype):
    if filetype == 'pptx':
        return process_powerpoint
    elif filetype == 'docx':
        return word_document_translation
    else:
        raise ValueError(f"Unsupported file type: {filetype}")
