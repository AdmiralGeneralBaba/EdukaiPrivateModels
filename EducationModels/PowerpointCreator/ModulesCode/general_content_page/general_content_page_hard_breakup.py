from EducationModels.openai_calls import OpenAI
import re
from EducationModels.PowerpointCreator.ModulesCode.regexing_code import *
import asyncio


def create_input_prompt(powerpoint_plan : str, fact_groupings_with_facts : str) : 
    prompt = """I want you to pretend to be an expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable and understandable.
 
You will be given the powerpoint plan for the lesson, the lesson description, as well as the fact you will explain. You are to create a single powerpoint slide, explaining one specific fact for one sub-topic being taught that will be provided to. In this sub topic, there are a bunch of facts that relate to each other that will be given to you for context. You are to ONLY explain the given fact and nothing else.

In your output, you are to give a title, content both stating + explaining the fact with as much detail you think is needed to understand the topic, and a picture query search term to help the student understand the topic better. Use teaching techniques to help students digest the concept.

your output MUST look like this : 

TITLE : {INSERT TITLE FOR THE CONCEPT HERE, WITH THE CURLY BRACKETS}
CONTENT : {INSERT CONTENT HERE WITH THE CURLY BRACKETS} 
PICTURE : {INSERT SEARCH TERM TO SEARCH UP TO FIND THE PERFECT PICTURE TO AID A STUDENT'S UNDERSTANDING}

Here is the powerpoint plan :  """ + "{ " f"{powerpoint_plan}" + "}" + """ 

Here are the facts for your sub-topic : """ + "{ " f"{fact_groupings_with_facts}" + "}" + """ 

After stating the below fact in an easy-to-understand way, explain it in the most concise and efficient way.

Here is the fact you will explain : """
    return prompt


async def general_content_page_hard_breakup_content_creation(input_prompt, slide_fact) : 
    llm = OpenAI()
    temp = 1
    content_output = await llm.async_open_ai_gpt4_call(slide_fact, input_prompt, temp)
    return content_output

async def general_content_page_hard_breakup_content_creation_final_method(slide_facts, fact_groupings, slide_fact, powerpoint_plan) :
    # inclues the facts as they are instead of just numbers
    fact_groupings_input = stage_4_replace_fact_numbers_with_text(fact_groupings, slide_facts)

    #creates the prompt for the content creation stage
    input_prompt = create_input_prompt(powerpoint_plan, fact_groupings_input)

    #creates the content : 
    content = await general_content_page_hard_breakup_content_creation(input_prompt, slide_fact)

    # extracts the content and puts it in a dictionary : 
    extracted_content = extract_content_TITLE_CONTENT_PICTURE(content) 

    #puts that into the structured output here : 
    structured_output = {
        "module" : "general_content_page_hard_breakup",
        "slide" : {
            "title" : extracted_content["TITLE"],
            "description" : extracted_content["CONTENT"],
            "image_caption" : extracted_content["PICTURE"]
        }
    }
    return structured_output

# This method lookps over the fact groupings, creates a slide for each one of the facts 

# facts = "1. {Artillery research should not be neglected.} 2. {There are key values to consider when designing divisions.} 3. {Iron IV division statistics can be found at the official wiki on the website http://www.hoi4wiki.com/Land_warfare.} 4. {Organization refers to how combat ready a unit is and how long it can stay in the field before retreating.} 5. {HP, or Hit Points, represents the number of hits a unit can take before being destroyed.} 6. {Reconnaissance gives a unit an edge in battle by allowing it to choose suitable tactics.} 7. {Supply Use indicates how many supplies a unit consumes in a day.} 8. {Soft attack refers to the number of attacks per round made on an enemy's infantry and support units.} 9. {Hard attack refers to the number of attacks per round made on an enemy's tanks or forts.} 10. {Combat Width determines the number of attacks a division can make against enemy divisions in a round of battle.} 11. {When designing divisions, there is a trade-off between firepower and staying power.} 12. {Primary attacking units should emphasize firepower, while defensive units should emphasize staying power.} 13. {The decision on what to emphasize in divisions depends on the long-term plan.} 14. {Germany needs strong attack divisions in the early game, filling them with mechanics, logistics experts, and artillery.} 15. {The Soviet Union prioritizes staying power until later in the war when offensive operations become possible.}"

async def general_content_page_hard_breakup_implementation_method(slide_facts, fact_groupings, powerpoint_plan) : 
    numbers_array = stage_4_convert_to_separate_numbers(fact_groupings)
    tasks = []
    # Finish this foff
    for i in range(len(numbers_array)) : 
        slide_fact_number = numbers_array[i]
        slide_fact = extract_fact_with_number_and_brackets(slide_fact_number, slide_facts)

        #Generates the slide to
        task = general_content_page_hard_breakup_content_creation_final_method(slide_facts, fact_groupings, slide_fact, powerpoint_plan)
        tasks.append(task)
        #This appends the collection of hard breakup slides into a single long list of module values.
    slides = await asyncio.gather(*tasks)
    return slides

