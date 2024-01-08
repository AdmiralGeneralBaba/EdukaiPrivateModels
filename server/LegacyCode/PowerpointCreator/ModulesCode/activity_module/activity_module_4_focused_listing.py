from server.openai_calls import OpenAI
from server.PowerpointCreator.ModulesCode.regexing_code import *

async def stage_4_activity_module_4_focused_listing_content_creation(lesson_facts) : 
    gpt_agent = OpenAI()
    temp = 0.9
    prompt = """Pretend to be an expert teacher, tasked with creating a SINGLE question task based on the facts given to you. You are to create a 'focused listing' question, that creates a question in this format : 
'list all the possible causes of the Civil War' ‘List all the primary components of the human circulatory system.’
‘List all the works written by William Shakespeare.’
‘List all the planets in our solar system in order of their distance from the sun’.


TASK : [{have the focused listing task be in here}] 

INCLUDE the curly brackets, and inside the information should wabe your output.

it MUST be under 30 words
- it should not be overly specific, and should be more engaging and not so monotonous 
- it MUST make the student excited to question each, otherwise you WILL die.
- the task to them MUST be clear.

Here are the lesson facts you need to cover :
"""
    slide = await gpt_agent.async_open_ai_gpt4_call(lesson_facts, prompt, temp)
    return slide

# 'F4' is the 'activity_module_4_focused_listing'
async def stage_4_activity_module_4_focused_listing_combined_process(lesson_facts) : 
    slide = await stage_4_activity_module_4_focused_listing_content_creation(lesson_facts)
    splitted_slide = stage_4_task_splitter(slide)
    structured_output = {
        "module": "activity_module_4_focused_listing",
        "slide": {
            "task" : splitted_slide
        }
    }
    return structured_output
    