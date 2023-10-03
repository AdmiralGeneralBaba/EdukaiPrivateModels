import json
import random

def stage_1_get_random_index(data):
    # Pick a random index from the JSON
    # -2 to ensure we have an index above the selected one
    selected_index = random.randint(0, len(data) -2)  
    return selected_index

def stage_2_find_next_page(data, selected_index, selected_page_number):
    # Find the next index where the page number is more than the selected page number
    for next_index in range(selected_index + 1, len(data)):
        next_page_number = data[next_index]["page_number"]
        if next_page_number > selected_page_number:
            return next_index, next_page_number
    else:  # if no such index is found, we use the last index
        next_index = len(data) - 1
        next_page_number = data[next_index]["page_number"]
        return next_index, next_page_number

def stage_3_find_page_range(data):
    # Get a random index and the page number for that index
    selected_index = stage_1_get_random_index(data)
    selected_page_number = data[selected_index]["page_number"]
    
    # Find the next page where the page number is more than the selected page number
    next_index, next_page_number = stage_2_find_next_page(data, selected_index, selected_page_number)
    
    return selected_page_number, next_page_number

def stage_4_token_max_for_question_model_input(string_maybe_list, token_max_limit : int):
    #converts the list of string into a single string, Need to change this for V2 
    single_string = " ".join(string_maybe_list)
    token_size = int(token_max_limit * 0.75)
    new_string = single_string[:token_size]
    return new_string

data = json.loads("""[
    {"chapter_name": "Chapter 1", "page_number": 1},
    {"chapter_name": "Chapter 2", "page_number": 2},
    {"chapter_name": "Chapter 3", "page_number": 2},
    {"chapter_name": "Chapter 4", "page_number": 4},
    {"chapter_name": "Chapter 5", "page_number": 7},
    {"chapter_name": "Chapter 6", "page_number": 10},
    {"chapter_name": "Chapter 7", "page_number": 11},
    {"chapter_name": "Chapter 8", "page_number": 11},
    {"chapter_name": "Chapter 9", "page_number": 14},
    {"chapter_name": "Chapter 10", "page_number": 15},
    {"chapter_name": "Chapter 11", "page_number": 18},
    {"chapter_name": "Chapter 12", "page_number": 20},
    {"chapter_name": "Chapter 13", "page_number": 22},
    {"chapter_name": "Chapter 14", "page_number": 23},
    {"chapter_name": "Chapter 15", "page_number": 26},
    {"chapter_name": "Chapter 16", "page_number": 28},
    {"chapter_name": "Chapter 17", "page_number": 30},
    {"chapter_name": "Chapter 18", "page_number": 33},
    {"chapter_name": "Chapter 19", "page_number": 35},
    {"chapter_name": "Chapter 20", "page_number": 38}
]""")






# Running the main function to find the page range