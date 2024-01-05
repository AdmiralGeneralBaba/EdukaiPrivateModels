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
- Information about the book itself excluding the knowledge it is supposed to talk about.

ONLY relay the fact numbers that have been determined irrelevant. Present each number within curly brackets, followed by a comma. Exclude these facts from the listed set.

For example, your output if purging ineligible facts would be: {2},{3},{7},{9},{15}.

If all facts pertain strictly to this subject without violating the stipulated conditions, simply reply with 'NONE'.

Review the following facts and excise any that meet the exclusion criteria promptly, lest you suffer immediate death:"""
    temp = 0.9
    facts_to_remove = llm.open_ai_gpt4_turbo_call(facts, prompt, temp)
    return facts_to_remove
#need to finish this, so that it removes the diluted facts, and then renumbers it back.


#This extracts the facts to remove from the LLM output, and puts it in a string array where i=fact number to remove.
def regex_facts_to_remove(facts) : 
    # The regex pattern to extract numbers within curly brackets
    pattern = r'\{(\d+)\}'

    # Using regex to find all matches
    matches = re.findall(pattern, facts)

    # Formatting the extracted numbers into a string array without quotes
    formatted_array = [num for num in matches]

    formatted_array
    return formatted_array


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


def combined_fact_diluter(facts) : 
    #Creates an instance of the infoextractor
    info_extractor = InfoExtractorV4()

    #Calls the fact_diluter_chain to choose which facts to remove.
    facts_to_take_away = fact_diluter_chain(facts)
    print(facts_to_take_away)
    #puts this text output into a string array of numbers to remove: 
    string_array_of_facts_to_remove = regex_facts_to_remove(facts_to_take_away)
    print(string_array_of_facts_to_remove)
    #Removes the facts from the input, so the facts with the number are removed : 
    shortened_facts = remove_facts_from_input(facts, string_array_of_facts_to_remove)

    #renumbers these facts so it makes sense
    final_facts = info_extractor.renumber_facts(shortened_facts)

    return final_facts

test_facts = """ 1. {The tutorial is not especially clear on some things like supply, infrastructure, or how to adjust early game strategies to fit mid and late game situations.} 2. {The early game of Hearts of Iron IV has very little true action unless you are playing Italy or Japan.} 3. {The early game is about setting the table for fighting the war on your terms.} 4. {Players need to think about how they will choose to fight the war.} 5. {There are grand strategic considerations of where to fight and when.} 6. {There are small strategic choices about research and production lines to get to the larger strategic vision.} 7. {Germany starts the game with very few dockyards compared to France, the United Kingdom, and the United States.} 8. {Germany has to import rubber and oil.} 9. {The German player will have to make early decisions about how to use those dockyards until more can be built or conquered.} 10. {Challenging the Royal Navy with battleships or cruisers will take a lot of time.} 11. {Carrier research starts far behind other powers.} 12. {Submarines are only moderately effective against large surface fleets.} 13. {You cannot invade the United Kingdom across the English Channel without clearing some sort of path for your armies.} 14. {Every decision in the game connects to another decision.} 15. {Many choices won’t bear fruit for months or years down the line.} 16. {Players need to spend the early game thinking about their long-term plans and how each decision will connect to another.}"""

facts_diluted = combined_fact_diluter(test_facts)
print(facts_diluted)
