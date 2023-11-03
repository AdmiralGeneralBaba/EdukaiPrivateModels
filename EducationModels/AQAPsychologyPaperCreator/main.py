from vector_database import vectorise_pdf
from scenario_creator_chain import combined_scenario_creator
from concept_identifer_chain import extract_topic_combined_stage
from psychology_essay_scenario_question_creator import psychology_scenario_16_marker_question_creator


# question creator, for now it is only the 16 marker scenario question
#Creates the 16_marker
def psychology_16_mark_scenario_creator_full(text, concept) : 
    scenario = combined_scenario_creator(text, concept)
    question = psychology_scenario_16_marker_question_creator(scenario, concept)
    exam_question = scenario + " " + question
    return exam_question

def main() : 
    print("put your input here : ")
    query = input()
    db = vectorise_pdf("EducationModels\\AQAPsychologyPaperCreator\\psychology.pdf", 3)
    concept = extract_topic_combined_stage(query)
    pages = db.similarity_search(concept)
    #Creates the RAG context for the query
    for i in range(len(pages)) : 
        long_string = "".join(page.page_content for page in pages)
    exam_question = psychology_16_mark_scenario_creator_full(long_string, concept)
    return exam_question
    #TEST THIS OUT TOMORROW

print(main())



     