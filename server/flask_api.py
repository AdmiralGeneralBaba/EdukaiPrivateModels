import os
import asyncio
import tempfile
from flask import Flask, request, jsonify
import requests
from mcq_creator_v1 import mcq_creator_v1
from flashcard_model_v2 import FlashcardModelV2
from text_processing_v1 import text_fact_transformer_V1
from info_extractor_v5 import InfoExtractorV5
from flask_cors import CORS
import file_process_methods as file_processor
from uvicorn.middleware.wsgi import WSGIMiddleware


app = Flask(__name__)
CORS(app)
#Need to find out how to take in a PDF input for this app.route path - perhaps it needs to access a database input path? search on this :7
 
#query parameter is '?pdf_url' 
def fetch_and_process_pdf(pdf_url):
    # Fetch the PDF from the URL
    response = requests.get(pdf_url)
    
    # Check if the response is a PDF (based on Content-Type header)
    if 'application/pdf' not in response.headers.get('Content-Type', ''):
        return None


    # Save the content to a temporary file
    fd, tmp_filepath = tempfile.mkstemp(suffix=".pdf")
    with os.fdopen(fd, 'wb') as tmp:
        tmp.write(response.content)

    return tmp_filepath

@app.route('/async_text_fact_breakdown/<path:text>') 
async def async_text_fact_breakdown(text) : 

    if len(text) > 1000000000 : 
        return "too long"
    else : 
        text_facts = await text_fact_transformer_V1(text) # NEED TO FIX THIS
        return jsonify(text_facts)

@app.route('/youtube_to_text/') 
async def async_text_fact_breakdown_youtube_url() : 
    # directory = request.args.get('directory')
    directory = r"C:\Users\david\Downloads\Youtube"
    youtube_url = request.args.get('youtube_url')
    info_extractor = InfoExtractorV5()
    text = info_extractor.transcribe_youtube_url(youtube_url, directory)
                   
    if len(text) > 100000 : 
        return "too long"
    else : 
        text_facts = await text_fact_transformer_V1(text) # NEED TO FIX THIS
        return jsonify(text_facts)


@app.route('/file_input', methods=['POST']) 
async def handleFileInput() : 
    if 'file' in request.files : 
        file = request.files['file']
        path = file_processor.process_file(file)
        print("this is the file name : ", file.filename)
        fileType = file.filename.split('.')[-1] 
        print("this is the file type :  ", fileType)
        process_method = file_processor.choose_file_process_type(fileType)
        data = process_method(path)

        data_processed = await text_fact_transformer_V1(data)
        return jsonify(data_processed)
    else : 
        return { 'error ' : 'no file found'}

@app.route('/mcq_creator/<path:lesson>') 
async def mcq_creator(lesson) : 
    mcq = await mcq_creator_v1(lesson, 1)
    return jsonify(mcq)

@app.route('/flashcards/<path:lesson>')
def flashcard_creator(lesson): 
    # Decoding the URL encoded lesson value
    flashcard_creator = FlashcardModelV2()
    # gpt_type is hard-coded to '1'
    flashcards = flashcard_creator.flashcard_creator_from_raw_facts(lesson, '0')
    return jsonify(flashcards)


@app.route('/test/<num>')
def number_printer(num) :
    return num


asgi_app = WSGIMiddleware(app)