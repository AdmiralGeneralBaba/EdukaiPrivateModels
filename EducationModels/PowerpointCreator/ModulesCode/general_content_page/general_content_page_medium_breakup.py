from EducationModels.openai_calls import OpenAI
import re
from EducationModels.PowerpointCreator.ModulesCode.regexing_code  import extract_content_TITLE_CONTENT_PICTURE
from EducationModels.PowerpointCreator.ModulesCode.regexing_code import stage_4_replace_fact_numbers_with_text
from EducationModels.PowerpointCreator.ModulesCode.regexing_code import stage_4_convert_to_separate_numbers
from EducationModels.PowerpointCreator.ModulesCode.regexing_code import extract_fact_with_number_and_brackets
import asyncio


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



async def general_content_page_medium_breakup_content_creation(input_prompt, slide_fact) : 
    llm = OpenAI()
    temp = 1
    content_output = await llm.async_open_ai_gpt4_call(slide_fact, input_prompt, temp)
    return content_output

async def general_content_page_medium_breakup_final_creation_method(slide_facts, fact_groupings, slide_fact, powerpoint_plan) :
    # inclues the facts as they are instead of just numbers
    fact_groupings_input = stage_4_replace_fact_numbers_with_text(fact_groupings, slide_facts)

    #creates the prompt for the content creation stage
    input_prompt = create_input_prompt(powerpoint_plan, fact_groupings_input)

    #creates the content : 
    content = await general_content_page_medium_breakup_content_creation(input_prompt, slide_fact)

    print("Here is the content : ", content)
    # extracts the content and puts it in a dictionary : 
    extracted_content = extract_content_TITLE_CONTENT_PICTURE(content) 
    print(extracted_content)

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

async def general_content_page_medium_breakup_final_method_looping(slide_facts, fact_groupings, powerpoint_plan) : 
    collection_of_hard_breakup_slides = []
    numbers_array = stage_4_convert_to_separate_numbers(fact_groupings)
    tasks = []
    # Finish this foff
    for i in range(len(numbers_array)) :
        slide_fact_number = numbers_array[i]
        slide_fact = extract_fact_with_number_and_brackets(slide_fact_number, slide_facts)

        #Generates the slide to append
        task= general_content_page_medium_breakup_final_creation_method(slide_facts, fact_groupings, slide_fact, powerpoint_plan)
        
        tasks.append(task)
        #This appends the collection of hard breakup slides into a single long list of module values.
        
    slides = await asyncio.gather(*tasks)
    for slide in slides : 
        collection_of_hard_breakup_slides.append(slide)
    
    return collection_of_hard_breakup_slides

######################### Testing code #################################

test_facts = "1. {The aggressiveness of offensive objectives should be considered, depending on the strength of the opponent.} 2. {Regularly editing land divisions is important as new research is unlocked and experience is accumulated from combat.} 3. {If you need bodies to stop the German or Soviet advance, set the deployment option for your units so that they are deployed as soon as they equipped.} 4. {These green troops will not be as effective as fully trained units will be, but they will be more effective than nothing.} 5. {If you have adjusted your conscription law to either Extensive Conscription or Service by Requirement, then manpower will probably not be an issue in the near term.} 6. {Have multiple lines of infantry, motorized/mechanized, and tank divisions under construction simultaneously.} 7. {A major power should be able to have six to eight infantry divisions being assembled alongside two to three tank divisions and two to three motorized/mechanized divisions.} 8. {You probably do not need to have an infinite stream of mountain or marine units.} 9. {Set limited production runs for these if you didn’t build enough in the pre-game.} 10. {A dozen mountain divisions should be enough in most instances, and only Japan and the United States will need more than 20 marine divisions.} 11. {If your attack line means you have to deal with enemy forts, your attacks will be more successful if they are accompanied by engineer support units, artillery, heavy tanks, and anti-tank support battalions.}"


fact_groupings = "2, 6, 7"

powerpoint_plan = """POWERPOINT 1 : Module: Title Page - Hearts of Iron IV, A Comprehensive Guide to Military Strategy & Resource Management

POWERPOINT 2 : Module: L.O page - Learning objects for the lesson

POWERPOINT 3 : Module: General content page - {1, 11}, Strategies for offensive combat effectiveness

POWERPOINT 4 : Module: Module 3 Roleplay Questions - {1, 11}

POWERPOINT 5 : Module: General content page - {2, 6, 7}, Managing military production and division development

POWERPOINT 6 : Module: Module 2 Bullet Questions - {2, 6, 7}

POWERPOINT 7 : Module: General content page - {3, 4}, Deploying units in response to immediate threats

POWERPOINT 8 : Module: Module 3 Roleplay Questions - {3, 4}

POWERPOINT 9 : Module: General content page - {5, 8, 9, 10}, Resource and unit type management for sustained military operations

POWERPOINT 10 : Module: Module 2 Bullet Questions - {5, 8, 9, 10}

POWERPOINT 11 : Module: Module 1 Brainstorming - {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}"""

# print(general_content_page_medium_breakup_final_method_looping(test_facts, fact_groupings, powerpoint_plan))
output = """Fact 2 : {The game's military production utilizes a prioritized "Production Line" system, where production efficiency works over time and affects the total output.}

TITLE : {Understand the Production Line System in Hearts of Iron IV}
CONTENT : {In Hearts of Iron IV, the military production operates through a unique "Production Line" system. This system runs on a concept called production efficiency, which is the efficiency of a production line in fulfilling an order. Over time, the production efficiency of a line increases, thus producing more units. It begins at 10% and can reach a maximum of 100%. Multiple factors influence this growth rate, such as the equipment’s complexity and the country’s industrial research advances. Hence, the more time a production line spends on manufacturing a specific equipment type, the better it gets at generating that gear, thus increasing the total output.}
PICTURE : {Hearts of Iron IV Production Line System}"""



# test_output = general_content_page_medium_breakup_final_method_looping(test_facts,fact_groupings, powerpoint_plan)
# print(test_output)

wrong_test = """TITLE : {Strategic Military Production: Simultaneous Construction of Infantry, Motorized/Mechanized, and Tank Divisions}

CONTENT : {Fact: It is essential to have multiple-lines of infantry, motorized/mechanized, and tank divisions under construction simultaneously.

Explanation: In the context of the military strategy game, 'Hearts of Iron IV', strategic resource and military production management is key. One efficient strategy is to have various types of units - Infantry, Motorized or Mechanized, and Tanks - under simultaneous construction. This approach allows for a comprehensive military force ready to tackle diverse battlefield scenarios. Infantry essential for holding lines and direct combat, motorized/mechanized units provide rapid mobility and flexibility, and tank divisions specialise in breakthroughs and dealing large scale damage. By constructing them all at once, it ensures your army remains diverse and prepared for any eventuality.}

PICTURE : {"Hearts of Iron IV military production"}"""
# extract_test = extract_content_TITLE_CONTENT_PICTURE(wrong_test)
# print(extract_test)

asyncio.run(general_content_page_medium_breakup_final_method_looping(test_facts, fact_groupings, powerpoint_plan))
# {1, 11}, Strategies for offensive combat effectiveness 
# {2, 6, 7}, Managing military production and division development
# {3, 4}, Deploying units in response to immediate threats
# {5, 8, 9, 10}, Resource and unit type management for sustained military operations
