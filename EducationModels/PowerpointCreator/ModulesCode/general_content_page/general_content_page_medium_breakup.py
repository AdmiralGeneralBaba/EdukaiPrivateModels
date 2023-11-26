from EducationModels.openai_calls import OpenAI
import re
from regexing_code import extract_content_TITLE_CONTENT_PICTURE
from regexing_code import stage_4_replace_fact_numbers_with_text
def extract_data_v2(text):
    # Define the regex patterns for TITLE, CONTENT, and PICTURE with optional spaces
    title_pattern = r"TITLE\s*\{(.*?)\}"
    content_pattern = r"CONTENT\s*\{(.*?)\}"
    picture_pattern = r"PICTURE\s*\{(.*?)\}"

    # Extract the text using the patterns
    title_text = re.search(title_pattern, text)
    content_text = re.search(content_pattern, text)
    picture_text = re.search(picture_pattern, text)

    # Prepare the dictionary to return
    data_dict = {
        "TITLE": title_text.group(1) if title_text else None,
        "CONTENT": content_text.group(1) if content_text else None,
        "PICTURE": picture_text.group(1) if picture_text else None
    }

    return data_dict

def create_input_prompt(powerpoint_plan : str, fact_groupings_with_facts : str) : 
    prompt = """I want you to pretend to be an expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable and understandable.
 
You will be given the powerpoint plan for the lesson, the lesson description, as well as the fact you will explain. You are to create a single powerpoint slide, explaining one specific fact for one sub-topic being taught that will be provided to. In this sub topic, there are a bunch of facts that relate to each other that will be given to you for context. You are to ONLY explain the given fact and nothing else.

In your output, you are to give a title, content both stating + explaining the fact in however much detail you think is needed to understand the topic, and a picture query search term to help the student understand the topic better.

your output MUST look like this : 

TITLE : {INSERT TITLE FOR THE CONCEPT HERE, WITH THE CURLY BRACKETS}
CONTENT : {INSERT CONTENT HERE WITH THE CURLY BRACKETS} 
PICTURE : {INSERT SEARCH TERM TO SEARCH UP TO FIND THE PERFECT PICTURE TO AID A STUDENT'S UNDERSTANDING}

Here is the powerpoint plan :  """ + "{ " f"{powerpoint_plan}" + "}" + """ 

Here are the facts for your sub-topic : """ + "{ " f"{fact_groupings_with_facts}" + "}" + """ 

After stating the below fact in an easy-to-understand way, explain it in the most concise and efficient way.

Here is the fact you will explain : """
    return prompt


def general_content_page_medium_breakup_content_creation(input_prompt, slide_fact) : 
    llm = OpenAI()
    temp = 1
    content_output = llm.open_ai_gpt4_call(slide_fact, input_prompt, temp)
    return content_output

def general_content_page_medium_breakup_final_method(slide_facts, fact_groupings, slide_fact, powerpoint_plan) :
    # inclues the facts as they are instead of just numbers
    fact_groupings_input = stage_4_replace_fact_numbers_with_text(fact_groupings, slide_facts)

    #creates the prompt for the content creation stage
    input_prompt = create_input_prompt(powerpoint_plan, fact_groupings_input)

    #creates the content : 
    content = general_content_page_medium_breakup_content_creation(input_prompt, slide_fact)

    # extracts the content and puts it in a dictionary : 
    extracted_content = extract_content_TITLE_CONTENT_PICTURE(content) 

    #puts that into the structured output here : 
    structured_output = {
        "module" : "general_content_page_medium_breakup",
        "slide" : {
            "title" : extracted_content["TITLE"],
            "description" : extracted_content["CONTENT"],
            "image_caption" : extracted_content["PICTURE"]
        }
    }
    return structured_output




  