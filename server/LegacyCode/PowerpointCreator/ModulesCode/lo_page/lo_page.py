from EducationModels.openai_calls import OpenAI
from EducationModels.PowerpointCreator.ModulesCode.regexing_code import stage_4_content_title_layout_splitter
async def stage_4_lo_page_combined_process(lessonFacts):
        gptAgent = OpenAI()
        temperature = 0.5
        inputPrompt = """I want you to pretend to be a expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable. Using the inputted facts, you are to create a SINGLE powerpoint slide at {SLIDE NUMBER}. Start with a title for the L.O page, by doing 'TITLE : INSERT TITLE HERE', and then 'CONTENT : INSERT THE CONTENT HERE'. 
- Have it follow a standard L.O page outline
- In the content, in no more than 6 bullet points, create the learning objectives for the lesson.
heres an example output for the 'Content' :  
By the end of this presentation, you should be able to:
Appreciate the significance of budgeting and financial planning in personal finance management.     
Identify the different types of investments, including stocks, bonds, and mutual funds.
Understand the functions and benefits of retirement accounts and their role in long-term financial planning.
Differentiate between saving and investing, and comprehend their respective roles in wealth creation.
Understand the implications of tax planning strategies for individual taxpayers in various income brackets.
Here are the lesson facts :
"""  # Your existing prompt
        powerpointSlide = await gptAgent.async_open_ai_gpt4_call(inputPrompt, lessonFacts, temperature)
        splittedPowerpointSlide = stage_4_content_title_layout_splitter(powerpointSlide)
        structured_output = {
            "module": "lo_page",
            "slide": {
                "title": splittedPowerpointSlide[0], # Assuming the title is the first part of the tuple
                "description": splittedPowerpointSlide[1] # Assuming the content/description is the second part of the tuple
            }
        }
        
        # Return the structured output
        return structured_output