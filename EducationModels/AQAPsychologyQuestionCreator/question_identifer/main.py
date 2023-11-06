from EducationModels.AQAPsychologyQuestionCreator.essay_question_prompts import psychology_description_16_marker_question_creator
from EducationModels.AQAPsychologyQuestionCreator.essay_question_prompts import psychology_discussion_16_marker_question_creator
from EducationModels.AQAPsychologyQuestionCreator.essay_question_prompts import psychology_16_mark_scenario_creator_full
from EducationModels.AQAPsychologyQuestionCreator.question_identifer.question_identifier_chain import psychology_question_type_identifier


def psychology_exam_essay_question_creator(query, context, concept) : 
    question_type = psychology_question_type_identifier(query)

    match question_type : 
        case "discussion" :
            question = psychology_discussion_16_marker_question_creator(context, query)
        case "description" : 
            question = psychology_description_16_marker_question_creator(context, query)
        case "scenario" : 
            question = psychology_16_mark_scenario_creator_full(context, concept)
    return question 


