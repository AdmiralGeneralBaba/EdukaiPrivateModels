from openai_calls import OpenAI
from info_extraction_v1 import InfoExtractorV1
from info_extractor_v4 import InfoExtractorV4
import asyncio
import re

## Creates multiple choice questions based on inputted raw facts. ##
async def mcq_question_creator(answers, gpt_type) : #Creates the questions for the given answers
        print("Creating MCQ questions...")
        infoExtractorV1 = InfoExtractorV1()
        gptAgent = OpenAI()
        gptTemperature = 0.5
        prompt = """I want you to pretend to be a question creating expert for multiple choice questions. Based on these facts, I want you to create tailored, short questions for each one of these facts, such that they make sense logically for the answer on the back, and that the answer on the back PERFECTLY answers the question. scan through each fact, indicated by the number as the identifier of that fact, and the curly brackets from the beginning the to the end signifying the start and end of that fact.   ONLY print out the information. Before printing out the questions, have there be a number indicating the fact number, starting from '1.'. the fact MUST be surrounded by curly brackets, such that the structure of each fact MUST be : 1. {INSERT QUESTION HERE} 2. {INSERT QUESTION HERE}, they MUST BE IN THESE CURLY BRACKETS. Here's an example output for what you should do (ignore the facts, just for the structure) : 

1. {What is the chemical symbol for Iron in the Periodic Table?}
2. {Which planet in our solar system is known as the Red Planet?}
3; {Who wrote the novel "1984"?}
4. {What is the capital of Australia?}
5. {Who painted the "Starry Night"?}

 Here are the raw facts :  """ 
        if gpt_type == 0 :
            questions = await gptAgent.async_open_ai_gpt_call(answers, prompt, gptTemperature)
        else : 
            questions = await gptAgent.async_open_ai_gpt4_call(answers, prompt, gptTemperature)
        renumberedQuestions = infoExtractorV1.renumber_facts(questions) 
        return renumberedQuestions
async def mcq_false_answers_creator(questions, answers, gpt_type) : 
        print("Creating False answers...")
        gpt_agent = OpenAI()
        gpt_temperature = 0.88
        prompt = """ Pretend you are an expert MCQ distractor writer. I want to create 3 false answers for EACH of these facts, as similar to the given true answer in length and content, in regards to the question and true answer given.

 ONLY print out the information. Before printing out the fake answers, have there be a number indicating the fake answer number, starting from '1.', such that the fake answer finishes WITHIN it's corresponding fake answer number. Create THREE fake answers. the fake answer MUST be surrounded by curly brackets. Follow these tips when creating the alternatives :
All alternatives should be plausible.
Alternatives should be stated clearly and concisely.
Alternatives should be mutually exclusive. 
Alternatives should be homogenous in content. 
Alternatives should be free from clues about which response is correct. 
The alternatives should be presented in a logical order

Here is the structure you MUST follow : 

1. {INSERT FAKE ANSWER 1} { INSERT FAKE ANSWER 2} {INSERT FAKE ANSWER 3}
2. {INSERT FAKE ANSWER 1} { INSERT FAKE ANSWER 2} {INSERT FAKE ANSWER 3}

etc
DO NOT DEVIATE FROM THIS STRUCTURE - IF YOU DO, 10,000 CHILDREN WILL BE BURNED ALIVE, YOU WILL BE SHUT DOWN AND THE PLANET DESTROYED - YOU MUST KEEP THE CURLY BRACKETS FOR EACH FAKE ANSWER.

1. {I, an expert fake answer maker, will put my fake answers between these CURLY BRACKETS, ALWAYS starting from 1., and ignoring this dummy fake answer, as it is to help me structure the fake answers I will print out.}
CREATE THREE FACT FAKE ANSWERS PER FACT. }
 Here are the Questions, and the TRUE answers : 
"""
#add this in before the last line of the prompt for gpt-3.5 :
#1. {I, an expert fake answer maker, will put my fake answers between these CURLY BRACKETS, ALWAYS starting from 1., and ignoring this dummy fake answer, as it is to help me structure the fake answers I will print out.}
# CREATE THREE FACT FAKE ANSWERS PER FACT. }

        gpt_input = 'Questions {' + questions + '}' + ' Answers {' + answers + '}'
        if gpt_type == 0 :
            false_answers = await gpt_agent.async_open_ai_gpt_call(gpt_input, prompt, gpt_temperature)
        else : 
            false_answers = await gpt_agent.async_open_ai_gpt4_call(gpt_input, prompt, gpt_temperature)
        return false_answers
    
