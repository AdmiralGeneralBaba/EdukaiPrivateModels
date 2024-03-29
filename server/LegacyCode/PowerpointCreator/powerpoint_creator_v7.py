import asyncio

from server.openai_calls import OpenAI
import re
from PowerpointCreator.PowerpointPlanCode.powerpoint_plan_creator_v7 import stage_3_powerpoint_plan_creator
from PowerpointCreator.ModulesCode.title_page.title_page import *
from PowerpointCreator.ModulesCode.ending_slide.ending_slide import *
from PowerpointCreator.ModulesCode.lo_page.lo_page import *
from PowerpointCreator.ModulesCode.question_module.question_module_2_bullet_questions import *
from PowerpointCreator.ModulesCode.question_module.question_module_3_roleplay_question import *

from PowerpointCreator.ModulesCode.activity_module.activity_module_1_brainstorming import *
from PowerpointCreator.ModulesCode.activity_module.activity_module_2_student_summarisation import *
from PowerpointCreator.ModulesCode.activity_module.activity_module_3_qa_pairs import *
from PowerpointCreator.ModulesCode.activity_module.activity_module_4_focused_listing import *
from PowerpointCreator.ModulesCode.general_content_page.general_content_page_hard_breakup import general_content_page_hard_breakup_implementation_method
from PowerpointCreator.ModulesCode.general_content_page.general_content_page_medium_breakup import general_content_page_medium_breakup_final_method_looping
from PowerpointCreator.ModulesCode.general_content_page.general_content_easy_bullet_points import general_content_easy_bullet_points_final_method

#     Fixed stages for a single lesson :
#################    FIXED STAGES FOR EVERY LESSON/POWERPOINT:  #####################

def stage_3_lesson_description(numberedFacts) : 
    gptAgent = OpenAI()
    stage3Temp = 0.49
    stage3Prompt = """These facts are included for a lesson. Summarise these facts into one,  brief line, outlining the lesson."""
    lessonDescription = gptAgent.open_ai_gpt4_call(numberedFacts, stage3Prompt, stage3Temp)
    return lessonDescription
def stage_3_slides_powerpoint_extractor(powerpoint_plan):
    # Match either a double newline or the end of the string
    powerpoint_slides = re.findall(r'(POWERPOINT \d+ : .+?)(?:\n\n|$)', powerpoint_plan, re.DOTALL)
    return powerpoint_slides




#############     MODULE GENERIC CODE:        ###############
# Looping stages 
#Extracts the powerpoint individual slide plans, and the total amount of slides for the current powerpoint

#Extracts the fact numbers from the optimum grouping of a single powerpoint slide 
def stage_4_extract_values_from_braces(substring: str):
    # Extract only numbers within curly braces from the given substring
    regex_pattern = r'\{(\d+(?:, \d+)*)\}'
    return re.findall(regex_pattern, substring)

def stage_4_facts_extraction_from_choices(slide_plan, factsString):
    # Use regex to extract the fact numbers from the slide content
    fact_numbers_match = re.search(r'\{(\d+(?:,\s*\d+)*)\}', slide_plan)
    if fact_numbers_match is None:
        return ""

    fact_numbers = fact_numbers_match.group(1)
    fact_numbers = list(map(int, fact_numbers.split(',')))  # Convert to a list of integers

    # Create a list to store the facts for this slide
    slide_facts = []

    # Use regex to extract facts based on fact numbers
    for num in fact_numbers:
        fact_match = re.search(rf"{num}\.\s*{{(.*?)}}", factsString)
        if fact_match:
            slide_facts.append(f"{num}. {{{fact_match.group(1)}}}")

    # Join the list of facts into a single string
    slide_facts_string = ' '.join(slide_facts)
    return slide_facts_string

def stage_4_extract_fact_groupings(slide_plan):
    # Use regex to extract the fact numbers from the slide content
    fact_numbers_match = re.search(r'\{(.+?)\}', slide_plan)
    if fact_numbers_match is None:
        return ""

    fact_numbers = fact_numbers_match.group(1)
    return fact_numbers



def stage_4_title_subtitle_layout_spliter(powerpointSlide):
    match = re.search(r"TITLE\s*:\s*(.+)\s*\n\s*SUBTITLE\s*:\s*(.+)", powerpointSlide)

    if match:
        title = match.group(1).strip()
        subtitle = match.group(2).strip()

        return [title, subtitle]
    else:
        return "No match found."
