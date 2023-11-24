import re

def stage_4_extract_values_from_braces(self, substring: str):
    # Extract all values within curly braces from the given substring
    regex_pattern = r'\{([^}]+)\}'
    return re.findall(regex_pattern, substring)

def stage_4_facts_extraction_from_choices(self, slide_plan, factsString):
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
def stage_4_task_splitter(self, powerpoint_slide: str):
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
    # Define the regex patterns for TITLE, CONTENT, and PICTURE with optional spaces
    title_pattern = r"TITLE\s*\{(.*?)\}"
    content_pattern = r"CONTENT\s*\{(.*?)\}"
    picture_pattern = r"PICTURE\s*\{(.*?)\}"

    # Extract the text using the patterns
    title_text = re.search(title_pattern, text)
    content_text = re.search(content_pattern, text)
    picture_text = re.search(picture_pattern, text)

    # Prepare the dictionary to return
    data_dict = {
        "TITLE": title_text.group(1) if title_text else None,
        "CONTENT": content_text.group(1) if content_text else None,
        "PICTURE": picture_text.group(1) if picture_text else None
    }

    return data_dict