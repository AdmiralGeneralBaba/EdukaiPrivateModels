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

    title_text = "test title"
    content_text = "test content"
    picture_text = "picture text"

    pt.create_title_slide(service, presentation_id, title_text, content_text)

if __name__ == '__main__':
    main()