import PyPDF2
import chapter_picker as cp
import chapter_extraction as ce
import question_creation as qc


#output is a aqa history a level paper based on textbook given.
def aqa_history_a_level_paper_1_creator_general_questions(start_num, end_num, path) : 
    contents_page_json = ce.stage_3_chapter_extractor_v1(start_num, end_num, path)
    output_dictionary = {'general_questions': []}
    for i in range(3) : 
        input_content = cp.stage_3_find_page_range(contents_page_json)
        question = qc.create_weighted_random_question(input_content) 
        output_dictionary['general_questions'].append = question     
    return output_dictionary

# need to create a new method down here for the 'arguments' question I will complete with teachers. 
