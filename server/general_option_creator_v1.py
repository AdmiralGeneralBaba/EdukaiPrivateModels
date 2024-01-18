from openai_calls import OpenAI
from info_extractor_v5 import InfoExtractorV5
import asyncio
import re

def summariser(text) : 
    llm = OpenAI()
    temp = 1
    prompt = """Summarise this: """
    summarised_text = llm.open_ai_gpt3_16k_call(text, prompt, temp)
    return summarised_text

def general_option_creator_llm_call(lesson_facts : str, summary : str) : 
    llm = OpenAI()
    temp = 1
    prompt = """ You are a student, expertly adept at being able to identify the important points within any content given. Inputted to you will be a list of facts, and your job is to reduce these facts to 1/3 the number given to you (e.g if there are 9 facts given, you must reduce this down approx 1/3 of the facts) 
Your decision should be based on deciding which facts are most important relating to the following summary of the text given that will be provided to you.

Your output must EXCLUSIVELY be ONLY the fact numbers you intend to keep and NOTHING ELSE



Here is the summary : """ + "{" + summary + "}" + "And here are the facts : "

    options_chosen = llm.open_ai_gpt4_turbo_call(lesson_facts, prompt, temp)
    return(options_chosen)


def extract_numbers_from_output(output) : 
    output_array = []
    regex_expression = (r"(\d+)\s*,\s*|(\d+)")
    output_array = re.findall(regex_expression, output)
    matches = [num for val in output_array for num in val if num]
    print(matches)
    return matches

def general_option_creator_v1(text, lesson_facts) : 
    info_extractor = InfoExtractorV5()
    summary = summariser(text)
    print(summary)
    chosen_numbers = general_option_creator_llm_call(lesson_facts, summary)
    extracted_numbers = extract_numbers_from_output(chosen_numbers)
    print(extracted_numbers)
    extracted_facts = info_extractor.extract_facts_from_number_array(lesson_facts, extracted_numbers)
    print(extracted_facts)
    return extracted_facts

##### Testing output ####
text_input = """ The Gulf War was an armed conflict between Iraq and a 42-country coalition led by the United States. The coalition's efforts against Iraq were carried out in two key phases: Operation Desert Shield, which marked the military buildup from August 1990 to January 1991; and Operation Desert Storm, which began with the aerial bombing campaign against Iraq on 17 January 1991 and came to a close with the American-led Liberation of Kuwait on 28 February 1991.

On 2 August 1990, Iraq invaded neighboring Kuwait, and had fully occupied the country within two days. Initially, Iraq ran the occupied territory under a puppet government known as the "Republic of Kuwait" before proceeding with an outright annexation in which Kuwaiti sovereign territory was split, with the "Saddamiyat al-Mitla' District" being carved out of the country's northern portion and the "Kuwait Governorate" covering the rest. Varying speculations have been made regarding the true intents behind the Iraqi invasion, most notably including Iraq's inability to repay the debt of more than US$14 billion that it had borrowed from Kuwait to finance its military efforts during the Iran–Iraq War. Kuwait's demands for repayment were coupled with its surge in petroleum production levels, which kept revenues down for Iraq and further weakened its economic prospects; throughout much of the 1980s, Kuwait's oil production was above its mandatory quota under OPEC, which kept international oil prices down. Iraq interpreted the Kuwaiti refusal to decrease oil production as an act of aggression towards the Iraqi economy, leading up to the hostilities. The invasion of Kuwait was immediately met with international condemnation, including in Resolution 660 by the United Nations Security Council (UNSC), which unanimously imposed economic sanctions against Iraq in Resolution 661. British prime minister Margaret Thatcher and American president George H. W. Bush deployed troops and equipment into Saudi Arabia and openly urged other countries to send their own forces to the scene. In response to the joint call, an array of countries joined the American-led coalition, forming the largest military alliance since World War II. The bulk of the coalition's military power was from the United States, with Saudi Arabia, the United Kingdom, and Egypt as the largest lead-up contributors, in that order; Saudi Arabia and the Kuwaiti government-in-exile paid around US$32 billion of the US$60 billion cost to mobilize the coalition against Iraq.

UNSC Resolution 678 adopted on 29 November 1990 offered Iraq one final chance until 15 January 1991 to implement Resolution 660 and withdraw from Kuwait; it further empowered states after the deadline to use "all necessary means" to force Iraq out of Kuwait. Initial efforts to dislodge the Iraqi presence in Kuwait began with an aerial and naval bombardment on 17 January 1991, which continued for five weeks. During this time, as the Iraqi military found itself unable to ward off the coalition's attacks, Iraq began to fire missiles at Israel. While the coalition itself did not include Israel, the Iraqi leadership had launched the campaign under the expectation that the missile barrage would provoke an independent Israeli military response, and hoped that such a response would prompt the coalition's Muslim-majority countries to withdraw (see Arab–Israeli conflict). However, the jeopardization attempt was ultimately unsuccessful as Israel did not respond to any Iraqi attacks, and Iraq continued to remain at odds with most Muslim-majority countries. Iraqi missile barrages aimed at coalition targets stationed in Saudi Arabia were also largely unsuccessful, and on 24 February 1991, the coalition launched a major ground assault into Iraqi-occupied Kuwait. The offensive was a decisive victory for American-led coalition forces, who liberated Kuwait and promptly began to advance past the Iraq–Kuwait border into Iraqi territory. A hundred hours after the beginning of the ground campaign, the coalition ceased its advance into Iraq and declared a ceasefire. Aerial and ground combat was confined to Iraq, Kuwait, and areas straddling the Iraq–Saudi Arabia border.

The conflict marked the introduction of live news broadcasts from the front lines of the battle, principally by the American network CNN. It has also earned the nickname Video Game War, after the daily broadcast of images from cameras onboard American bombers during Operation Desert Storm. The Gulf War has gained notoriety for including three of the largest tank battles in American military history.

Names
The war is also known under other names, such as the Persian Gulf War, First Gulf War, Kuwait War, First Iraq War, or Iraq War[24][25][26][a] before the term "Iraq War" became identified instead with the 2003 Iraq War (also referred to in the U.S. as "Operation Iraqi Freedom").[27] The war was named Umm al-Ma'arik ("mother of all battles") by Iraqi officials.[28]

The following names have been used to describe the conflict itself: Gulf War and Persian Gulf War are the most common terms for the conflict used within western countries, though it may also be called the First Gulf War (to distinguish it from the 2003 invasion of Iraq and the subsequent Iraq War). Some authors have called it the Second Gulf War to distinguish it from the Iran–Iraq War.[29] Liberation of Kuwait (Arabic: تحرير الكويت) (taḥrīr al-kuwayt) is the term used by Kuwait and most of the coalition's Arab states, including Saudi Arabia, Bahrain, Egypt, and the United Arab Emirates. Terms in other languages include French: la Guerre du Golfe and German: Golfkrieg (Gulf War); German: Zweiter Golfkrieg (Second Gulf War); French: Guerre du Koweït (War of Kuwait).[citation needed]

Operational names
Most of the coalition states used various names for their operations and the war's operational phases. These are sometimes incorrectly used as the conflict's overall name, especially the US Desert Storm:

Operation Desert Shield was the US operational name for the US buildup of forces and Saudi Arabia's defense from 2 August 1990, to 16 January 1991[citation needed]
Operation Desert Storm was the US name of the airland conflict from 17 January 1991, through 28 February 1991[citation needed]
Operation Desert Sabre (early name Operation Desert Sword) was the US name for the airland offensive against the Iraqi Army in the Kuwaiti Theater of Operations (the "100-hour war") from 24 to 28 February 1991, in itself, part of Operation Desert Storm[citation needed]
Operation Desert Farewell was the name given to the return of US units and equipment to the US in 1991 after Kuwait's liberation, sometimes referred to as Operation Desert Calm[citation needed]
Operativo Alfil was the Argentine name for Argentine military activities[citation needed]
Opération Daguet was the French name for French military activities in the conflict[citation needed]
Operation Friction was the name of the Canadian operations[30]
Operation Granby was the British name for British military activities during the operations and conflict[31]
Operazione Locusta (Italian for Locust) was the Italian name for the operations and conflict[citation needed]
Campaign names
The US divided the conflict into three major campaigns:

Defense of Saudi Arabian country for the period 2 August 1990, through 16 January 1991[citation needed]
Liberation and Defense of Kuwait for the period 17 January 1991, through 11 April 1991[citation needed]
Southwest Asia Cease-Fire for the period 12 April 1991, through 30 November 1995, including Operation Provide Comfort[citation needed]"""    