def stage_4_task_splitter(powerpoint_slide: str):
    # Regex pattern targeting only the 'TASK :' section
    task_specific_pattern = r'TASK\s*:\s*\[\s*(\{\s*[^}]*\s*\}(?:\s*,\s*\{\s*[^}]*\s*\})*)'
    
    # Find the substring that starts with "TASK :"
    task_substring_match = re.search(task_specific_pattern, powerpoint_slide)
    if task_substring_match:
        task_substring = task_substring_match.group(1)
    else:
        task_substring = ""

    # Then, extract all values within curly braces from the found substring
    regex_pattern = r'\{([^}]+)\}'
    extracted_values = re.findall(regex_pattern, task_substring)
    
    return extracted_values

def stage_4_regex_roleplay(powerpoint_slide: str):
    # Regex pattern targeting the 'ROLEPLAY' section
    roleplay_pattern = r'ROLEPLAY\s*:\s*\[\s*(\{\s*[^}]+\s*\}(?:\s*,\s*\{\s*[^}]+\s*\})*)]'
    roleplay_match = re.search(roleplay_pattern, powerpoint_slide)
    
    if roleplay_match:
        return stage_4_extract_values_from_braces(roleplay_match.group(1))
    else:
        return []

def stage_4_regex_task(powerpoint_slide: str):
    # Regex pattern targeting the 'TASK :' section
    task_pattern = r'TASK\s*:\s*\[(\{[^}]+\}(?:,\s?\{[^}]+\})*)\]'
    task_match = re.search(task_pattern, powerpoint_slide)
    
    if task_match:
        return stage_4_extract_values_from_braces(task_match.group(1))
    else:
        return []

def stage_4_regex_picture(powerpoint_slide: str):
    # Regex pattern targeting the 'PICTURE' section
    picture_pattern = r'PICTURE\s*:\s*\[\s*(\{\s*[^}]*\s*\}(?:\s*,\s*\{\s*[^}]*\s*\})*)'
    picture_match = re.search(picture_pattern, powerpoint_slide)
    
    if picture_match:
        return stage_4_extract_values_from_braces(picture_match.group(1))
    else:
        return []
def stage_4_regex_example(powerpoint_slide: str) : 
    picture_pattern = r'EXAMPLE\s*:\s*\[\s*(\{\s*[^}]*\s*\}(?:\s*,\s*\{\s*[^}]*\s*\})*)'
    picture_match = re.search(picture_pattern, powerpoint_slide)
    
    if picture_match:
        return stage_4_extract_values_from_braces(picture_match.group(1))
    else:
        return []

def extract_slide_number(slideOutline):
    match = re.search(r'POWERPOINT\s(\d+)\s:', slideOutline)

    if match:
        slide_number = int(match.group(1))
        return slide_number
    else:
        return "No match found."
#Extracts the facts from the fact numbers for the powerpoint slide

#NEED TO CREATE A FUNCTION HERE CALLED 'def stage_4_picture_search(searchQueryList)', where it first checks if it's a list, then searches at position i and returns 
#the first image that comes up, OR if it's just a string it just searches it up using that string ONLY.

#################    MODULE SPECIFIC CODE:         ##########################: 
async def stage_4_A_slide_general_content_page(slideNumber, lessonDecription, powerpointPlan, slideFacts):
    gptAgent = OpenAI()
    stage4Temp = 0.5
    generalContentPagePrompt = """ I want you to pretend to be an expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable. Based on this lesson description, and the inputted facts, you are to create a SINGLE powerpoint slide  based on the facts given. Assume that everything in the lesson description is covered in the other slides. Start with a UNIQUE, INTERESTING title, by doing TITLE : INSERT TITLE HERE, and then CONTENT : INSERT THE CONTENT HERE. Tips for content:
- Take into account the context of the overall lesson. 
- Use examples for context/metaphors, with easy-to-understand ways of explaining them
- Use the best techniques to help students understand the concepts
- Make it fun and engaging, but understand that this is one powerpoint slide out of many.
- Use these facts ONLY- DO NOT make up information/facts
- Don't sound cringey or corny
- DO NOT leave any space for placeholder (e.g for an image) - the powerpoint must be a finished product.
- the whole thing should be UNDER 180 words. 
- Use spacing where needed to increase readability
- DO NOT JUST LIST THE FACTS
- ALL of the information provided must be understood by the student to the level provided 
"""  
    gptInput = f"Lesson description : {{ {lessonDecription} }} Lesson Context : {{ {powerpointPlan} }} SLIDE NUMBER IS {slideNumber + 1}, Slide facts :  {slideFacts}"
    
    powerpointSlide = await gptAgent.async_open_ai_gpt4_call(gptInput, generalContentPagePrompt, stage4Temp)
    return powerpointSlide
    #Split the title and content from the returned powerpoint slide : 
