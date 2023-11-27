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

facts = "1. {Artillery research should not be neglected.} 2. {There are key values to consider when designing divisions.} 3. {Iron IV division statistics can be found at the official wiki on the website http://www.hoi4wiki.com/Land_warfare.} 4. {Organization refers to how combat ready a unit is and how long it can stay in the field before retreating.} 5. {HP, or Hit Points, represents the number of hits a unit can take before being destroyed.} 6. {Reconnaissance gives a unit an edge in battle by allowing it to choose suitable tactics.} 7. {Supply Use indicates how many supplies a unit consumes in a day.} 8. {Soft attack refers to the number of attacks per round made on an enemy's infantry and support units.} 9. {Hard attack refers to the number of attacks per round made on an enemy's tanks or forts.} 10. {Combat Width determines the number of attacks a division can make against enemy divisions in a round of battle.} 11. {When designing divisions, there is a trade-off between firepower and staying power.} 12. {Primary attacking units should emphasize firepower, while defensive units should emphasize staying power.} 13. {The decision on what to emphasize in divisions depends on the long-term plan.} 14. {Germany needs strong attack divisions in the early game, filling them with mechanics, logistics experts, and artillery.} 15. {The Soviet Union prioritizes staying power until later in the war when offensive operations become possible.}"

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

output = """Fact 2 : {The game's military production utilizes a prioritized "Production Line" system, where production efficiency works over time and affects the total output.}

TITLE : {Understand the Production Line System in Hearts of Iron IV}
CONTENT : {In Hearts of Iron IV, the military production operates through a unique "Production Line" system. This system runs on a concept called production efficiency, which is the efficiency of a production line in fulfilling an order. Over time, the production efficiency of a line increases, thus producing more units. It begins at 10% and can reach a maximum of 100%. Multiple factors influence this growth rate, such as the equipment’s complexity and the country’s industrial research advances. Hence, the more time a production line spends on manufacturing a specific equipment type, the better it gets at generating that gear, thus increasing the total output.}
PICTURE : {Hearts of Iron IV Production Line System}"""




print(asyncio.run(general_content_page_hard_breakup_implementation_method(test_facts, fact_groupings, powerpoint_plan)))






  