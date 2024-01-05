from EducationModels.PowerpointCreator.ModulesCode.regexing_code import *
from EducationModels.openai_calls import OpenAI

async def stage_4_title_page_combined_process(lessonFacts):
    gptAgent = OpenAI()
    temperature = 0.7
    inputPrompt = """I want you to pretend to be a expert teacher, making a perfectly constructed first powerpoint slide based on the inputted lesson facts. You are to create a perfect Title and subtitle. Put the title in 'TITLE : INSERT TITLE HERE ' then 'SUBTITLE : INSERT SUBTITLE HERE' 
Here are the lesson facts : """ # Your existing prompt
    titlePowerpoint = await gptAgent.async_open_ai_gpt4_call(inputPrompt, lessonFacts, temperature)

    print(titlePowerpoint)
    splitTitlePowerpoint = stage_4_title_subtitle_layout_spliter(titlePowerpoint)
    # Creating the structured output to match the desired format
    structured_output = {
        "module": "title_page",
        "slide": {
            "title": splitTitlePowerpoint[0], # Assuming the title is the first part of the tuple
            "subtitle": splitTitlePowerpoint[1] # Assuming the subtitle/description is the second part of the tuple
        }
    }

    # Return the structured output
    return structured_output