import json
from authentication import authenticate
import presentation_tools as pt

json_test = [
  {
    "module": "Title Page",
    "slide": {
      "title": "Exploring the Complexity of Memory: Neurological Perspectives",
      "subtitle": "The Intricate Pathways of Memory Formation and Retrieval in the Brain"
    }
  },
  {
    "module": "L.O page",
    "slide": {
      "title": "Neurobiology of Memory: Understanding Different Memory Systems",
      "description": "By the end of this presentation, you should be able to:\n\n1. Identify the brain regions associated with auditory parts of working memory and the visual sketchpad.\n2. Understand the potential evolutionary relationship between working memory and speech.\n3. Differentiate between the types and locations of long-term memory systems in the brain.\n4. Describe the role of the cortex in object perception and memory categorization.\n5. Explain the differences between episodic and semantic memory, and the impact of specific neurological conditions on these memory systems.\n6. Understand the roles of the perirhinal cortex and hippocampus in episodic memory encoding and familiarity."
    }
  },
  {
    "module": "General content page",
    "slide": {
      "title": "The Brain's Post-it Note: Understanding Working Memory",
      "description": "Working memory, the brain's \"post-it note\", is our system for temporarily holding and manipulating information. It's like the mental workspace where we juggle and process data. Critical for cognitive abilities such as planning, problem solving and reasoning, it's the foundation of our mental agility.\n\nAt the heart of this system is the prefrontal cortex, a region of the brain acting as the conductor of this cognitive orchestra, managing, organizing, and manipulating information. It's the boss in the office of our minds, keeping track of tasks, and ensuring everything runs smoothly.\n\nWith working memory, we can plan our day, solve a puzzle, or reason out complex problems. It's the unsung hero behind our everyday cognitive feats!",
      "image_caption": "'Prefrontal cortex working memory diagram'"
    }
  }
]

def main():
    service = authenticate()
    presentation = service.presentations().create(body={}).execute()
    presentation_id = presentation.get('presentationId')
    
    # Get the list of slides in the presentation.
    slides = presentation.get('slides')
    
    # If there are slides in the presentation, delete the first one.
    if slides:
        slide_id = slides[0].get('objectId')
        requests = [{
            'deleteObject': {
                'objectId': slide_id
            }
        }]
        service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()
    
    # Now, call create_powerpoint
    create_powerpoint(service, presentation_id, json_test)


def create_powerpoint(service, presentation_id, json_data):
    for i in range(len(json_data)):
        module_name = json_data[i]['module']
        if module_name == 'Title Page':
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
            description = '\n'.join(task)
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
    else:
        return None

if __name__ == '__main__':
    main()