#Creates the title and content ofr the 'General Content Page' slide.
############# MODULE A, 'General Content Page' ###################:


async def stage_4_A_picture_query_single_picture(powerpointSlide) : 
    gptAgent = OpenAI()
    pictureQueryPrompt = """I want you to pretend to be an expert teacher. Your task is to analyse the inputted powerpoint slide, and from it ONLY print a SINGLE image query that this powerpoint slide needs to be used to search online on google to find the image, like so (dont include the brackets):

'{INSERT SEARCH QUERY HERE}'

Aim to make the search query have the highest chance of success of getting the correct image first time when searching, THINK about it - don't ask for an image that most likely won't exist.
Create only ONE image query
Here is the slide : 
"""
    pictureQuery = await gptAgent.async_open_ai_gpt4_call(powerpointSlide, pictureQueryPrompt, 0.0)
    return pictureQuery
#Creates the picture search query for the 'General Content Page' slide. 
async def stage_4_A_combined_process(slideNumber, powerpointSlideOutlines, lessonDescription, powerpointPlan, lessonFacts):
    #'A' is 'General content page' 
    slideFacts = stage_4_facts_extraction_from_choices(powerpointSlideOutlines[slideNumber], lessonFacts) # Gets slide facts
    powerpointSlide = await stage_4_A_slide_general_content_page(slideNumber, lessonDescription, powerpointPlan, slideFacts) # Creates slide
    searchQuery = await stage_4_A_picture_query_single_picture(powerpointSlide) # Makes a search query to search online
    powerpointTitleAndContent = stage_4_content_title_layout_splitter(powerpointSlide) #Splits slide into a 'Title' string and 'Content' String
    
    # Creating the structured output to match the desired format
    structured_output = {
        "module": "General content page",
        "slide": {
            "title": powerpointTitleAndContent[0], # Assuming the title is the first part of the tuple
            "description": powerpointTitleAndContent[1], # Assuming the content/description is the second part of the tuple
            "image_caption": searchQuery # Here, I'm considering the 'searchQuery' to represent the image caption. Adjust if needed.
        }
    }
    
    # Return the structured output
    return structured_output
#stage_4_B refers to created the L.O page module

    

################ MODULE EXTRACTION CODE ###################:

#Extracts the module from a powerpoint slide, outputs the correct prompt
def stage_5_extract_module(powerpoint_line):
    pattern = r'Module.*?:\s*(.+?)\s*-'
    powerpointModule = re.search(pattern, powerpoint_line)
    if powerpointModule:
        return powerpointModule.group(1)
    else: 
        print("ERROR in module extraction, make sure the module output syntax is correct.")
