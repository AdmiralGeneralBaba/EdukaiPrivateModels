from openai_calls import OpenAI
import re


class PowerpointCreatorV4 : 
    #     Fixed stages for a single lesson :
#################    FIXED STAGES FOR EVERY LESSON/POWERPOINT:  #####################
    def stage_1_groupings_for_facts(numberedFacts) : 
        gptAgent = OpenAI()
        stage1Temp = 0.64
        stage1Prompt = """Group these facts into logically consistent chunks to be used for a SINGLE  powerpoint slide - DO NOT make the facts be too long. ONLY output the numbers of the facts, and put them in curly brackets e.g {1, 5, 6} or {7, 13, 2}, and then, in your mind, INTERNALLY justify WHY you chose them.
Then, write a short, 1 line description of the facts NEXT to the facts, like so :
{1, 2, 3}, blah blah, 
{4,5,6}, blah blah, 
etc
also, each section HAS  to be between 2 -  5 facts, and no more/less than that. IF IT'S LESS OR MORE THAN THAT YOU DIE.
For example, you can't output 'these facts are about the...'. Say this in your mind, you must ONLY output the numbers, e.g {1,6,5}
I also want you to order them in the best way to learn these facts, for a powerpoint
DO NOT PRINT YOUR THOUGHTS - I CANNOT STRESS THIS ENOUGH. IF YOU DO, MY FAMILY WILL DIE AND I WILL KILL YOU
here are the facts: 
"""
        optimalFactGroupings= gptAgent.open_ai_gpt4_call(numberedFacts, stage1Prompt, stage1Temp)
        return optimalFactGroupings
    def stage_2_powerpoint_plan(numberedFacts, optimalFactGroupings) : 
        gptAgent = OpenAI()
        stage2Temp = 0.0
        stage2Prompt = """Pretend you are a planner for a powerpoint presentation, tasked the specified modules for each slide. Based on the facts and their corropsonding numbers, as well as the groupings given to you, I need you to :
1. Choose the module for the powerpoint slide number
2. In this module, reprint it, and in the space for 'fact numbers', I want you to insert the fact numbers to be included in that PowerPoint, 
3. Output should be a complete powerpoint plan, with the modules for each powerpoint slide and their corrosponding fact numbers included

organise it like so : 
POWERPOINT 1 : {your output}
POWERPOINT 2 : {your output} 
etc 
Here are the modules name; JUST print out the module name you picked ,and the facts with them. : 
1. Title Page  {no facts needed - just create a title and subtitle separated by a comma}

2. L.O page  + {Learning objects for the lesson} 

3. General content page+ {fact numbers} + {grouping description supplied in the input NEXT to the fact number groupings}

4. Ending slide + {Ending summary title, then a comma, then the summary}
Here are the lesson facts : 
"""      
        gptInput = numberedFacts + optimalFactGroupings
        powerpointPlan = gptAgent.open_ai_gpt4_call(gptInput, stage2Prompt, stage2Temp)
        return powerpointPlan  
    def stage_3_lesson_description(numberedFacts) : 
        gptAgent = OpenAI()
        stage3Temp = 0.49
        stage3Prompt = """These facts are included for a lesson. Summarise these facts into one,  brief line, outlining the lesson."""
        lessonDescription = gptAgent.open_ai_gpt4_call(numberedFacts, stage3Prompt, stage3Temp)
        return lessonDescription

#############     MODULE GENERIC CODE:        ###############
    # Looping stages 
    #Extracts the powerpoint individual slide plans, and the total amount of slides for the current powerpoint
    def stage_4_facts_for_slide_powerpoint_extractor(self, powerpointPlan) : 
        powerpointNumbers = re.findall(r"POWERPOINT (\d+)", powerpointPlan)
        last_powerpoint_number = powerpointNumbers[-1] if powerpointNumbers else None
        powerpointSlides = re.findall(r'(POWERPOINT \d+ : .+? \{.*?\} \{.*?\})', powerpointPlan)
        return powerpointSlides, last_powerpoint_number
    #Extracts the fact numbers from the optimum grouping of a single powerpoint slide 
    def stage_4_facts_extraction_from_choices(self, slideNumber, factsString):
        # Use regex to extract the fact numbers from the slide text
        fact_numbers_match = re.search(r'\{(.+?)\}', slideNumber)
        if fact_numbers_match is None:
            return []

        fact_numbers = fact_numbers_match.group(1)
        fact_numbers = list(map(int, fact_numbers.split(',')))  # Convert to a list of integers

        # Create a list to store the facts for this slide
        slide_facts = []

        # Split the facts string into a list of facts
        factsList = factsString.splitlines()

        # Go through the list of facts and add the ones with matching numbers to slide_facts
        for fact in factsList:
            # Check if line starts with a number
            if fact.split(' ')[0].isdigit():
                number = int(fact.split(' ')[0])  # Extract the fact number from the fact string
                if number in fact_numbers:
                    slide_facts.append(fact)

        return slide_facts
    #Extracts the facts from the fact numbers for the powerpoint slide

    #NEED TO CREATE A FUNCTION HERE CALLED 'def stage_4_picture_search(searchQueryList)', where it first checks if it's a list, then searches at position i and returns 
    #the first image that comes up, OR if it's just a string it just searches it up using that string ONLY.


