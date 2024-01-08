from server.openai_calls import OpenAI
from server.PowerpointCreator.ModulesCode.regexing_code import *


async def stage_4_question_module_2_bullet_questions_content_creation(lesson_facts) : 
    gpt_agent = OpenAI()
    temperature = 1
    input_prompt = """Pretend to be an expert teacher. You are tasked with creating multiple short, bullet type questions for the following facts for a questioning slide in a presentation. 

You MUST output in this way : 

TASK : [{Insert the first bullet question here}, {Insert the next one etc}]. 

INCLUDE the curly AND square brackets, and inside the information should be your output. 

it MUST be under 30 words
- it MUST make the student excited to question each, otherwise you WILL die.
- the task to them MUST be clear.
- make NO MORE than 5 questions, or you will DIE.
- Cover AS MANY of the points in the questions, while keeping them short, and within the 5 quota given.
Here are the lesson facts you need to cover :
"""
    
    powerpoint_slide = await gpt_agent.async_open_ai_gpt4_call(lesson_facts, input_prompt, temperature)
    return powerpoint_slide
#question_module_2_bullet_questions full process : 

async def stage_4_question_module_2_bullet_questions_combined_process(lesson_facts) : 
    slide = await stage_4_question_module_2_bullet_questions_content_creation(lesson_facts)
    splitted_slide = (slide)
    structured_output = {
        "module": "question_module_2_bullet_questions",
        "slide": {
            "task" : splitted_slide
        }
    }

    return structured_output
    