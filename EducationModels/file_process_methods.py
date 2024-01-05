import os
import tempfile
from langchain.document_loaders import UnstructuredPowerPointLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import UnstructuredPowerPointLoader
from werkzeug.utils import secure_filename
from langchain.document_loaders import UnstructuredWordDocumentLoader


def process_file(file) : 
        temp_path = tempfile.mkdtemp()

        filename = secure_filename(file.filename)

        full_path =  os.path.join(temp_path, filename)

        file.save(full_path)

        return full_path
    
def process_powerpoint(directory_path) : 
    loader = UnstructuredPowerPointLoader(directory_path)
    data = loader.load()
    return data

# # Finsih this tomorrow (new years eve.)
# def process_worddoc(self, directory_path) :     
#     loader = 
    
def powerpoint_translation(powerpoint_file_url : str) : 
    loader = UnstructuredPowerPointLoader(powerpoint_file_url)
    data = loader.load()
    return data

# Input the word document URL, and it will process it into text
def word_document_translation(word_document_file_directory: str):
    loader = UnstructuredWordDocumentLoader(word_document_file_directory)

    data = loader.load()
    print(data)

    # Initialize an empty string to store concatenated content
    combined_content = ""

    for document in data:
        # Concatenate the content of each document
        combined_content += document.page_content + "\n"  # Adding a newline for separation

    # Return the combined content as a single string
    return combined_content

def choose_file_process_type(filetype):
    if filetype == 'pptx':
        return process_powerpoint
    elif filetype == 'docx':
        return word_document_translation
    else:
        raise ValueError(f"Unsupported file type: {filetype}")