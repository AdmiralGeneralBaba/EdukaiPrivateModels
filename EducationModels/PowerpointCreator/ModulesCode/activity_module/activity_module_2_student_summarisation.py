from EducationModels.openai_calls import OpenAI
from EducationModels.PowerpointCreator.ModulesCode.regexing_code import *


async def stage_4_activity_module_2_student_summarisation_slide_content_creation(lesson_facts) :
    gpt_agent = OpenAI()
    temp = 0.5
    prompt = """ I want you to pretend to be an expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable. Based on this lesson description, and the inputted facts, you are to create a SINGLE powerpoint slide based on the facts given. Assume that everything in the lesson description is covered in the other slides. Your job is to create a powerpoint slide that takes into account the slides BEFORE your slide number and nothing else.

You are to create a slide asking students to summarize about what they have learnt. Your output should be EXACTLY like this structure : 
TASK : [{have the summarisation task be inside here}]. INCLUDE the curly brackets, and inside the information should be your output.

it MUST be under 30 words
- it should not be overly specific, and should be more engaging and not so monotonous 
- it MUST make the student excited to brainstorm, otherwise you will die.
- the task to them MUST be clear.
Here are the lesson facts you need to cover:
"""

    slide = await gpt_agent.async_open_ai_gpt4_call(lesson_facts, prompt, temp)
    return slide

#'F2' is the 'activity_module_2_student_summarisation' 
async def stage_4_activity_module_2_student_summarisation_combined_process(lesson_facts) :
    slide = await stage_4_activity_module_2_student_summarisation_slide_content_creation(lesson_facts)
    splitted_slide = stage_4_task_splitter(slide)
    structured_output = {
        "module": "activity_module_2_student_summarisation",
        "slide": {
            "task" : splitted_slide
        }
    }
    return structured_output