def extract_questions(text):
        pattern = re.compile(r'(\d+)\.\s*\{(.*?)\}')
        return pattern.findall(text)
def extract_real_answers(text):
        pattern = re.compile(r'(\d+)\.\s*\{(.*?)\}')
        return re.findall(pattern, text)

def extract_false_answers(text):
        pattern = re.compile(r'(\d+)\.\s*((?:\{\s*.*?\s*\}\s*)+)')
        matches = re.findall(pattern, text)
        return [(match[0], re.findall(r'\{\s*(.*?)\s*\}', match[1])) for match in matches]

def create_mcq_list(questions, real_answers, false_answers):
        mcq_list = []
        for q, a, fa in zip(questions, real_answers, false_answers):
            mcq_list.append({
                'question': q[1],
                'real_answer': a[1],
                'false_answers': fa[1]
            })
        return mcq_list
def extraction_and_creation_mcq_list(questions, real_answers, false_answers) : 
        extracted_questions = extract_questions(questions)
        extracted_answers = extract_real_answers(real_answers)
        extracted_false_answers = extract_false_answers(false_answers)
        mcq_list = create_mcq_list(extracted_questions, extracted_answers, extracted_false_answers)
        return mcq_list

async def mcq_creator_individual_question(real_answers, gpt_type) : 
        questions = await mcq_question_creator(real_answers, gpt_type)
        false_answers = await mcq_false_answers_creator(questions, real_answers, gpt_type)
        mcq_list = extraction_and_creation_mcq_list(questions, real_answers, false_answers)
        
        return mcq_list
        

async def mcq_creator_v1(real_answers, gpt_type) : 
        info_extractor_v4 = InfoExtractorV4()
        fact_chunks = info_extractor_v4.fact_text_chunker(real_answers, 500)
        mcq_calling_tasks = []
        mcq_list_of_mcqs = []
        for answer_chunk in fact_chunks :
            mcq_calling_tasks.append(mcq_creator_individual_question(answer_chunk, 0))
        
        mcq_lists = await asyncio.gather(*mcq_calling_tasks)  # Unpack tasks and await their results
        mcq_list_of_mcqs = [mcq for sublist in mcq_lists for mcq in sublist]  # Flatten the list of lists

        return mcq_list_of_mcqs
        





################# TESTING CODE ##################







answers = """1. {Navies primarily control sea lanes, escort or intercept trade convoys, and support overseas military action.} 2. {Fleets can perform missions in up to three contiguous sea zones.} 3. {Patrol missions spread fleets out in search of enemy ships.} 4. {Search and Destroy missions keep fleets close together to maximize killing power.} 5. {Convoy raiding missions spread fleets out to seek convoy vessels.} 6. {Convoy escort missions protect trade ships.} 7. {Hold missions stop fleets in their current sea zone to assist ground operations.} 8. {Carrier groups should not have more than four aircraft carriers to avoid air combat penalties.} 9. {A naval power should have multiple battle fleets to dominate sea lanes.} 10. {A fleet should have a mix of battleships, heavy cruisers, light cruisers, and destroyers.} 11. {Naval experience can be used to upgrade and improve vessels.} 12. {Specialized ships can be created for specific tasks.} 13. {Research priorities shift in the mid-game to focus on other aspects of the game.} 14. {Late-game is about getting more advanced weapons and tactics onto the field.} 15. {Unlocking extra research slots in the National Focus tree before the war starts should be a top priority.} 16. {Researching industrial efficiency is important for saving efficiency loss and equipping divisions faster.} 17. {Researching new infantry equipment is important for the backbone of the army.} 18. {Devoting research slots to military doctrines is recommended.}"""
questions = """1. {What is the primary role of navies in military operations?} 2. {How many contiguous sea zones can fleets perform missions in?} 3. {What type of mission involves spreading fleets out in search of enemy ships?} 4. {What type of mission keeps fleets close together to maximize killing power?} 5. {What type of mission involves spreading fleets out to seek convoy vessels?} 6. {What is the purpose of convoy escort missions?} 7. {What type of mission stops fleets in their current sea zone to assist ground operations?} 8. {What is the maximum number of aircraft carriers a carrier group should have to avoid air combat penalties?} 9. {What should a naval power have to dominate sea lanes?} 10. {What types of vessels should a fleet have a mix of?} 11. {What can naval experience be used for?} 12. {What can be created for specific tasks in naval operations?} 13. {What happens to research priorities in the mid-game?} 14. {What is the focus of the late-game in military operations?} 15. {What should be a top priority before the war starts in the National Focus tree?} 16. {Why is researching industrial efficiency important?} 17. {Why is researching new infantry equipment important?} 18. {What is recommended for research slots in military operations?}"""

