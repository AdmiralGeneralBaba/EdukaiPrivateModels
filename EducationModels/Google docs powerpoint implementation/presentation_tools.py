import requests
from selenium import webdriver
import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def fetch_image_urls(query, max_links_to_fetch=2, api_key='AIzaSyAe2BL2P6DiaYaKzGVFXoolyjUt0NT7xs4', cse_id='f2a7e2726ff814997'):
    endpoint = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
        'searchType': 'image',
        'num': max_links_to_fetch
    }

    response = requests.get(endpoint, params=params)
    result = response.json()
    
    if 'items' in result:
        return [item['link'] for item in result['items']]
    else:
        return []

def create_text_boxes(service, presentation_id, new_slide_id):
    # Create text boxes: title, content, and picture
    title_box_request = {
        'createShape': {
            'objectId': f'title_{new_slide_id}',  # Unique ID based on slide ID
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': new_slide_id,
                'size': {'height': {'magnitude': 50, 'unit': 'PT'}, 'width': {'magnitude': 600, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 13, 'unit': 'PT'}
            }
        }
    }
    content_box_request = {
        'createShape': {
            'objectId': f'content_{new_slide_id}',  # Unique ID based on slide ID
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': new_slide_id,
                'size': {'height': {'magnitude': 320, 'unit': 'PT'}, 'width': {'magnitude': 350, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 11, 'translateY': 80, 'unit': 'PT'}
            }
        }
    }
    # Send the request
    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': [title_box_request, content_box_request]}
    ).execute()

def insert_text_and_image(service, presentation_id, new_slide_id, title_text, content_text, image_urls):
    # Insert text into the boxes
    title_insert_request = {
        'insertText': {
            'objectId': f'title_{new_slide_id}',  # Referencing the unique ID
            'text': title_text,
            'insertionIndex': 0
        }
    }
    content_insert_request = {
        'insertText': {
            'objectId': f'content_{new_slide_id}',  # Referencing the unique ID
            'text': content_text,
            'insertionIndex': 0
        }
    }


    # Use the scraped image URL for the picture box
    picture_insert_request = {
        'createImage': {
            'url': image_urls[1],  # The scraped image URL
            'objectId': f'img_{new_slide_id}',  # Unique ID based on slide ID
            'elementProperties': {
                'pageObjectId': new_slide_id,
                'size': {'height': {'magnitude': 50, 'unit': 'PT'}, 'width': {'magnitude': 100, 'unit': 'PT'}},
                'transform': {'scaleX': 5, 'scaleY': 5, 'translateX': 285, 'translateY': 110, 'unit': 'PT'}
            }
        }
    }
    # Send the request
    try: 
        service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': [title_insert_request, content_insert_request, picture_insert_request]}
            ).execute()
    except : 
        picture_insert_request = {
        'createImage': {
            'url': image_urls[1],  # The scraped image URL
            'objectId': f'img_{new_slide_id}',  # Unique ID based on slide ID
            'elementProperties': {
                'pageObjectId': new_slide_id,
                'size': {'height': {'magnitude': 50, 'unit': 'PT'}, 'width': {'magnitude': 100, 'unit': 'PT'}},
                'transform': {'scaleX': 5, 'scaleY': 5, 'translateX': 285, 'translateY': 110, 'unit': 'PT'}
            }
        }
    }
        service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': [title_insert_request, content_insert_request, picture_insert_request]}
            ).execute()
        
        
 
def style_text(service, presentation_id, new_slide_id):
    # Update style of title text
    title_style_update_request = {
        'updateTextStyle': {
            'objectId': f'title_{new_slide_id}',  # Referencing the unique ID
            'textRange': {
                'type': 'ALL'
            },
            'style': {
                'bold': True,
                'fontSize': {
                    'magnitude': 24,  # Adjust the font size as per preference
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

#### creates the 'general_content_slide' #### : 
def create_general_content_slide(service, presentation_id, title_text, content_text, picture_text):
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
    
    image_urls = fetch_image_urls(picture_text)
    if image_urls:
        picture_url = image_urls[0]
        print("The image scrapped IS : " + picture_url)
    else:
        picture_url = "DEFAULT_IMAGE_URL"  # Use a default image URL in case scraping fails
   
    # Modularized calls
    create_text_boxes(service, presentation_id, new_slide_id)
    insert_text_and_image(service, presentation_id, new_slide_id, title_text, content_text, image_urls)
    style_text(service, presentation_id, new_slide_id)



#### Creates the 'TITLE_SLIDE' predefined layout #### : 
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





#### Creates the 'TITLE_AND_BODY' predefined layout #### : 
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




#### Creates the 'SECTION_HEADER' predefined layout #### : 
def create_section_header_slide_layout(service, presentation_id, header_text):
    # Define the request for creating a slide using the 'SECTION_HEADER' predefined layout
    slide_creation_request = {
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'SECTION_HEADER'
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
    
    # Fetch the slide details to extract the object ID of header
    slide_details = service.presentations().pages().get(
        presentationId=presentation_id,
        pageObjectId=new_slide_id
    ).execute()

    # Extract object ID for header
    header_id = slide_details['pageElements'][0]['objectId']

    # Populate the header using 'insertText' request
    insert_header_request = {
        'insertText': {
            'objectId': header_id,
            'text': header_text,
            'insertionIndex': 0
        }
    }

    # Execute the request to insert header text
    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': [insert_header_request]}
    ).execute()

    return {
        'slideId': new_slide_id,
        'headerId': header_id
    }