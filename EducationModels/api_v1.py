import sys
import os
import tempfile
from flask import Flask, request, jsonify
import requests
from yearly_plan_ai_models_v2 import YearlyPlanCreatorV2
from homework_creator_v1 import homeworkCreatorsV1
from powerpoint_creator_v4 import PowerpointCreatorV4
from mcq_creator_v1 import McqCreatorV1
from flashcard_model_v2 import FlashcardModelV2

app = Flask(__name__)
app.debug = True

#Need to find out how to take in a PDF input for this app.route path - perhaps it needs to access a database input path? search on this :7
 
#query parameter is '?pdf_url' 
@app.route('/yearly_plan_creator/')
def yearly_plan():
    # Retrieve the URL from the query parameters
    pdf_url = request.args.get('pdf_url')

    # Fetch the PDF from the URL
    response = requests.get(pdf_url)
    
    # Check if the response is a PDF (based on Content-Type header)
    if 'application/pdf' not in response.headers.get('Content-Type', ''):
        return jsonify({"error": "Invalid URL or not a PDF"}), 400
    
    # Save the content to a temporary file
    fd, tmp_filepath = tempfile.mkstemp(suffix=".pdf")
    with os.fdopen(fd, 'wb') as tmp:
        tmp.write(response.content)

    # Process the PDF
    yearly_planner = YearlyPlanCreatorV2()
    yearly_plan = yearly_planner.yearly_plan_facts_per_lesson_pdf_input_only(tmp_filepath)

    # Once processing is done, delete the temporary file
    os.remove(tmp_filepath)

    # Return the result
    return jsonify(yearly_plan)
@app.route('/homework_creator/<lesson>')
def homework_creation(lesson) : 
    homework_creator = homeworkCreatorsV1()
    lesson_homework = homework_creator.homework_creator_template_one(lesson, 1)
    return jsonify(lesson_homework)

@app.route('/powerpoint_creator/<lesson>')
def powerpoint_creator(lesson):
    powerpoint_creator = PowerpointCreatorV4()
    powerpoint = powerpoint_creator.stage_6_create_powerpoint(lesson)
    return jsonify(powerpoint)

@app.route('/mcq_creator/<lesson>/<gpt_type>') 
def mcq_creator(lesson, gpt_type) : 
    mcq_creator = McqCreatorV1()
    mcq = mcq_creator.mcq_creator_v1(lesson, gpt_type)
    return jsonify(mcq)

@app.route('/flashcards/<lesson>/<gpt_type>') 
def flashcard_creator(lesson, gpt_type) : 
    flashcard_creator = FlashcardModelV2()
    flashcards = flashcard_creator.flashcard_creator_from_raw_facts(lesson, gpt_type)
    return jsonify(flashcards)


@app.route('/lesson_test/<lesson>')
def print_lesson(lesson) : 
    return lesson
@app.route('/test/<num>')
def number_printer(num) :
    return num


if __name__  == '__main__' :
    app.run()
