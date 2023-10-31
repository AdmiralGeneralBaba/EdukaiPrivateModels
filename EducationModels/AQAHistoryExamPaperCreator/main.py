import PyPDF2
import chapter_picker as cp
import chapter_extraction as ce
import question_creation as qc


#output is a aqa history a level paper based on textbook given.
def aqa_history_aqa_level_paper_1_creator_general_questions(start_num, end_num, path) : 
    contents_page_json = ce.stage_3_chapter_extractor_v1(start_num, end_num, path)

    output_dictionary = {'general_questions': []}
    #for loop for no of questions
    for i in range(3) : 
        # Finding the page : 
        start_and_end_numbers = cp.stage_3_find_page_range(contents_page_json['content'])
        # Shortening the input : 
        input_content_raw = ce.extract_page(start_and_end_numbers[0], start_and_end_numbers[1])
        # Here we input the input content raw into the token reducer, such that it is below the number we put in here : 
        input_content_shortened = cp.stage_4_token_max_for_question_model_input(input_content_raw, 5000)
        #generating questions here : 
        question = qc.create_weighted_random_question(input_content_shortened) 
        output_dictionary['general_questions'].append = question     
    #returns a list of questions, in this case three.
    return output_dictionary

def aqa_history_aqa_level_paper_1_creator_general_questions_testing(path) : 
    print("Chapter extraction in progress...")
    contents_page_json = {'content': [{'chapter_name': 'Trying to preserve autocracy, 1855–1894', 'page_number': 1}, {'chapter_name': 'The growth of opposition to tsarist rule', 'page_number': 41}, {'chapter_name': 'economic and social developments', 'page_number': 50}, {'chapter_name': 'The collapse of autocracy, 1894–191 7', 'page_number': 60}, {'chapter_name': 'The economic development of russia to 1914', 'page_number': 74}, {'chapter_name': 'Social developments to 1914', 'page_number': 84}, {'chapter_name': 'Opposition: ideas and ideologies', 'page_number': 93}, {'chapter_name': 'political authority, opposition and the state of russia in wartime', 'page_number': 101}, {'chapter_name': 'The establishment of Bolshevik government', 'page_number': 111}, {'chapter_name': 'The emergence of Communist dictatorship, 1917–1941', 'page_number': 124}, {'chapter_name': 'The c ommunist dictatorship', 'page_number': 135}, {'chapter_name': 'economic developments', 'page_number': 146}, {'chapter_name': 'Leninist/Stalinist Society', 'page_number': 157}, {'chapter_name': 'communist control and Terror', 'page_number': 168}, {'chapter_name': 'The Soviet union by 1941', 'page_number': 178}, {'chapter_name': 'The Stalinist dictatorship and reaction, 1941–1964', 'page_number': 184}, {'chapter_name': 'Stalinism in wartime', 'page_number': 184}, {'chapter_name': 'political authority 1945–53', 'page_number': 195}, {'chapter_name': 'Khrushchev and reaction to Stalinism, 1953–64', 'page_number': 203}, {'chapter_name': 'economic and social developments', 'page_number': 209}, {'chapter_name': 'Opposition and the fall of Khrushchev', 'page_number': 221}, {'chapter_name': 'The Soviet union by 1964', 'page_number': 228}]}
    
    output_dictionary = {'general_questions': []}
    print("Starting for loop...")
    for i in range(3): 
        print("finding page...")
        start_and_end_numbers = cp.stage_3_find_page_range(contents_page_json['content'])
        print("Shortening input...")
        input_content_raw = ce.extract_page(5, 9, path)
        input_content_shortened = cp.stage_4_token_max_for_question_model_input(input_content_raw, 5000)

        # Check if input_content_shortened is a string
        if not isinstance(input_content_shortened, str):
            print(f"Expected a string, but got {type(input_content_shortened)} with value: {input_content_shortened}")

        print(f"generating question {i}...")
        question = qc.create_weighted_random_question(input_content_shortened) 
        output_dictionary['general_questions'].append(question)  # fixed this line as well
    print("All questions generated!")
    return output_dictionary
# need to create a new method down here for the 'arguments' question I will complete with teachers. 

path = "C:\\Users\\david\\Desktop\\AlgoCo\\Private Education Models\\EdukaiPrivateModels\\AQA History 1st sample.pdf"
path2 = "C:\\Users\\david\\Desktop\\AlgoCo\\Private Education Models\\EdukaiPrivateModels\\AQA History 2nd sample.pdf"


print(aqa_history_aqa_level_paper_1_creator_general_questions_testing(path2))