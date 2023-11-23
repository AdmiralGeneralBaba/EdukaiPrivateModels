from EducationModels.openai_calls import OpenAI
from regexing_code import *

async def stage_4_activity_module_3_qa_pairs_slide_content_creation(lesson_facts) :
    gpt_agent = OpenAI()
    temp = 0.8
    prompt = """ I want you to pretend to be an expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable. Based on this lesson description, and the inputted facts, you are to create a SINGLE powerpoint slide based on the facts given. Assume that everything in the lesson description is covered in the other slides. Your job is to create a powerpoint slide that takes into account the slides BEFORE your slide number and nothing else.

You are to create a slide asking students to pair up, and for them to ask each other questions to each other and to answer the questions from their partner. Have it be a game, almost trying to catch them out on certain sections. Include an example with your output.  Your output should be EXACTLY like this structure : 
TASK : [{have the brainstorming task be inside here}]. EXAMPLE : [{Have the example inside here, in this format: Q: "QUESTION HERE" A"ANSWER HERE"}]

INCLUDE the curly brackets, and inside the information should be your output.

it MUST be under 30 words
- it should not be overly specific, and should be more engaging and not so monotonous 
- it MUST make the student excited to question each, otherwise you WILL die.
- the task to them MUST be clear.

Here are the lesson facts you need to cover: 

"""

    slide = await gpt_agent.async_open_ai_gpt4_call(lesson_facts, prompt, temp)
    return slide
def stage_4_activity_module_3_qa_pairs_slide_regex_split(slide) : 
    task = stage_4_task_splitter(slide)
    example = stage_4_regex_example(slide)

    slide = {
        "task" : task,
        "example" : example
    }
    return slide

async def stage_4_activity_module_3_qa_pairs_slide_combined_process(lesson_facts) : 
    slide = await stage_4_activity_module_3_qa_pairs_slide_content_creation(lesson_facts)
    slide_dict = stage_4_activity_module_3_qa_pairs_slide_regex_split(slide)
    
    structured_output = {
        "module": "activity_module_3_qa_pairs",
        "slide": slide_dict
    }
    return structured_output