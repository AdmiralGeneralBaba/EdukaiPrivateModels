import re

def stage_4_extract_values_from_braces(substring: str):
    # Extract all values within curly braces from the given substring
    regex_pattern = r'\{([^}]+)\}'
    return re.findall(regex_pattern, substring)

def stage_4_facts_extraction_from_choices(slide_plan, factsString):
    # Use regex to extract the fact numbers from the slide content
    fact_numbers_match = re.search(r'\{(.+?)\}', slide_plan)
    if fact_numbers_match is None:
        return ""

    fact_numbers = fact_numbers_match.group(1)
    fact_numbers = list(map(int, fact_numbers.split(',')))  # Convert to a list of integers

    # Create a list to store the facts for this slide
    slide_facts = []

    # Use regex to extract facts based on fact numbers
    for num in fact_numbers:
        fact_match = re.search(rf"{num}\.\s*{{(.*?)}}", factsString)
        if fact_match:
            slide_facts.append(f"{num}. {{{fact_match.group(1)}}}")

    # Join the list of facts into a single string
    slide_facts_string = ' '.join(slide_facts)
    return slide_facts_string


def stage_4_content_title_layout_splitter(self, powerpointSlide):
    match = re.search(r"TITLE\s*:\s*((?:.|\s)*?)\s*CONTENT\s*:\s*((?:.|\s)*)", powerpointSlide, re.IGNORECASE)
    if match:
        title, content = match.groups()
        return title.strip(), content.strip()
    else:
        print("No match found in the provided slide content.")



def stage_4_title_subtitle_layout_spliter(self, powerpointSlide):
    match = re.search(r"TITLE\s*:\s*(.+)\s*\n\s*SUBTITLE\s*:\s*(.+)", powerpointSlide)

    if match:
        title = match.group(1).strip()
        subtitle = match.group(2).strip()

        return [title, subtitle]
    else:
        return "No match found."
    
def stage_4_task_splitter(powerpoint_slide: str):
    # Regex pattern targeting only the 'TASK :' section
    task_specific_pattern = r'TASK\s*:\s*\[\s*(\{\s*[^}]*\s*\}(?:\s*,\s*\{\s*[^}]*\s*\})*)'
    
    # Find the substring that starts with "TASK :"
    task_substring_match = re.search(task_specific_pattern, powerpoint_slide)
    if task_substring_match:
        task_substring = task_substring_match.group(1)
    else:
        task_substring = ""

    # Then, extract all values within curly braces from the found substring
    regex_pattern = r'\{([^}]+)\}'
    extracted_values = re.findall(regex_pattern, task_substring)
    
    return extracted_values

def stage_4_regex_roleplay(self, powerpoint_slide: str):
    # Regex pattern targeting the 'ROLEPLAY' section
    roleplay_pattern = r'ROLEPLAY\s*:\s*\[\s*(\{\s*[^}]+\s*\}(?:\s*,\s*\{\s*[^}]+\s*\})*)]'
    roleplay_match = re.search(roleplay_pattern, powerpoint_slide)
    
    if roleplay_match:
        return self.stage_4_extract_values_from_braces(roleplay_match.group(1))
    else:
        return []

def stage_4_regex_task(self, powerpoint_slide: str):
    # Regex pattern targeting the 'TASK :' section
    task_pattern = r'TASK\s*:\s*\[(\{[^}]+\}(?:,\s?\{[^}]+\})*)\]'
    task_match = re.search(task_pattern, powerpoint_slide)
    
    if task_match:
        return self.stage_4_extract_values_from_braces(task_match.group(1))
    else:
        return []

def stage_4_regex_picture(self, powerpoint_slide: str):
    # Regex pattern targeting the 'PICTURE' section
    picture_pattern = r'PICTURE\s*:\s*\[\s*(\{\s*[^}]*\s*\}(?:\s*,\s*\{\s*[^}]*\s*\})*)'
    picture_match = re.search(picture_pattern, powerpoint_slide)
    
    if picture_match:
        return self.stage_4_extract_values_from_braces(picture_match.group(1))
    else:
        return []
def stage_4_regex_example(self, powerpoint_slide: str) : 
    picture_pattern = r'EXAMPLE\s*:\s*\[\s*(\{\s*[^}]*\s*\}(?:\s*,\s*\{\s*[^}]*\s*\})*)'
    picture_match = re.search(picture_pattern, powerpoint_slide)
    
    if picture_match:
        return self.stage_4_extract_values_from_braces(picture_match.group(1))
    else:
        return []

def extract_slide_number(self, slideOutline):
    match = re.search(r'POWERPOINT\s(\d+)\s:', slideOutline)

    if match:
        slide_number = int(match.group(1))
        return slide_number
    else:
        return "No match found."
    
def extract_content_TITLE_CONTENT_PICTURE(text):
    # Define the regex patterns for TITLE, CONTENT, and PICTURE
    # Using re.DOTALL to allow for multiline content and relaxing the pattern to match various punctuation
    title_pattern = r"TITLE\s*\{\s*(.*?)\s*\}"
    content_pattern = r"CONTENT\s*\{\s*(.*?)\s*\}"
    picture_pattern = r"PICTURE\s*\{\s*(.*?)\s*\}"

    # Extract the text using the patterns with re.DOTALL flag
    title_text = re.search(title_pattern, text, re.DOTALL)
    content_text = re.search(content_pattern, text, re.DOTALL)
    picture_text = re.search(picture_pattern, text, re.DOTALL)

    # Prepare the dictionary to return
    data_dict = {
        "TITLE": title_text.group(1).strip() if title_text else None,
        "CONTENT": content_text.group(1).strip() if content_text else None,
        "PICTURE": picture_text.group(1).strip() if picture_text else None
    }

    return data_dict

def stage_4_replace_fact_numbers_with_text(fact_groupings : str, facts : str):
    # Parse the facts string to create a mapping of fact number to fact text
    facts = re.findall(r'(\d+)\. \{([^}]+)\}', facts)
    fact_map = {num: fact for num, fact in facts}

    # Function to replace fact numbers with texts
    def replace_fact(match):
        fact_nums = match.group(1).split(', ')
        facts = [fact_map[num.strip()] for num in fact_nums if num.strip() in fact_map]
        return "{" + '; '.join(facts) + "}, " + match.group(2)

    # Replace fact numbers in the input string
    return re.sub(r'\{([\d, ]+)\}, ([^\n]+)', replace_fact, fact_groupings)

def stage_4_convert_to_separate_numbers(numbers_string: str):

    if not numbers_string:
        return []

    return [num.strip() for num in numbers_string.split(',')]

def extract_fact_with_number_and_brackets(fact_number: str, facts_list: str):
    """
    Extracts a specific fact, including its number and curly braces, from a list of facts based on the fact number.

    Parameters:
    fact_number (str): The number of the fact to be extracted.
    facts_list (str): A string containing all facts, each numbered and enclosed in curly braces.

    Returns:
    str: The extracted fact with number and curly braces, or an empty string if the fact number is not found.
    """
    # Regex pattern to match the entire fact including the number and curly braces
    pattern = rf"({fact_number}\.\s*\{{.*?\}})"
    match = re.search(pattern, facts_list)

    if match:
        return match.group(1)
    else:
        return ""  # Return an empty string if no match is found