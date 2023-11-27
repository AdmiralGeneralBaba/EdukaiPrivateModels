from EducationModels.openai_calls import OpenAI
from EducationModels.PowerpointCreator.ModulesCode.regexing_code import *
import asyncio


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


async def general_content_easy_bullet_points_content_creation(input_prompt, slide_facts) : 
    llm = OpenAI()
    temp = 1
    content_output = await llm.async_open_ai_gpt4_call(slide_facts, input_prompt, temp)
    return content_output

async def general_content_easy_bullet_points_final_method(fact_groupings, powerpoint_plan, slide_number, lesson_facts) :
    prompt = create_input_prompt(powerpoint_plan,slide_number )
    slide_facts = stage_4_replace_fact_numbers_with_text(fact_groupings, lesson_facts)
    content = await general_content_easy_bullet_points_content_creation(prompt, slide_facts)
    print(content)
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

print(asyncio.run(general_content_easy_bullet_points_final_method(fact_groupings, powerpoint_plan, 5, test_facts)))