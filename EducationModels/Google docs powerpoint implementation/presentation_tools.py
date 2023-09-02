

#### creates the 'General Content Page' slide outline. 
def create_text_boxes(service, presentation_id, new_slide_id):
    # Create text boxes: title, content, and picture
    title_box_request = {
        'createShape': {
            'objectId': 'custom_title_box_id',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': new_slide_id,
                'size': {'height': {'magnitude': 50, 'unit': 'PT'}, 'width': {'magnitude': 600, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 25, 'unit': 'PT'}
            }
        }
    }
    content_box_request = {
        'createShape': {
            'objectId': 'custom_content_box_id',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': new_slide_id,
                'size': {'height': {'magnitude': 250, 'unit': 'PT'}, 'width': {'magnitude': 320, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 20, 'translateY': 120, 'unit': 'PT'}
            }
        }
    }
    picture_box_request = {
        'createShape': {
            'objectId': 'custom_picture_box_id',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': new_slide_id,
                'size': {'height': {'magnitude': 50, 'unit': 'PT'}, 'width': {'magnitude': 100, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 480, 'translateY': 170, 'unit': 'PT'}
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

#### Creates the 'general content slide' layout :
def create_general_content_slide(service, presentation_id, title_text, content_text="Your content here...", picture_text="Your picture here..."):
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

def create_title_slide_layout(service, presentation_id, title_text, subtitle_text):
    # Define the request for creating a slide using the 'TITLE' predefined layout
    title_slide_creation_request = {
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE'
            }
        }
    }
    
    # Execute the request
    response = service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': [title_slide_creation_request]}
    ).execute()

    # Get the object ID of the newly created slide
    new_slide_id = response.get('replies')[0]['createSlide']['objectId']
    
    # Fetch the slide details to extract the object IDs of title and subtitle
    slide_details = service.presentations().pages().get(
        presentationId=presentation_id,
        pageObjectId=new_slide_id
    ).execute()

    # Extract object IDs for title and subtitle
    title_id = slide_details['pageElements'][0]['objectId']
    subtitle_id = slide_details['pageElements'][1]['objectId']

    # Populate the title and subtitle using 'insertText' requests
    insert_title_request = {
        'insertText': {
            'objectId': title_id,
            'text': title_text,
            'insertionIndex': 0
        }
    }
    insert_subtitle_request = {
        'insertText': {
            'objectId': subtitle_id,
            'text': subtitle_text,
            'insertionIndex': 0
        }
    }

    # Execute the requests to insert title and subtitle text
    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': [insert_title_request, insert_subtitle_request]}
    ).execute()

    return {
        'slideId': new_slide_id,
        'titleId': title_id,
        'subtitleId': subtitle_id
    }

def create_title_and_body_slide_layout(service, presentation_id, title_text, body_text):
    # Define the request for creating a slide using the 'TITLE_AND_BODY' predefined layout
    slide_creation_request = {
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE_AND_BODY'
            }
        }
    }
    
    # Execute the request
    response = service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': [slide_creation_request]}
    ).execute()

    # Get the object ID of the newly created slide
    new_slide_id = response.get('replies')[0]['createSlide']['objectId']
    
    # Fetch the slide details to extract the object IDs of title and body
    slide_details = service.presentations().pages().get(
        presentationId=presentation_id,
        pageObjectId=new_slide_id
    ).execute()

    # Extract object IDs for title and body
    title_id = slide_details['pageElements'][0]['objectId']
    body_id = slide_details['pageElements'][1]['objectId']

    # Populate the title and body using 'insertText' requests
    insert_title_request = {
        'insertText': {
            'objectId': title_id,
            'text': title_text,
            'insertionIndex': 0
        }
    }
    insert_body_request = {
        'insertText': {
            'objectId': body_id,
            'text': body_text,
            'insertionIndex': 0
        }
    }

    # Execute the requests to insert title and body text
    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': [insert_title_request, insert_body_request]}
    ).execute()

    return {
        'slideId': new_slide_id,
        'titleId': title_id,
        'bodyId': body_id
    }