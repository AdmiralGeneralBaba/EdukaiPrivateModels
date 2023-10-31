
from vector_database import vectorise_pdf
from prompt_chains import combined_scenario_creator
from prompt_chains import extract_topic_combined_stage


def main() : 
    print("put your input here : ")
    query = input()
    db = vectorise_pdf("EducationModels\\AQAPsychologyPaperCreator\\psychology.pdf", 3)
    concept = extract_topic_combined_stage(query)
    pages = db.similarity_search(concept)
    #Creates the RAG context for the query
    for i in range(len(pages)) : 
        long_string = "".join(page.page_content for page in pages)
    
    scenario = combined_scenario_creator(text=long_string, concept=concept)
    return scenario

print(main())