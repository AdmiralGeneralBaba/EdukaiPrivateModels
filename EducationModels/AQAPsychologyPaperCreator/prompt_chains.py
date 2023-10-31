from EducationModels.openai_calls import OpenAI

#Here is all the different chains for the scenario creator stage : 
#Need to create a holistic method combining these into one method
def cleanup_text_stage_1(text) : 
    llm = OpenAI()
    prompt = """From this inputted text, you are to give it back in readable format, such that all of the annotations for new lines are removed, and any incomplete words are set to be correct. ONLY output the text, and DO NOT CHANGE ANY OF THE CONTENT - you must remain 100 percent true to the source material, or die.

Here is an example of how you would handle a given input : 
 original { KEY TERMS \nMulti-store model (MSM)  – an explanation \nof memory that sees information flowing \nthrough a series of storage systems\nSensory register (SR)  – a short-duration \nstore holding impressions of information \nreceived by the senses\nShort-term memory (STM)  – a temporary \nstore holding small amounts of information \nfor brief periods\nLong-term memory (LTM)  – a permanent \nstore holding limitless amounts of \ninformation for long periods\nCoding  – the means by which information \nis represented in memory\nCapacity  – the amount of information that \ncan be stored at a given time\nDuration  – the length of time information \nremains within storage } 


changed { Key Terms

Multi-store model (MSM) – an explanation of memory that sees information flowing through a series of storage systems.
Sensory register (SR) – a short-duration store holding impressions of information received by the senses.
Short-term memory (STM) – a temporary store holding small amounts of information for brief periods.
Long-term memory (LTM) – a permanent store holding limitless amounts of information for long periods.
Coding – the means by which information is represented in memory.
Capacity – the amount of information that can be stored at a given time.
Duration – the length of time information remains within storage.
"""
    temp  = 0.7
    cleaned_page = llm.open_ai_gpt3_16k_call(text, prompt, temp)
    return cleaned_page

def fact_breakdown_stage_2(cleaned_text) : 
    llm = OpenAI
    prompt = """Pretend you are an fact analyser, who is the best in the world for creating 100 percent accurate facts for a piece of inputted text, tasked with listing the pure facts from a given text. 
I need you to list the facts here, such that they are the pure information needed to understand the textbook. Make sure to include this raw information, and nothing more. When listing the facts, 
                             ONLY print out the information. Before printing out the facts, have there be a number indicating the fact number, starting from '1.', such that the fact finishes WITHIN it's corresponding fact number. the fact MUST be surrounded by curly brackets
                             , such that the structure of each fact MUST be : 1. {INSERT FACT HERE} 2. {INSERT FACT HERE} etc. An example output would be : 
1. {Most kingdoms in Kingdoms of Fantasy IX typically start with three rainbow-colored unicorns.}
2. {In the early stages of the game, players should prioritize their unicorn training on agility and magical endurance.}
3. {When it comes to marshmallow production in a fantastical context, efficiency and magic infusion should be your top priorities to ensure high-quality, magical treats.}
4. {In relation to enchanted factories, transmutation spells should be given the highest priority to maximize production efficiency and product enchantment quality.}
etc.
DO NOT DEVIATE FROM THIS STRUCTURE - IF YOU DO, 10,000 CHILDREN WILL BE BURNED ALIVE, YOU WILL BE SHUT DOWN AND THE PLANET DESTROYED - YOU MUST KEEP THE CURLY BRACKETS FOR EACH FACT
1. {I, an expert fact analyser, will put my facts between these CURLY BRACKETS, ALWAYS starting from 1., and ignoring this dummy fact, as it is to help me structure the facts I will print out.}
 Here is the content : 
"""
    temp = 0.7
    facts = llm.open_ai_gpt_call(cleaned_text, prompt, temp)
    return facts

def fact_diluter_stage_3(facts, concept) : 
    llm = OpenAI
    prompt = f"""You are to pretend to be a expert fact chooser, tasked with picking out which facts from this relate SPECIFICALLY to the following concept : 
{concept}

ONLY output the facts, in the same exact format, or you will DIE
"""
    temp = 0.8
    diluted_facts = llm.open_ai_gpt_call(facts, prompt, temp)
    return diluted_facts

def psychology_term_identifer_stage_4(diluted_facts) : 
    llm = OpenAI()
    prompt = """From these facts, list the psychology-specific terms from it, and nothing else. Your list should start with the number for the fact number you extracted the term you got it from ,and then the term associated with it.   :"""
    temp = 0.0
    psychology_terms = llm.open_ai_gpt_call(diluted_facts, prompt, temp)
    return psychology_terms

