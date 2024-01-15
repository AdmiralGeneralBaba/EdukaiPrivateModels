from fastapi import FastAPI, HTTPException, Header, Request, UploadFile, File
import asyncio
import tempfile
from fastapi.responses import RedirectResponse
from flask import redirect
from pydantic import BaseModel
import requests
import firebase_admin
import stripe
from mcq_creator_v1 import mcq_creator_v1
from flashcard_model_v2 import FlashcardModelV2
from text_processing_v1 import text_fact_transformer_V1
from text_processing_v1 import count_facts
from info_extractor_v5 import InfoExtractorV5
from flask_cors import CORS
import file_process_methods as file_processor
from uvicorn.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials
from firebase_admin import auth, firestore
import redis
from upstash_redis import Redis
import os
from openai_calls import OpenAI
import openai
from os import environ as env

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
    allow_origins=["*"],  # Specify the allowed origin
    allow_credentials=True,
    allow_methods=["POST", "GET"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

for key, value in os.environ.items():
    print(f"{key}: {value}")

# Stripe API key : 
print(env['MY_VARIABLE'])
#API key setup
stripe.api_key = os.getenv("STRIPE_API")
openai.api_key = os.getenv('OPENAI_API_KEY')


print(os.getenv("STRIPE_API"))
print("This is the redis password : ", )

r = redis.Redis(
  host='eu1-moral-jaybird-38118.upstash.io',
  port=38118,
  password= "f0dc8b78859b4be9acc4d80710b6f83f"
)

cred = credentials.Certificate("./firebase_admin_auth.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#Functions for checking Redis and the user perms : 
def checkRedis(user_id):
    user_key = f"user:{user_id}"
    if r.exists(user_key):
        redis_cache = r.hgetall(user_key)
        max_requests = int(redis_cache[b'max_questions'])
        current_requests = int(redis_cache[b'current_questions'])
        if max_requests <= current_requests:
            return False
        else:
            return True
    else:
        # Note: Consider using 'hset' for newer Redis versions
        r.hmset(user_key, {'max_questions': 2000, 'current_questions': 0})
        return True
def setupRedis(user_id) : 
    user_key = f"user{user_id}"
    r.hmset(user_key, {'max_questions' : 100, 'current_questions' : 0})
#Need to add in the serverless redis setup so that it can actuaoly chcekc the caching properly : 
def checkUserPerms(user_id) :
    checkedRedis = checkRedis(user_id)
    if checkedRedis == True :
        return True
    else :
        return False
    
def incrementRedisRequestCount(user_id, question_count) : 
    userid = f"user:{user_id}"
    r.hincrby(userid, 'current_questions', question_count)

class RegisterRequest(BaseModel):
    email: str
    user_id : str

class CheckoutModel(BaseModel) : 
    tier : int
    customer_id : str
    user_id : str

class BillingModel(BaseModel) : 
    customer_id : str

@app.post("/register") 
async def register_user(request: RegisterRequest):
    try:
        # Create Stripe customer
        stripe_customer = stripe.Customer.create(email=request.email)
        print("this is the stripe customer object", stripe_customer)
        # Save the Stripe customer ID in Firestore
        db = firestore.client()
        print("this is the DB", db)
        print(request.user_id)
        user_ref = db.collection('users').document(request.user_id)
        user_ref.set({
            'stripe_customer_id': stripe_customer.id,
            'tier' : 0
            # You can add more user-related information here if needed
        })
        setupRedis(user_ref.id)
        # Return the user ID and Stripe customer ID
        return {"user_id": request.user_id, "stripe_customer_id": stripe_customer.id}     
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/current_usage_data/{user_id}') 
async def current_usage(user_id: str):
    search_query = f"user:{user_id}"
    redis_cache = r.hgetall(search_query)
    
    # Ensure that the keys exist in Redis cache
    if b'max_questions' in redis_cache and b'current_questions' in redis_cache:
        max_questions = int(redis_cache[b'max_questions'])
        current_questions = int(redis_cache[b'current_questions'])
        request_object = { 
            "max_questions": max_questions,
            "current_questions": current_questions
        }
    else:
        # Handle the case where the keys don't exist
        request_object = {
            "error": "Data not found for the specified user."
        }

    return request_object

@app.post('/create-checkout-session')
async def create_checkout_session(CheckoutModel : CheckoutModel):
    tier = CheckoutModel.tier
    customer_id = CheckoutModel.customer_id
    user_id = CheckoutModel.user_id
    print(tier, customer_id, user_id)
    
    def choosePrice(tier) : 
        if(tier == 1): 
            price = "price_1OXqCOJeWZ1WiRc9mVmS3zZh"
        elif(tier == 2) : 
            price = "price_1OXqCiJeWZ1WiRc9SOKt90Cy"
        return price
    try:
        price = choosePrice(tier)
        checkout_session = stripe.checkout.Session.create(
            customer=customer_id,
            line_items=[    
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': price,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url='http://localhost:3000/' + 'input',
            cancel_url='http://localhost:3000/' + 'subscriptions',
        )
    except Exception as e:
        return str(e)

    return checkout_session.url

@app.post("/manage-billing-section")
async def manage_billing(billing_model: BillingModel):
    customer_id = billing_model.customer_id
    # You might want to handle exceptions here for production code
    try:
        # Create a billing portal session
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url="http://localhost:3000/input"
        )

        # Return the URL to the user
        return {"url": session.url}

    except stripe.error.StripeError as e:
        # Handle Stripe errors (e.g., invalid customer ID)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/webhook")
async def webhook(request: Request):  
    print("CAME THROUGH")
    data = await request.json()  # Adjusted to get JSON data from the request
    customer_id = data['data']['object']['customer']
    line_item = data['data']['object']['lines']['data'][0]['price']['id']
    usersRef = db.collection("users")
    users = usersRef.where("stripe_customer_id", "==", customer_id)
    userDocs = users.get()
    userDoc = userDocs[0]
    user_id = userDoc.id
    print(user_id)
    def calculateTier(line_item) : 
        tier = 0
        if(line_item == "price_1OVh5aJeWZ1WiRc9hIBWJOoi") : 
            tier = 1
        elif(line_item == "price_1OVh6NJeWZ1WiRc9eO0RQMq5") :
            tier = 2
        elif(line_item == "price_1OVh6iJeWZ1WiRc9FzkfrGqW") : 
            tier = 3 
        return tier
    
    userDocRef = usersRef.document(user_id)
    tier = calculateTier(line_item)
    userDocRef.update({"tier" : tier})
    
    checkUserPerms(user_id)
    def chooseRateChange(line_item) : 
        max_requests = 0
        if(line_item == "price_1OVh5aJeWZ1WiRc9hIBWJOoi") : 
            max_requests = 5
        elif(line_item == "price_1OVh6NJeWZ1WiRc9eO0RQMq5") :
            max_requests = 8000
        elif(line_item == "price_1OVh6iJeWZ1WiRc9FzkfrGqW") : 
            max_requests = 500000  
        return max_requests
    
    new_max_requests = chooseRateChange(line_item)
    redis_search = f"user:{user_id}"
    r.hset(redis_search, "max_questions", new_max_requests)

  

#########################################################################################################################################################################
#########################################################################################################################################################################
################################################      THE ROUTES BELOW ARE THE AI ROUTES :     ##########################################################################
#########################################################################################################################################################################
#########################################################################################################################################################################
    

@app.post("/async_text_fact_breakdown/") 
async def async_text_fact_breakdown(request : Request, user_id : str = Header(None, alias="User-ID")) : 

    userPerms = checkUserPerms(user_id)
    if userPerms == False : 
        return { "error" : "tier_too_low"}
    
    text = await request.body()
    text = text.decode("utf-8")
    

    if len(text) > 1000000000 : 
        return "too long"
    else : 
        text_facts = await text_fact_transformer_V1(text) # NEED TO FIX THIS
        question_count = count_facts(text_facts['lesson_facts'])
        incrementRedisRequestCount(user_id, question_count)
        return text_facts


@app.post('/file_input') 
async def handleFileInput(file : UploadFile = File(...), user_id : str = Header(None, alias="User-ID")) : 

    print("THIS IS THE USER ID TAKEN FROM AS A HEADER IN THE FILE INPUT : ", user_id)
    userPerms = checkUserPerms(user_id)
    if userPerms == False : 
        return { "error" : "tier_too_low"}
    
    if file :
        path = file_processor.process_file(file)
        print("this is the file name : ", file.filename)
        fileType = file.filename.split('.')[-1] 
        print("this is the file type :  ", fileType)
        process_method = file_processor.choose_file_process_type(fileType)
        data = process_method(path)

        file_facts = await text_fact_transformer_V1(data)
        # calculates the question coiunt and increments the redis middleware
        question_count = count_facts(file_facts['lesson_facts'])
        incrementRedisRequestCount(user_id, question_count)
        return (file_facts)
    else : 
        return { 'error ' : 'no file found'}

@app.post('/mcq_creator/') 
async def mcq_creator(request : Request) :
    set = await request.body() 
    set = set.decode("utf-8")


    mcq = await mcq_creator_v1(set, 1)
    return (mcq)

@app.post('/flashcards/')
async def flashcard_creator(request : Request): 
    set = await request.body()
    set = set.decode("utf-8")
    # Decoding the URL encoded lesson value
    flashcard_creator = FlashcardModelV2()
    # gpt_type is hard-coded to '1'
    flashcards = flashcard_creator.flashcard_creator_from_raw_facts(set, '0')
    return (flashcards)

@app.get('/test/{num}')
def number_printer(num) :
    test = "test"
    return test

@app.get('/youtube_to_text/') 
async def async_text_fact_breakdown_youtube_url(youtube_url : str) : 
    # directory = request.args.get('directory')
    directory = r"C:\Users\david\Downloads\Youtube"
    info_extractor = InfoExtractorV5()
    text = info_extractor.transcribe_youtube_url(youtube_url, directory)
                   
    if len(text) > 100000 : 
        return "too long"
    else : 
        text_facts = await text_fact_transformer_V1(text) # NEED TO FIX THIS
        return (text_facts)

@app.get('/openai-test/{text}')
async def test(text : str) : 
   text_facts =  await text_fact_transformer_V1(text)
   return (text_facts)