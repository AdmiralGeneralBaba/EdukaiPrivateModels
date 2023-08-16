from flask import Flask, jsonify
from EducationModels.yearly_plan_ai_models_v2 import YearlyPlanCreatorV2
from EducationModels.homework_creator_v1 import homeworkCreatorsV1
from EducationModels.powerpoint_creator_v4 import PowerpointCreatorV4
from EducationModels.mcq_creator_v1 import McqCreatorV1
from EducationModels.flashcard_model_v2 import FlashcardModelV2
app = Flask(__name__)
app.debug = True

@app.route('/yearly_plan_creator/<path>')
def yearly_plan(path) : 
    yearly_planner = YearlyPlanCreatorV2()
    yearly_plan = yearly_planner.yearly_plan_facts_per_lesson_pdf_input_only(path)
    return yearly_plan 

@app.route('/homework_creator/<lesson>')
def homework_creation(lesson) : 
    homework_creator = homeworkCreatorsV1()
    lesson_homework = homework_creator.homework_creator_generic(lesson)
    return jsonify(lesson_homework)
@app.route('/powerpoint_creator/<lesson>')
def powerpoint_creator(lesson):
    powerpoint_creator = PowerpointCreatorV4()
    powerpoint_creator.stage_6_create_powerpoint(lesson)
    return jsonify(powerpoint_creator)
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



@app.route('/test/<num>')
def number_printer(num) :
    print(num)

if __name__  == '__main__' :
    app.run()