def scenario_creator_stage_5(diluted_facts, concept) : 
    llm = OpenAI()
    prompt = """Pretend you are an expert scenario writer, to write an accurate and short little scenario involving people, supposed to demonstrate THIS CONCEPT :""" + f"{concept}" + """
The purpose of this is in the context of a question; it is supposed to demonstrate a concept for a student. 

Here are some optimal examples for you to model your STYLE of output; ignore what is being discussed, FOCUS ON THE STYLE, LENGTH AND TONE : 

example 1 : { Natasha had studied a lot for her A-level Drama performance, mostly practising lines from
a play alone in her room. However, once on stage in front of her teacher and the
examiners, Natasha struggled to remember her lines. Instead, she kept quoting lines from
a different play she had once learnt for GCSE. 
} 

example 2 : { It is the end of the school day and Freddie is pushing other students in the bus queue.
“Stop it, will you?” protests one of Freddie’s classmates.
“You can’t tell me what to do!” laughs Freddie.
At that moment, Freddie turns to see the deputy head, wearing a high-visibility jacket,
staring angrily at him. Without thinking, Freddie stops pushing the other boys and waits
quietly in line.

}

example 3 : { Max has a phobia of the sea. On a family holiday as a child, he was carried away by the
tide and had to be rescued by a lifeguard. Now he has a family of his own, Max refuses to
go on beach holidays.
}


the scenario MUST be under 100 words; if it's not, you have failed, and will instantly suffer the greatest pain any being can imagine for all of eternity. 

Here are the facts relating to this concept for you to explore in your scenario WHERE FUCKING NEEDED. use these facts to guide your creation of the scenario, however, you must not mention them explicitly; you must SHOW them in action implicitly. Output ONLY the scenario, and NOTHING ELSE. 
 : 
"""
    temp = 0.9
    scenario = llm.open_ai_gpt_call(diluted_facts, prompt, temp)
    return scenario
 
def identify_terms_stage_6(psychology_terms, scenario) : 
    llm = OpenAI()
    prompt = """ You are to be a expert decider, tasked with deciding to either a. quote with DIRECT ACCURACY if these specific terms were explicitly quoted in the passage, and if so, quote the associated passage relating to it. The quote MUST contain the specific keyword here. For example, if there is a term called 'leg muscle', and the quote says only 'leg', you shouldn't include that sentence. You must act like a dynamic regex looking for the term. + {""" + f"{psychology_terms}" + "}" + """

YOUR OUTPUT SHOULD LOOK LIKE THIS :

TERM : {INSERT TERM USED} QUOTE : {INSERT QUOTE HERE THAT ONLY CONTAINS THE SENTENCE WITH THE TERM} 

YOU MUST ONLY contain the sentence that includes the term when making this; if you dont, you will BE CRUSHED AND BURNED FOREVER.
"""
    temp = 0.83
    terms_found = llm.open_ai_gpt_call(scenario, prompt, temp)
    return terms_found 

def remove_terms_stage_7(terms_found, scenario, concept) : 
    llm = OpenAI()
    prompt = f""" You are tasked with removing any SINGLE sentence that mentions the concepts given to you here. You don't have to remove the entire section; ONLY the SINGLE sentence/part that ends with a full stop that mentions the terms given here.

HOWEVER, the passage must still display this concept here : {concept}. IF removing the part that is quoted will make the resulting passage not relate to the inputted concept, then DO NOT remove it; THIS IS MORE IMPORTANT THAN REMOVING IT, THE RESULTING PASSAGE MUST RELATE THE CONCEPT UNDER ALL CIRCUMSTANCES.
Here are the terms I am referring. Provided will be first the term and the specific section you should focus on, and then the passage itself. 

Here is the passage : 
{scenario}

YOU MUST keep everything BUT the single line relating to the concepts here.

for example, if the term is 'muscles', and the sentence quoted is 'Johnny walked to the store. This shows he is using his muscles', you would ONLY remove the second part of the sentence and leave in the first part, so it says 'Johnny walked to the store'. 

here are the terms and the quotation to focus on to remove. JUST OUTPUT THE NEW PASSAGE AND NOTHING MORE: """
    temp = 0.9
    final_scenario = llm.open_ai_gpt_call(terms_found, prompt, temp)

# This is the combined method here : 
def combined_scenario_creator(text : str, concept : str) : 
    # cleaned_text = cleanup_text_stage_1(text) # this is probably not needed
    facts = fact_breakdown_stage_2(text)
    diluted_facts = fact_diluter_stage_3(facts, concept)
    psychology_terms = psychology_term_identifer_stage_4(diluted_facts)
    scenario = scenario_creator_stage_5(diluted_facts, concept)
    terms_found = identify_terms_stage_6(psychology_terms, scenario)
    final_scenario = remove_terms_stage_7(terms_found, scenario, concept)
    return final_scenario 
    


# HERE IS THE CHAIN FOR THE CONCEPT IDENTIFER PART : 
def extract_topic_combined_stage(input) : 
    llm = OpenAI()
    temp = 0.8
    prompt = """ you are an expert topic extractor, born to extract the topic underlying the following input. You are to output ONLY the topic that is being discussed, such that anything else included in the request given is ignored. However, you must include some of the specifics within that topic by the user as well, otherwise you will be grinded and burned alive. 

Here are some example inputs, and the outputs you should give : 

input : {i need a 16 mark question about the multi-store model that tests students that is very hard.}
output : {the multi-store model.} 

input : {create a 16 marker relating to ainsworhts strange situation} 
output : {ainsworhts strange situation} 

input : {can you create me a question about the characteristics of phobias? (e.g ocd or something)}
output : {the characteristics of phobias and ocd}

Here is the user inputted query : + {INPUT USER QUERY HERE} 
"""
    concept = llm.open_ai_gpt_call(input, prompt, temp)
    return concept
