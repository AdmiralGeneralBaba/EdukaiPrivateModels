import json
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

json_test = [{
    "module": "Title Page",
    "slide": {
        "subtitle": "An In-depth Exploration of Function Domains, Ranges, Graphs, Implicit Functions, and Inverse Functions.",
        "title": "Understanding Mathematical Functions: From Basics to Advanced Concepts"
    }
}]

# Define the scope (permissions) you're requesting
SCOPES = ['https://www.googleapis.com/auth/presentations']

# Authenticate and create the service object
flow = InstalledAppFlow.from_client_secrets_file('C:\\Users\\david\\Desktop\\AlgoCo\\Private Education Models\\EdukaiPrivateModels\\credentials.json', SCOPES)
creds = flow.run_local_server(port=0)  # This will open a web page for authentication

service = build('slides', 'v1', credentials=creds)

presentation = service.presentations().create(body={}).execute()
presentation_id = presentation.get('presentationId')

# Create a blank slide
slide_creation_request = {
    'createSlide': {
        'slideLayoutReference': {
            'predefinedLayout': 'BLANK'
        }
    }
}

response = service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': [slide_creation_request]}).execute()
slide_id = response.get('replies')[0]['createSlide']['objectId']



################################ content page functions ######################

def create_text_boxes(service, presentation_id, new_slide_id):
    # Create text boxes: title, content, and picture
    title_box_request = {
        'createShape': {
            'objectId': 'custom_title_box_id',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': new_slide_id,
                'size': {'height': {'magnitude': 50, 'unit': 'PT'}, 'width': {'magnitude': 600, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 100, 'translateY': 30, 'unit': 'PT'}
            }
        }
    }
    content_box_request = {
        'createShape': {
            'objectId': 'custom_content_box_id',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': new_slide_id,
                'size': {'height': {'magnitude': 400, 'unit': 'PT'}, 'width': {'magnitude': 320, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 150, 'unit': 'PT'}
            }
        }
    }
    picture_box_request = {
        'createShape': {
            'objectId': 'custom_picture_box_id',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': new_slide_id,
                'size': {'height': {'magnitude': 400, 'unit': 'PT'}, 'width': {'magnitude': 320, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 420, 'translateY': 150, 'unit': 'PT'}
            }
        }
    }
    
    # Send the request
    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': [title_box_request, content_box_request, picture_box_request]}
    ).execute()

def insert_text(service, presentation_id, title_text, content_text, picture_text):
    # Insert text into the boxes
    title_insert_request = {
        'insertText': {
            'objectId': 'custom_title_box_id',
            'text': title_text,
            'insertionIndex': 0
        }
    }
    content_insert_request = {
        'insertText': {
            'objectId': 'custom_content_box_id',
            'text': content_text,
            'insertionIndex': 0
        }
    }

    picture_insert_request = {
        'insertText': {
            'objectId': 'custom_picture_box_id',
            'text': picture_text,
            'insertionIndex': 0
        }
    }

    # Send the request
    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': [title_insert_request, content_insert_request, picture_insert_request]}
    ).execute()

def style_text(service, presentation_id):
    # Update style of title text
    title_style_update_request = {
    'updateTextStyle': {
        'objectId': 'custom_title_box_id',
        'textRange': {
            'type': 'ALL'
        },
        'style': {
            'bold': True,
            'fontSize': {
                'magnitude': 24,  # You can adjust the font size as per your preference
                'unit': 'PT'
            }
        },
        'fields': 'bold,fontSize'
    }
}

    # Send the request
    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': [title_style_update_request]}
    ).execute()

def create_and_populate_slide(service, presentation_id, title_text, content_text="Your content here...", picture_text="Your picture here..."):
    # Create a blank slide
    slide_creation_request = {
    'createSlide': {
        'slideLayoutReference': {
            'predefinedLayout': 'BLANK'
        }
    }
}
    response = service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': [slide_creation_request]}).execute()
    new_slide_id = response.get('replies')[0]['createSlide']['objectId']

    # Modularized calls
    create_text_boxes(service, presentation_id, new_slide_id)
    insert_text(service, presentation_id, title_text, content_text, picture_text)
    style_text(service, presentation_id)

create_and_populate_slide(service, presentation_id,"test title", "test content","picture text")