#################    MODULE SPECIFIC CODE:         ##########################: 

    ############# MODULE A, 'General Content Page' ###################:
    def stage_4_A_slide_general_content_page_splitter(self, powerpointSlide) :
        match = re.search(r"TITLE:\s*(.*?)\n\nCONTENT:\s*\n(.*?)(?=\n\n|$)", powerpointSlide, re.DOTALL)
        if match is not None:
            title, content = match.groups()
            return title, content
        else:
            print("No match found in the provided slide content.")
    #Splits up out of the general content page into two sections of strings
    def stage_4_A_slide_general_content_page(self, slideNumber, lessonDecription, powerpointPlan, slideFacts ) : 
        gptAgent = OpenAI()
        stage4Temp = 0.97  
        generalContentPagePrompt = """ I want you to pretend to be an expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable. Based on this lesson description, and the inputted facts, you are to create a SINGLE powerpoint slide ({SLIDE NUMBER}) based on the facts given. Assume that everything in the lesson description is covered in the other slides. Start with a UNIQUE, INTERESTING title, by doing TITLE : {INSERT TITLE HERE}, and then CONTENT : {INSERT THE CONTENT HERE}. Tips for content:
- Take into account the context of the overall lesson. 
- Use examples for context/metaphors, with easy-to-understand ways of explaining them
- Use the best techniques to help students understand the concepts
- Make it fun and engaging, but understand that this is one powerpoint slide out of many.
- Use these facts ONLY- DO NOT make up information/facts
- Don't sound cringey or corny
- DO NOT leave any space for placeholder (e.g for an image) - the powerpoint must be a finished product.
- the whole thing should be UNDER 180 words. 
- Use spacing where needed to increase readability
""" 
        gptInput = "Lesson description : {" + lessonDecription  +"}" + "Lesson Context : {" + powerpointPlan + "}" + f"SLIDE NUMBER IS {slideNumber}, " + "Lesson Facts: "  + slideFacts ## Input for GPT

        powerpointSlide = gptAgent.open_ai_gpt4_call(gptInput, generalContentPagePrompt, temp=stage4Temp) 
        titleAndContent = self.stage_4_A_slide_general_content_page_splitter(powerpointSlide)
        return titleAndContent
        #Split the title and content from the returned powerpoint slide : 
    #Creates the title and content ofr the 'General Content Page' slide.
    def stage_4_A_picture_query_single_picture(self, titleAndContent) : 
        gptAgent = OpenAI()
        pictureQueryPrompt = """I want you to pretend to be an expert teacher. Your task is to analyse the inputted powerpoint slide, and from it ONLY print a number of images that this powerpoint slide need, and then the search query intended to be used to search online on google next the image number, like so (dont include the brackets):

'{INSERT SEARCH QUERY HERE}'

Aim to make the search query have the highest chance of success of getting the correct image first time when searching, THINK about it - don't ask for an image that most likely won't exist.
Create only ONE image query
Here is the slide : 
"""
        fullSlide = " TITLE : " + titleAndContent[0] + " CONTENT : " + titleAndContent[1]
        pictureQuery = gptAgent.open_ai_gpt4_call(fullSlide, pictureQueryPrompt, 0.0)
        return pictureQuery
    #Creates the picture search query for the 'General Content Page' slide. 

   
   
    def stage_4_A_combined_process(self, slideNumber, lessonDescription, powerpointPlan, lessonFacts) :
        slideFacts = self.stage_4_facts_extraction_from_choices(slideNumber, lessonFacts) # Gets slide facts
        powerpointSlide = self.stage_4_A_slide_general_content_page(slideNumber,lessonDescription,powerpointPlan, slideFacts) # Creates slide
        powerpointTitleAndContent = self.stage_4_A_slide_general_content_page_splitter(powerpointSlide) #Splits slide into a 'Title' string and 'Content' String
        searchQuery = self.stage_4_A_picture_query_single_picture(powerpointSlide) # Makes a search query to search online
        #NEED to input a stage here where it searches online for a image.
        return powerpointTitleAndContent, searchQuery # Returns the splitted powerpoint slide tuple and the search query
        








