from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import (
    OpenAIWhisperParser
)
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain.document_loaders import UnstructuredPowerPointLoader
from langchain.document_loaders import Docx2txtLoader
from docx import Document


# set a flag to switch between local and remote parsing
# change this to True if you want to use local parsing
local = False

# 
save_dir = "C:/Users/david"

#Input is a string as to not cause confusion on the input.
def transcribe_youtube_url(youtube_url :str, save_dir):
    # Check if youtube_url is a string
    if not isinstance(youtube_url, str):
        raise ValueError("The input must be a string representing a YouTube URL")
    url_array = [youtube_url]
    loader = GenericLoader(YoutubeAudioLoader(url_array, save_dir), OpenAIWhisperParser())
    docs = loader.load()
    print(len(docs))
    combined_docs = [doc.page_content for doc in docs]
    text = " ".join(combined_docs)
    
    return text

# Input the powerpoint URL - Need to have this stored on the cloud, then use the address as the input for this method : 
def powerpoint_translation(powerpoint_file_url : str) : 
    loader = UnstructuredPowerPointLoader(powerpoint_file_url)
    data = loader.load()
    return data

def word_document_translation(word_document_file_directory : str) : 
    loader = Docx2txtLoader(word_document_file_directory)
    data = loader.load()
    return data


# url = "https://www.youtube.com/watch?v=IAyE9hyttq4" 
# pp_url = "C:\\Users\\david\\Downloads\\make-it-stick-study-strategies-for-retention.pptx"

# word_path = "C:\Users\david\Desktop"



# test = powerpoint_translation(pp_url)  

word_path = "C:\\Users\\david\Desktop\\business-model-canvas_test.docx"

test = word_document_translation(word_path)
print(test)
