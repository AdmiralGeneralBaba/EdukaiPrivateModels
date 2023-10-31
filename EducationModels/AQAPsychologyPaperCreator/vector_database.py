from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

def vectorise_pdf(url : str, k) : 
    embedding = OpenAIEmbeddings()
    loader = PyPDFLoader(url)
    pages = loader.load_and_split()
    db = Chroma.from_documents(pages, embedding, k=k)
    return db

