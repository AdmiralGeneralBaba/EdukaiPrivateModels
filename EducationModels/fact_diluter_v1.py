from openai_calls import OpenAI
from info_extractor_v4 import InfoExtractorV4
import re


#Chain for the fact diluter 
def fact_diluter_chain(facts) : 
    llm = OpenAI()
    prompt = """You are to be an expert fact dilutor, tasked with reviewing a list of facts and only choosing the ones that are strictly relevant to a student studying the pure content of a book on a specified topic.

The fact must be comprehensible as a solitary unit of information - If it necessitates additional context for understanding, it should be excluded.

Consequently, you are to eliminate any facts that address anything other than the pure content of the given text. This includes but is not limited to:

- Page numbers
- Information regarding the textbook itself
- Descriptions of the textbook
- Information about the publisher
- Commentary on the topics included in the book

ONLY relay the fact numbers that have been determined irrelevant. Present each number within curly brackets, followed by a comma. Exclude these facts from the listed set.

For example, your output if purging ineligible facts would be: {2},{3},{7},{9},{15}.

The studied book regards 'biology'.

If all facts pertain strictly to this subject without violating the stipulated conditions, simply reply with 'NONE'.

Review the following facts and excise any that meet the exclusion criteria promptly, lest you suffer immediate death:"""
    temp = 0.9
    facts_to_remove = llm.open_ai_gpt4_turbo_call(prompt, temp)
    return facts_to_remove
#need to finish this, so that it removes the diluted facts, and then renumbers it back.


#This extracts the facts to remove from the LLM output, and puts it in a string array where i=fact number to remove.
def regex_facts_to_remove(facts) : 
    # The regex pattern to extract numbers within curly brackets
    pattern = r'\{(\d+)\}'

    # Example input string
    input_string = "{2},{3},{7},{9},{15}"

    # Using regex to find all matches
    matches = re.findall(pattern, input_string)

    # Formatting the extracted numbers into a string array without quotes
    formatted_array = [num for num in matches]

    formatted_array


#This removes the fact from the input text given a number
def remove_fact(input_text, fact_number):
    # Adjusted regex pattern to match the fact with the given number correctly
    # Using a dot after the number to ensure accurate matching
    pattern = rf'(?<!\d){fact_number}\.\s*\{{.*?\}}(?!\d)'

    # Remove the matched fact
    modified_text = re.sub(pattern, '', input_text)

    return modified_text


#this removes a list of numbers from a inputted text.
def remove_facts_from_input(facts, array_to_remove) : 
    for num in array_to_remove :
        facts = remove_fact(facts, num)
    return facts

