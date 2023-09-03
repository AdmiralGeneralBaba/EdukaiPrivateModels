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
  },
  {
    "module": "question_module_2_bullet_questions",
    "slide": {
      "task": [
        "\"What gives solar energy its renewable status?\"",
        "\"Explain the photovoltaic effect in solar power plants\"",
        "\"What are the components of a solar panel?\"",
        "\"How does solar power affect our dependency on fossil fuels?\"",
        "\"Describe the capacity of the sun's energy delivery to Earth every hour\""
      ]
    }
  },
  {
    "module": "General content page",
    "slide": {
      "title": "Journey of Memories: From Short-term to Long-term",
      "description": "Imagine our brain as a vast library, where long-term memories are books stored on shelves. Fact 4 tells us that these books aren't just in one room, but scattered throughout the library.\n\nThe hippocampus acts like a librarian (Fact 5), it helps in transferring these books (information) from the reception (short-term memory) to their rightful places on the shelves (long-term memory).\n\nBut what about the chilling ghost stories or heartwarming tales that tug at our emotions? They get a special corner, overseen by the amygdala (Fact 6). This section is for emotional memories, especially those spine-tingling fear memories.\n\nSo, our brain's library is a complex, organized space, each region playing a unique role in the story of our memories.",
      "image_caption": "'Brain as a library metaphor'"
    }
  },

  {
    "module": "General content page",
    "slide": {
      "title": "The Web of Knowledge: Unraveling Semantic Memory",
      "description": "Dive into the realm of Semantic Memory, a crucial part of our long-term memory. It's like a vast library, storing our understanding of the world, from the meanings of words to general knowledge.\n\nImagine it as a massive web, where each strand represents a concept. These strands are interconnected, forming networks of related concepts, much like a spider weaving a web of knowledge.\n\nThis organization allows us to link ideas, making sense of the world around us. For instance, the concept 'apple' might connect to 'fruit', 'red', 'sweet', and 'tree'.\n\nRemember, Semantic Memory is our personal encyclopedia, always ready to provide information as we navigate our lives!",
      "image_caption": "'Semantic memory network concept'"
    }
  },
  {
    "module": "General content page",
    "slide": {
      "title": "The Epic Tale of Episodic Memory",
      "description": "Welcome to the theatre of your mind, where episodic memory plays out the scenes of your past! Episodic memory is your brain's personal movie director, enabling you to recall specific events and experiences.\n\nThe stars of this show? The hippocampus and frontal cortex. These brain regions take center stage in the production of episodic memory, orchestrating your ability to remember that unforgettable summer vacation or your first day at school.\n\nRemember, every memory is a story waiting to be told, and episodic memory is the narrator that brings these tales to life!",
      "image_caption": "'Hippocampus and frontal cortex brain diagram'"
    }
  },
  {
    "module": "General content page",
    "slide": {
      "title": "The Story of Our Lives: Understanding Episodic Memory",
      "description": "Let's dive into the world of Episodic Memory, the \"personal storyteller\" of our brain! It's responsible for the recollection of specific events, situations, and experiences. Imagine it as a personal diary, recording your life's unique moments.\n\nThe hero of this story is the Hippocampus, nestled in the medial temporal lobe. It's the 'scribe', crucial for writing these episodic 'entries'.\n\nBut what happens when our 'scribe' faces damage? Tragically, it leads to profound difficulties in creating new episodic 'entries'. However, the 'entries' or skills learned before the damage, remain intact, thanks to the support of other brain areas.\n\nSo, even when our 'scribe' is down, our 'diary' doesn't lose all its previous tales!",
      "image_caption": "'Hippocampus in the human brain diagram'"
    }
  },
  {
    "module": "General content page",
    "slide": {
      "title": "The Brain's Memory Keepers: Hippocampus & Prefrontal Cortex",
      "description": "Did you know that certain parts of your brain are like the guardians of your personal history? Meet the Hippocampus and Prefrontal Cortex!\n\n1. The Hippocampus: This little seahorse-shaped structure in your brain is like a scribe, constantly writing down your life's events. But if it gets damaged, it can't record new episodes anymore, causing issues with forming new episodic memories.\n\n2. The Prefrontal Cortex: Think of it as the librarian of your brain, helping you retrieve those precious episodic memories when you need them. So, next time you're reminiscing about that awesome summer vacation, thank your prefrontal cortex!\n\nRemember, a healthy brain is key to a vivid memory album!",
      "image_caption": "'Hippocampus and Prefrontal Cortex in the human brain diagram'"
    }
  },
  {
    "module": "General content page",
    "slide": {
      "title": "Unraveling Memory Mysteries: Semantic Dementia & Neurological Research",
      "description": "Peek into the world of memory disorders with Semantic Dementia, a unique form of frontotemporal dementia. This condition chips away at our semantic memory, impacting both verbal and non-verbal domains, much like an artist gradually losing their color palette.\n\nBut how do we know this? Welcome to the realm of Neurological Research! Tools like fMRI and PET scans are our 'magnifying glasses', allowing us to explore the brain's memory systems in vivid detail. These technologies not only help us understand the intricate workings of memory but also shed light on how diseases can disrupt this delicate mechanism.\n\nUnderstanding memory isn't just about knowing the process; it's also about exploring the disruptions to appreciate the complexity of our brains!",
      "image_caption": "'fMRI scan of brain with Semantic Dementia'"
    }
  },
  {
    "module": "Ending slide",
    "slide": {
      "title": "Memory Mastery: A Neurobiological Adventure",
      "description": "1. **Your Brain's Memory Map** :\n    - Auditory Memory: Left frontal and parietal lobes.\n    - Visual Memory: Right hemisphere.\n2. **Evolutionary Ties** : Remember, your working memory and speech are lifelong buddies from the evolution journey!\n3. **The Infinite Memory Web** : Our long-term memory functions through a complex web of interconnected networks.\n4. **Sensory Pathways** : From our senses to our brain's processing networks - information travels first class!\n5. **Perception Junction** : Cortex - the place where perceptions become representations.\n6. **Just the Facts, Please!** : Semantic memory - our brain's factual storage house.\n7. **Skills & Feels** : Skills and emotional learning - the dynamic duo of long-term memory.\n8. **Personal Stories** : Episodic memory - recall your unique experiences in vibrant detail.\n9. **Remember the Familiar** : Perirhinal Cortex plays an important role in episodic memory, while hippocampus chronicles events and places.\n10. **Hey, What's That?** : Amnesia and semantic dementia - when memory encounters obstacles.\n11. **Scientists at Work** : The quest to decode memory continues with brain studies, neurological patients, and lab animal research.\n\nAlways remember, memory is not just about remembering but also about the joy of learning and experiencing life. Keep exploring!"
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