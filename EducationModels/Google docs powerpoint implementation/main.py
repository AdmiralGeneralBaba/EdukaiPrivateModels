import json
from authentication import authenticate
import presentation_tools as pt

json_test = [{
    "module": "Title Page",
    "slide": {
        "subtitle": "An In-depth Exploration of Function Domains, Ranges, Graphs, Implicit Functions, and Inverse Functions.",
        "title": "Understanding Mathematical Functions: From Basics to Advanced Concepts"
    }
}]

def main():
    service = authenticate()
    presentation = service.presentations().create(body={}).execute()
    presentation_id = presentation.get('presentationId')
    create_powerpoint(service, presentation_id, json_test)

def create_powerpoint(service, presentation_id, json_data):
    for i in range(len(json_data)):
        module_name = json_data[i]['module']
        if module_name == 'Title page':
            title = json_data[i]['slide']['title']
            subtitle = json_data[i]['slide']['subtitle']
            pt.create_title_slide_layout(service, presentation_id, title, subtitle)

        elif module_name == 'L.O page':
            title = json_data[i]['slide']['title']
            description = json_data[i]['slide']['description']
            pt.create_title_and_body_slide_layout(service,presentation_id, title, description )
        elif module_name == 'General content page':
            description = json_data[i]['slide']['description']
            image_caption = json_data[i]['slide']['image_caption']
            title = json_data[i]['slide']['title']
            pt.create_general_content_slide(service, presentation_id, title, description, image_caption)
        elif module_name == 'Ending slide':
            description = json_data[i]['slide']['description']
            title = json_data[i]['slide']['title']
            pt.create_title_and_body_slide_layout(service, presentation_id, title, description)     
        elif module_name == 'question_module_2_bullet_questions':
            task = json_data[i]['slide']['task']
            description = '\n'.join(task["task"])
            pt.create_title_and_body_slide_layout(service, presentation_id, "", description)
        elif module_name == 'question_module_3_roleplay_questions':
            roleplay = json_data[i]['slide']['roleplay'][0]
            task = json_data[i]['slide']['task'][0]
            picture = json_data[i]['slide']['picture'][0]
            pt.create_general_content_slide(service, presentation_id, roleplay, task, picture)
        elif module_name == 'activity_module_1_brainstorming':
            task = json_data[i]['slide']['task'][0]
            pt.create_section_header_slide_layout(service, presentation_id, task)
        elif module_name == 'activity_module_2_student_summarisation':
            task = json_data[i]['slide']['task'][0]
        elif module_name == 'activity_module_3_qa_pairs':
            task = json_data[i]['slide']['task'][0]
            example = json_data[i]['slide']['task'][0]
            pt.create_title_and_body_slide_layout(service, presentation_id, task, example)
        elif module_name == 'activity_module_4_focused_listing':
            task = json_data[i]['slide']['task'][0]
            pt.create_section_header_slide_layout(service, presentation_id, task) 
        else:
            print("MODULE NOT FOUND ERROR")
            pass
    else:
        return None

if __name__ == '__main__':
    main()