lesson_facts = """1. {The Gulf War was an armed conflict between Iraq and a 42-country coalition led by the United States.} 2. {The coalition's efforts against Iraq were carried out in two key phases: Operation Desert Shield and Operation Desert Storm.} 3. {Operation Desert Shield marked the military buildup from August 1990 to January 1991.} 4. {Operation Desert Storm began with the aerial bombing campaign against Iraq on 17 January 1991.} 5. {Operation Desert Storm came to a close with the American-led Liberation of Kuwait on 28 February 1991.} 6. {On 2 August 1990, Iraq invaded neighboring Kuwait and fully occupied the country within two days.} 7. {Iraq ran the occupied territory under a puppet government known as the "Republic of Kuwait" before proceeding with an outright annexation.} 8. {Kuwait's demands for repayment of a debt led to the Iraqi invasion.} 9. {Resolution 660 by the United Nations Security Council imposed economic sanctions against Iraq.} 10. {British prime minister Margaret Thatcher and American president George H. W. Bush deployed troops and equipment into Saudi Arabia.} 11. {An array of countries joined the American-led coalition.} 12. {Saudi Arabia and the Kuwaiti government-in-exile paid around US$32 billion of the US$60 billion cost to mobilize the coalition against Iraq.} 13. {UNSC Resolution 678 offered Iraq one final chance until 15 January 1991 to withdraw from Kuwait.} 14. {Iraq began to fire missiles at Israel during the coalition's attacks.} 15. {Israel did not respond to any Iraqi attacks.} 16. {Iraqi missile barrages aimed at coalition targets stationed in Saudi Arabia were largely unsuccessful.} 17. {On 24 February 1991, the coalition launched a major ground assault into Iraqi-occupied Kuwait.} 18. {The offensive was a decisive victory for American-led coalition forces.} 19. {The Gulf War marked the introduction of live news broadcasts from the front lines of the battle.} 20. {The conflict has gained notoriety for including three of the largest tank battles in American military history.} 21. {The war is also known under other names such as the Persian Gulf War, First Gulf War, and Kuwait War.} 22. {The war was named Umm al-Ma'arik ("mother of all battles") by Iraqi officials.} 23. {The most common terms for the conflict used within western countries are Gulf War and Persian Gulf War.} 24. {Liberation of Kuwait is the term used by Kuwait and most of the coalition's Arab states.} 25. {The US used various names for their operations and the war's operational phases, including Operation Desert Shield, Operation Desert Storm, and Operation Desert Sabre.} 26. {The conflict was divided into three major campaigns: Defense of Saudi Arabian country, Liberation and Defense of Kuwait, and Southwest Asia Cease-Fire.}"""


general_option_creator_v1(text_input, lesson_facts)