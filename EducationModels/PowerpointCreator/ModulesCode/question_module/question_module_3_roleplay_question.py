from EducationModels.openai_calls import OpenAI
from regexing_code import *
import re

async def stage_4_question_module_3_roleplay_question_slide_content_creation(lesson_facts) : 
    gpt_agent = OpenAI()
    temperature = 1
    prompt = """Pretend to be an expert teacher. You are tasked with creating a roleplay scenario to create questions for. For these facts, you will create and put the scenario in the 'ROLEPLAY' value, then in the 'TASK' section you will insert the roleplay questions in the format given. in the 'PICTURE' section, you must make a PERFECT google search query to get an image that will help immerse them INTO the roleplay part you have given them.
You MUST output in this way : 

ROLEPLAY : [{Insert a short, brief exciting description of the roleplay you will base the questions on, to engage students}]  
TASK : [{Insert the roleplay question here}, {Insert the second roleplay question here etc}] 
PICTURE : [{Insert image to get them in the mood of the roleplay you have created.}]

INCLUDE the curly AND square brackets, and inside the information should be your output. 

it MUST be under 30 words
- it MUST make the student excited to question each, otherwise you WILL die.
- the task to them MUST be clear.
- make NO MORE than 5 questions, or you will DIE.
- Cover AS MANY of the points in the questions, while keeping them short, and within the 5 quota given.
- DO NOT stretch the students too hard; it MUST be achievable with the facts given.
Here are the lesson facts you need to cover :
"""

    slide = await gpt_agent.async_open_ai_gpt4_call(lesson_facts, prompt, temperature)
    return slide 
#splits up the inputted slide into values within the dictionary of 'slide_content'
def stage_4_question_module_3_roleplay_question_regex_split(slide): 
    roleplay = stage_4_regex_roleplay(slide)
    task = stage_4_regex_task(slide)
    picture = stage_4_regex_picture(slide)

    slide = {
        "roleplay": roleplay, 
        "task": task,
        "picture": picture
    }
    
    return slide
# this is the question_module_3_roleplay_questions submodule
async def stage_4_question_module_3_roleplay_question_combine_process(lesson_facts) : 
    
    slide = await stage_4_question_module_3_roleplay_question_slide_content_creation(lesson_facts)
    slide_dict = stage_4_question_module_3_roleplay_question_regex_split(slide)
    
    structured_output = {
        "module": "question_module_3_roleplay_question",
        "slide": slide_dict
    }
    return structured_output