#'powerpointSlideOutline' is the outline for a single slide and not t5he grouping.
async def stage_5_module_powerpoint_slide_function_calls(module, powerpointSlideOutline, slideNumber, lessonFacts, lessonDescription, powerpointPlan):
        print(lessonFacts)
        print("THE SLIDE PLAN IS : " + powerpointSlideOutline)
        powerpoint_facts = stage_4_facts_extraction_from_choices(powerpointSlideOutline, lessonFacts)
        print("HERE ARE THE FACTS FOR THE CURRENT POWERPOINT : " + powerpoint_facts)
        print("""
                These are the facts for the current powerpoint : 
                """ + powerpoint_facts)
        if re.search("title_page", module):
            titlePage = await stage_4_title_page_combined_process(lessonFacts)
            return titlePage
        elif re.search("lo_page", module):
            loPage = await stage_4_lo_page_combined_process(lessonFacts)
            return loPage
        elif re.search("general_content_page_easy_bullet_points", module):
            fact_groupings = stage_4_extract_fact_groupings(powerpointSlideOutline)
            bullet_slide = await general_content_easy_bullet_points_final_method(fact_groupings, powerpointPlan, slideNumber, lessonFacts)
            return bullet_slide
        elif re.search("general_content_page_medium_slide_breakup", module) : 
            fact_groupings =  stage_4_extract_fact_groupings(powerpointSlideOutline)
            medium_breakup_slides = await general_content_page_medium_breakup_final_method_looping(powerpoint_facts, fact_groupings, powerpointPlan)
            return medium_breakup_slides
        elif re.search("general_content_page_hard_slide_breakup", module) : 
            fact_groupings =  stage_4_extract_fact_groupings(powerpointSlideOutline)
            hard_breakup_slides = await general_content_page_hard_breakup_implementation_method(powerpoint_facts, fact_groupings, powerpointPlan)
            return hard_breakup_slides
        elif re.search("ending_slide", module):
            finalSlide = await stage_4_ending_slide_combine_process(lessonFacts)
            return finalSlide
        elif re.search("question_module_2_bullet_questions", module):
            question_slide = await stage_4_question_module_2_bullet_questions_combined_process(powerpoint_facts)
            return question_slide
        elif re.search("question_module_3_roleplay_questions", module):
            question_slide = await stage_4_question_module_3_roleplay_question_combine_process(powerpoint_facts)
            return question_slide
        elif re.search("activity_module_1_brainstorming", module):
            activity_slide = await stage_4_activity_module_1_brainstorming_combined_process(powerpoint_facts)
            return activity_slide
        elif re.search("activity_module_2_student_summarisation", module):
            activity_slide = await stage_4_activity_module_2_student_summarisation_combined_process(powerpoint_facts)
            return activity_slide
        elif re.search("activity_module_3_qa_pairs", module):
            activity_slide = await stage_4_activity_module_3_qa_pairs_slide_combined_process(powerpoint_facts)
            return activity_slide
        elif re.search("activity_module_4_focused_listing", module):
            activity_slide = await stage_4_activity_module_4_focused_listing_combined_process(powerpoint_facts)
            return activity_slide

        
        print("Error : no module found.")

            

async def stage_6_create_powerpoint(lessonFacts : str, question_choice : bool) : 
  
    powerpointSlidesDetailed = []
    
    final_powerpoint_plan = stage_3_powerpoint_plan_creator(lessonFacts, question_choice)
    print(final_powerpoint_plan)

    lessonDescription = stage_3_lesson_description(lessonFacts)
    powerpointSlideOutlines = stage_3_slides_powerpoint_extractor(final_powerpoint_plan)

    slide_creation_tasks = []
    for i, slide_outline in enumerate(powerpointSlideOutlines):
        module = stage_5_extract_module(slide_outline)
        slide_creation_task = stage_5_module_powerpoint_slide_function_calls(module, slide_outline, i, lessonFacts, lessonDescription, final_powerpoint_plan)
        slide_creation_tasks.append(slide_creation_task)

    powerpointSlidesDetailed = await asyncio.gather(*slide_creation_tasks)
    return powerpointSlidesDetailed

# test_facts = "1. {The aggressiveness of offensive objectives should be considered, depending on the strength of the opponent.} 2. {Regularly editing land divisions is important as new research is unlocked and experience is accumulated from combat.} 3. {If you need bodies to stop the German or Soviet advance, set the deployment option for your units so that they are deployed as soon as they equipped.} 4. {These green troops will not be as effective as fully trained units will be, but they will be more effective than nothing.} 5. {If you have adjusted your conscription law to either Extensive Conscription or Service by Requirement, then manpower will probably not be an issue in the near term.} 6. {Have multiple lines of infantry, motorized/mechanized, and tank divisions under construction simultaneously.} 7. {A major power should be able to have six to eight infantry divisions being assembled alongside two to three tank divisions and two to three motorized/mechanized divisions.} 8. {You probably do not need to have an infinite stream of mountain or marine units.} 9. {Set limited production runs for these if you didn’t build enough in the pre-game.} 10. {A dozen mountain divisions should be enough in most instances, and only Japan and the United States will need more than 20 marine divisions.} 11. {If your attack line means you have to deal with enemy forts, your attacks will be more successful if they are accompanied by engineer support units, artillery, heavy tanks, and anti-tank support battalions.}"



# print(asyncio.run(stage_6_create_powerpoint(test_facts, False)))