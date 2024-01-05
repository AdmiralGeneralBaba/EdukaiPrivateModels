from EducationModels.openai_calls import OpenAI
from EducationModels.PowerpointCreator.ModulesCode.regexing_code import *
async def stage_4_ending_slide_combine_process(lessonFacts):
    gptAgent = OpenAI()
    temperature = 0.
    inputPrompt = """I want you to pretend to be a expert teacher, making a perfectly constructed FINAL powerpoint slide for your students, so that it is easily readable. Using the inputted facts, you are to create a SINGLE powerpoint slide. Start with a title for the Ending slide, by doing 'TITLE : INSERT TITLE HERE', and then 'CONTENT : INSERT THE CONTENT HERE'. 
- Have it follow a standard ending slide structure.
- In the content, keep it brief and short, about what the WHOLE lesson was about in an engaging, fun way for students.
- It should wrap up what they learnt, and be a conclusion for the students.
Here are the lesson facts :
"""
    powerpointSlide = await gptAgent.async_open_ai_gpt4_call(inputPrompt, lessonFacts, temperature)
    splittedPowerpointSlide = stage_4_content_title_layout_splitter(powerpointSlide)

    # Formatting the output as a dictionary
    structured_output = {
        "module": "ending_slide",
        "slide": {
            "title": splittedPowerpointSlide[0],  # Assuming the title is the first part of the tuple
            "description": splittedPowerpointSlide[1]  # Assuming the content/description is the second part of the tuple
        }
    }

    return structured_output