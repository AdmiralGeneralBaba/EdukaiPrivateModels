from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import (
    OpenAIWhisperParser
)
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

# set a flag to switch between local and remote parsing
# change this to True if you want to use local parsing
local = False
save_dir = "C:/Users/david"

#Input is a string as to not cause confusion on the input.
def transcribe_youtube_url(youtube_url :str):
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

url = "https://www.youtube.com/watch?v=IAyE9hyttq4" 
test = transcribe_youtube_url(url)

print(test)