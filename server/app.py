from fastapi import FastAPI, UploadFile, File
import asyncio
import tempfile
import requests
from mcq_creator_v1 import mcq_creator_v1
from flashcard_model_v2 import FlashcardModelV2
from text_processing_v1 import text_fact_transformer_V1
from info_extractor_v5 import InfoExtractorV5
from flask_cors import CORS
import file_process_methods as file_processor
from uvicorn.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
    allow_origins=["*"],  # Specify the allowed origin
    allow_credentials=True,
    allow_methods=["POST", "GET"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/async_text_fact_breakdown/{text}") 
async def async_text_fact_breakdown(text) : 


    if len(text) > 1000000000 : 
        return "too long"
    else : 
        text_facts = await text_fact_transformer_V1(text) # NEED TO FIX THIS
        return (text_facts)

@app.get('/youtube_to_text/') 
async def async_text_fact_breakdown_youtube_url(youtube_url : str) : 
    # directory = request.args.get('directory')
    directory = r"C:\Users\david\Downloads\Youtube"
    info_extractor = InfoExtractorV5()
    text = info_extractor.transcribe_youtube_url(youtube_url, directory)
                   
    if len(text) > 100000 : 
        return "too long"
    else : 
        text_facts = await text_fact_transformer_V1(text) # NEED TO FIX THIS
        return (text_facts)


@app.post('/file_input') 
async def handleFileInput(file : UploadFile = File(...)) : 
    if file :
        path = file_processor.process_file(file)
        print("this is the file name : ", file.filename)
        fileType = file.filename.split('.')[-1] 
        print("this is the file type :  ", fileType)
        process_method = file_processor.choose_file_process_type(fileType)
        data = process_method(path)

        data_processed = await text_fact_transformer_V1(data)
        print(data_processed)
        return (data_processed)
    else : 
        return { 'error ' : 'no file found'}

@app.get('/mcq_creator/{lesson}') 
async def mcq_creator(lesson) : 
    mcq = await mcq_creator_v1(lesson, 1)
    return (mcq)

@app.get('/flashcards/{lesson}')
def flashcard_creator(lesson): 
    # Decoding the URL encoded lesson value
    flashcard_creator = FlashcardModelV2()
    # gpt_type is hard-coded to '1'
    flashcards = flashcard_creator.flashcard_creator_from_raw_facts(lesson, '0')
    return (flashcards)

@app.get('/test/{num}')
def number_printer(num) :
    return num
