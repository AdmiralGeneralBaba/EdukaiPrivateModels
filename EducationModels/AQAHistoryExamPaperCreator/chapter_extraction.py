import PyPDF2
from EducationModels.openai_calls import OpenAI
import json
from EducationModels.AQAHistoryExamPaperCreator import general_methods as gm



def stage_1_cleanup(pdf_text) : 
    llm = OpenAI()
    input_prompt = """ You are to be an expert text cleaner. From this inputted text of a contents page of a book, you are to clean up the text such that it is within readable format, and change NOTHING ELSE. 

Include the page numbers for each chapter. 
Here is the input : 
"""    
    temp = 0 
    cleanup = llm.open_ai_gpt3_16k_call(pdf_text, input_prompt, temp )
    return cleanup 
def stage_2_json_creator(cleaned_text) : 
    llm = OpenAI()
    temp = 1
    input_prompt = """ I want you to become an expert JSON creator. Your job is to create me a JSON from the following input, which is a contents page for a book. 

Within the JSON, you are to each instance inside it have two values; chapter_name : {insert the chapter name} and page_number : {insert the page number} (being the page number where it starts from)

include only the sub-chapters, and such that only the ones that start from a number, NOT  a roman numeral (e.g v, iv etc)

DO NOT include duplicate chapters for the same page - e.g if the both start at '5', assume the last one is the real chapter, and ignore the previous entries. 

The output should look such as this : 
content {[ 
{
chapter_name : {chapter name here}
page_number : {page_number here}
}
{
chapter_name : {chapter name here}
page_number : {page_number here}
}
]} 

output the JSON and NOTHING ELSE. 

Here is the input : 
"""
    raw_output = llm.open_ai_gpt4_call(cleaned_text, input_prompt, temp)
    json_output = json.loads(raw_output)
    return json_output

def stage_3_chapter_extractor_v1(start_num, end_num, path) : 
    
    content = gm.extract_page(start_num, end_num, path)
    input_cleanup = ''.join(content)
    print("Stage 1 in progress...")
    cleaned_text = stage_1_cleanup(input_cleanup)
    print("Stage 2 in progress...")
    json_output = stage_2_json_creator(cleaned_text)
    print("COMPLETE!")
    return json_output




path = "C:\\Users\\david\\Desktop\\AlgoCo\\Private Education Models\\EdukaiPrivateModels\\AQA History 1st sample.pdf"
path2 = "C:\\Users\\david\\Desktop\\AlgoCo\\Private Education Models\\EdukaiPrivateModels\\AQA History 2nd sample.pdf"
print(gm.extract_page(4, 6, path2))
# test = stage_3_chapter_extractor_v1(2,3,path2)

# print(test)