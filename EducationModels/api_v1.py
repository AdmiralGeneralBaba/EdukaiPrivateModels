import sys
import os
import asyncio
import tempfile
from flask import Flask, request, jsonify
import requests
from aqa_english_language_paper_1_v1 import aqa_english_language_paper_1_generator
from yearly_plan_ai_models_v2 import YearlyPlanCreatorV2
from yearly_plan_ai_models_v3 import YearlyPlanCreatorV3
from homework_creator_v1 import homeworkCreatorsV1
from powerpoint_creator_v5 import PowerpointCreatorV5
from mcq_creator_v1 import McqCreatorV1
from flashcard_model_v2 import FlashcardModelV2
from text_processing_v1 import text_fact_transformer_V1
import urllib

app = Flask(__name__)
app.debug = True

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

@app.route('/yearly_plan_creator/')
def yearly_plan():
    pdf_url = request.args.get('pdf_url')
    tmp_filepath = fetch_and_process_pdf(pdf_url)

    if not tmp_filepath:
        return jsonify({"error": "Invalid URL or not a PDF"}), 400

    # Process the PDF
    yearly_planner = YearlyPlanCreatorV2()
    yearly_plan = yearly_planner.yearly_plan_facts_per_lesson_pdf_input_only(tmp_filepath)

    # Once processing is done, delete the temporary file
    os.remove(tmp_filepath)

    # Return the result
    return jsonify(yearly_plan)

@app.route('/async_yearly_plan_creator/')
async def async_yearly_plan():
    pdf_url = request.args.get('pdf_url')
    tmp_filepath = fetch_and_process_pdf(pdf_url)

    if not tmp_filepath:
        return jsonify({"error": "Invalid URL or not a PDF"}), 400

    # Process the PDF
    yearly_planner = YearlyPlanCreatorV3()
    yearly_plan = await yearly_planner.yearly_plan_facts_per_lesson_pdf_input_only(tmp_filepath)

    # Once processing is done, delete the temporary file
    os.remove(tmp_filepath)

    # Return the result
    return jsonify(yearly_plan)



@app.route('/async_text_fact_breakdown/<path:text>') 
async def async_text_fact_breakdown(text) : 

    if len(text) > 10000000 : 
        return "too long"
    else : 
        text_facts = await text_fact_transformer_V1(text) # NEED TO FIX THIS
        return jsonify(text_facts)


@app.route('/aqa_english_language_paper_1/')
def create_exam_paper():
    pdf_url = request.args.get('pdf_url')
    book_title = request.args.get('book_title')
    book_type = request.args.get('book_type')
    
    tmp_filepath = fetch_and_process_pdf(pdf_url)
    if not tmp_filepath:
        return jsonify({"error": "Invalid URL or not a PDF"}), 400

    exam_paper = aqa_english_language_paper_1_generator(tmp_filepath, book_title, book_type)

    # Once processing is done, delete the temporary file
    os.remove(tmp_filepath)

    return jsonify(exam_paper)

@app.route('/homework_creator/<path:lesson>')
def homework_creation(lesson) : 
    homework_creator = homeworkCreatorsV1()
    lesson_homework = homework_creator.homework_creator_template_one(lesson, 1)
    return jsonify(lesson_homework)

@app.route('/powerpoint_creator/<path:lesson>')
def powerpoint_creator(lesson):
    powerpoint_creator = PowerpointCreatorV5()
    powerpoint = powerpoint_creator.stage_6_create_powerpoint(lesson)
    return jsonify(powerpoint)

@app.route('/mcq_creator/<path:lesson>') 
def mcq_creator(lesson) : 
    mcq_creator = McqCreatorV1()
    mcq = mcq_creator.mcq_creator_v1(lesson, 1)
    return jsonify(mcq)

@app.route('/flashcards/<path:lesson>')
def flashcard_creator(lesson): 
    # Decoding the URL encoded lesson value
    flashcard_creator = FlashcardModelV2()
    # gpt_type is hard-coded to '1'
    flashcards = flashcard_creator.flashcard_creator_from_raw_facts(lesson, '1')
    return jsonify(flashcards)

# In the future, have a endpoint for each exam board 
#inputs : pdfFile, titleOfBook, bookType

@app.route('/lesson_test/<lesson>')
def print_lesson(lesson) : 
    return lesson
@app.route('/test/<num>')
def number_printer(num) :
    return num


if __name__  == '__main__' :
    app.run()
# Change this API where needed, for it to be either A. accessible on the local network by all devices, or B. accessible to all devices anywhere : 
# Here are the steps :


# #Local Network Accessibility:

# Simplicity: Easy
# Steps:
# Bind your Flask app to 0.0.0.0 (i.e., app.run(host='0.0.0.0')).
# Determine your computer's local IP address.
# Share the IP address and port with team members. They can access the Flask app using http://YOUR_LOCAL_IP:PORT/.
# External Network Accessibility:

# Simplicity: Moderate (can vary based on router and ISP)

# Steps:

# Configure port forwarding on your router. This involves logging into your router's admin interface and setting it to forward external requests on a particular port to your computer's IP address and the port your Flask app is running on.
# Determine your public IP address (e.g., using "WhatIsMyIP").
# Share the public IP address and port with external users. They can access the Flask app using http://YOUR_PUBLIC_IP:PORT/.