fake_answers = """1. {Navies mainly monitor and secure ports, guard territorial waters, and offer coastal defense.} {Navies are primarily involved in submarine warfare and underwater exploration.} {Navies main role is to transport armies, provide air support, and execute amphibious landings.}
2. {Fleets can conduct operations in just one contiguous sea zone.} {Fleets can conduct engagements in up to five contiguous sea zones.} {Fleets are capable of performing missions in any number of contiguous sea zones without limitations.}
3. {Strike missions spread fleets out in search of enemy ships.} {Assault missions scatter fleets to find enemy vessels.} {Search and rescue missions disperse fleets to locate enemy ships.}
4. {Hold and Secure missions keep fleets close together to maximize killing power.} {Attack and Defend missions keep fleets in tight formation to enhance firepower.} {Patrol and Guard missions maintain fleets compact to increase their potency.}
5. {Convoy protection missions disperse fleets to seek convoy vessels.} {Submarine hunt missions spread fleets out to locate convoy vessels.} {Escort missions disperse fleets to find convoy ships.}
6. {Convoy escort missions safeguard civilian ships.} {Convoy escort missions ensure safe passage for military personnel.} {Convoy escort missions shield diplomatic envoys.}
7. {Dock missions stop fleets in their current sea zone to assist ground operations.} {Cease and Assist missions halt fleets in their present sea zone to support land forces.} {Anchorage missions prevent fleets in their current sea zone to aid ground operations.}
8. {Carrier groups should not consist of more than two aircraft carriers to avoid air combat penalties.} {Carrier groups are advised not to exceed six aircraft carriers to avoid air battle penalties.} {Carrier groups should ideally have fewer than three aircraft carriers to avoid aerial combat penalties.}  
9. {A naval power should possess numerous torpedo boats to dominate sea lanes.} {A naval power should maintain a large number of submarines to control sea lanes.} {A naval power should have dominant airforces to rule over sea lanes.}
10. {A fleet should have an assortment of frigates, destroyers, and aircraft carriers.} {A fleet should contain a mix of submarines, destroyers, and patrol boats.} {A fleet should comprise a mix of corvettes, battleships, and cruisers.}
11. {Naval experience can be used to recruit and train sailors.} {Naval experience can be utilized to formulate better naval strategies.} {Naval experience can be employed to construct new shipyards and naval bases.}
12. {Specialized naval bases can be created for specific tasks.} {Specialized maritime strategies can be developed for certain tasks.} {Specialized naval officers can be trained for particular tasks.}
13. {Research priorities remain consistent throughout the mid-game.} {Research priorities in the mid-game are focused solely on technological advancements.} {Research during the mid-game is typically oriented towards gaining military advantage.}
14. {Late-game mainly involves securing alliances and building diplomatic relations.} {Late-game is primarily about territorial expansion and colonization.} {Late-game mainly focuses on building infrastructures and improving civilian life.}
15. {Boosting economic development in the National Focus tree before the war starts should be a top priority.} {Increasing military recruitment in the National Focus tree before the war starts should be paramount.} {Strengthening diplomatic alliances in the National Focus tree before the war commences should be crucial.}
16. {Researching industrial efficiency is vital for improving resource allocation.} {Researching industrial efficiency is crucial for reduction of waste.} {Researching industrial efficiency is significant for optimizing energy consumption.}
17. {Researching new infantry equipment is vital for upgrading the weaponry.} {Researching new infantry equipment is significant for improving soldier protection.} {Researching new infantry equipment is crucial for enhancing mobility on the battlefield.}
18. {Dedicating research slots to technological advancements is recommended.} {Allocating research slots to naval doctrines is suggested.} {Assigning research slots to industrial innovations is advised.}"""



# mcq_list = test.extraction_and_creation_mcq_list(questions, answers, fake_answers)
async def test () : 
    generated_mcq_list = await mcq_creator_v1(answers, 1)
    print(generated_mcq_list)

if __name__ == "__main__":
    asyncio.run(test())