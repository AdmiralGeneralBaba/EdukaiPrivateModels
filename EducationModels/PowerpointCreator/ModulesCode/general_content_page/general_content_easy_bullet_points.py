from EducationModels.openai_calls import OpenAI
import re
from regexing_code import extract_content_TITLE_CONTENT_PICTURE



def create_input_prompt(powerpoint_plan, slide_number) : 
    prompt = """I want you to pretend to be an expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable. Based on this lesson description and the inputted facts, you are to create a SINGLE powerpoint slide  based on the facts given. provided will also be the powerpoint plan for context. 

Start with a UNIQUE, INTERESTING title, by doing 
TITLE {INSERT TITLE HERE}, CONTENT {INSERT THE CONTENT HERE}, followed by a search term for a picture to go along the facts as best you can, PICTURE {INSERT PICTURE QUERY HERE}. 

Tips for content:
- Take into account the context of the overall lesson. 
- Use these facts ONLY- DO NOT make up information/facts
- DO NOT leave any space for placeholder (e.g for an image) - the powerpoint must be a finished product.
- State the facts in a way that is easy for them to understand, but is not long-winded. 

An example output would be : 
TITLE {title text here, with the curly brackets}, 
CONTENT {content text here, with the curly brackets}, 
PICTURE {picture text here, with the curly brackets}

Here is the powerpoint plan : 

""" + "{ " f"{powerpoint_plan}" + "}" + """ 

The current slide number is """ + "{ " f"{slide_number}" + "}" + """ 

and here are the facts : """
    return prompt


def general_content_easy_bullet_points_content_creation(input_prompt, slide_fact) : 
    llm = OpenAI()
    temp = 1
    content_output = llm.open_ai_gpt4_call(slide_fact, input_prompt, temp)
    return content_output

def general_content_easy_bullet_points_final_method(slide_facts, powerpoint_plan, slide_number) :
    prompt = create_input_prompt(powerpoint_plan,slide_number )
    content = general_content_easy_bullet_points_content_creation(prompt, slide_facts)
    extracted_content = extract_content_TITLE_CONTENT_PICTURE(content) 

    structured_output = {
        "module" : "general_content_easy_bullet_points",
        "slide" : {
            "title" : extracted_content["TITLE"],
            "description" : extracted_content["CONTENT"],
            "image_caption" : extracted_content["PICTURE"]
        }
    }
    return structured_output




  