################ MODULE EXTRACTION CODE ###################:

    #Extracts the module from a powerpoint slide, outputs the correct prompt
    def stage_5_extract_module(self, powerpoint_line):
        pattern = r"POWERPOINT \d+ : (.*?) \{"
        powerpointModule = re.search(pattern, powerpoint_line)
        if powerpointModule:
            return powerpointModule.group(1)  # Return the captured group, which is the module name
        else : 
            print("ERROR in module extraction, make sure the module output syntax is correct.")
        #returns the prompt for that module
    
 
  

test = PowerpointCreatorV4()

facts =  """1 Supply routes can be improved by improving infrastructure and naval bases.
2 The map is divided into air zones for planes to operate in.
3 There are five basic types of planes in Hearts of Iron IV.
4 Fighters can be used for air superiority and interception missions.
5 There are light fighters and heavy fighters, each with different capabilities.
6 Heavy fighters have greater operational range and can sustain more damage but are vulnerable to lighter fighter planes.
7 Guns work better against enemy bombers.
8 Close attack aircraft are light bombers used to support armies in combat.
9 CAS planes attack enemy troops directly.
10 CAS planes can also attack ships and ports through Naval Strikes and Port Strikes.
11 CAS planes make up the bulk of bombing wings.
12 Tactical bombers are midway between close attack support and strategic bombers.
13 Tactical bombers can perform Close Air Support, Port Strikes, or Strategic bombing.
14 Tactical bombers have greater range than CAS planes but cannot attack ships at sea.
15 Strategic bombers are used for the destruction of the enemy's industrial base and infrastructure.
16 Strategic bombers have long range and high survivability.
17 Mid-game is a period of time during the game.
18 Naval bombers specialize in naval strikes and port strikes.
19 Naval bombers are crucial for Japan and Italy due to the risk of amphibious and naval attacks.
20 Naval bombers are specialized in their purpose.
21 Japan and the United States should develop the carrier variant of naval bombers.
Here are the optimal fact groupings """


# Text of the PowerPoint slide
slide = 'POWERPOINT 3 : General content page {1, 17} {Infrastructure and Game Timing}'

# extracted_facts = test.stage_4_facts_extraction(slide, facts)
# 
# print(extracted_facts)

powerpoint_line = "POWERPOINT 2 : L.O page {Learning objects for the lesson}"
module = test.stage_4_extract_module(powerpoint_line)
print(module)  # Output: L.O page

text = """
SLIDE NUMBER: 7

TITLE: Naval Bombers: The Oceanic Advantage in Hearts of Iron IV

CONTENT: 

Naval bombers play a critical role in Hearts of Iron IV, specializing in naval strikes and port strikes. Given their specific role, they are absolutely crucial for countries like Japan and Italy where the risk of amphibious and naval attacks is high.

Take the scenarios of Japan and the United States. Both countries are surrounded by large bodies of water, making them attractive targets for maritime assaults. Here, naval bombers act as a formidable line of defense. But, these are not just 'regular' naval bombers. 

For countries like Japan and the United States, it's essential to develop the carrier variant of naval bombers. Why? Imagine a mobile airstrip crossing oceans, carrying a fleet of airborne defenders, ready to protect against maritime threats from any direction. That's what a carrier gives you. In Hearts of Iron IV, it’s not just about having the right weapons, but knowing how to use them strategically.
"""
test.stage_4_A_combined_process()


######################            TO DO FOR THIS SECTION :            ###########################

#NEED TO CREATE A FUNCTION HERE CALLED 'def stage_4_picture_search(searchQueryList)', where it first checks if it's a list, then searches at position i and returns 
    #the first image that comes up, OR if it's just a string it just searches it up using that string ONLY. LOOK UP, I PUT IT WHERE IT SHOULD GO
#NEED TO add in the L.O module, title page module and ending slide module/extract it from the powerpoint plan
#NEED TO figure out how to search online programmically and have it return 
#NEED to finish the 'powerpoint full process' creator