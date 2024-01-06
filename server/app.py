from fastapi import FastAPI, HTTPException, Header, Request, UploadFile, File
import asyncio
import tempfile
from pydantic import BaseModel
import requests
import firebase_admin
import stripe
from mcq_creator_v1 import mcq_creator_v1
from flashcard_model_v2 import FlashcardModelV2
from text_processing_v1 import text_fact_transformer_V1
from info_extractor_v5 import InfoExtractorV5
from flask_cors import CORS
import file_process_methods as file_processor
from uvicorn.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials
from firebase_admin import auth
import redis
from upstash_redis import Redis
import os


stripe.api_key = os.getenv("STRIPE_API_KEY")
class RegisterRequest(BaseModel):
    email: str
    password: str



r = redis.Redis(
  host='eu1-moral-jaybird-38118.upstash.io',
  port=38118,
  password='f0dc8b78859b4be9acc4d80710b6f83f'
)


cred = credentials.Certificate("./firebase_admin_auth.json")
firebase_admin.initialize_app(cred)

app = FastAPI()


def checkRedis(user_id):
    user_key = f"user:{user_id}"
    if r.exists(user_key):
        redis_cache = r.hgetall(user_key)
        max_requests = int(redis_cache[b'max_requests'])
        current_requests = int(redis_cache[b'current_requests'])
        if max_requests <= current_requests:
            return False
        else:
            return True
    else:
        # Note: Consider using 'hset' for newer Redis versions
        r.hmset(user_key, {'max_requests': 2, 'current_requests': 0})
        return True

#Need to add in the serverless redis setup so that it can actuaoly chcekc the caching properly : 
def checkUserPerms(user_id) :
    checkedRedis = checkRedis(user_id)
    if checkedRedis == True :
        return True
    else :
        return False
    
def incrementRedisRequestCount(user_id) : 
    userid = f"user:{user_id}"
    r.hincrby(userid, 'current_requests', 1)

app.add_middleware(
  CORSMiddleware,
    allow_origins=["*"],  # Specify the allowed origin
    allow_credentials=True,
    allow_methods=["POST", "GET"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/register") 
async def register_user(request: RegisterRequest):
    try:
        # Create user with Firebase
        firebase_user = auth.create_user(email=request.email, password=request.password)

        # Create Stripe customer
        stripe_customer = stripe.Customer.create(email=request.email)

        # Optional: Save the Stripe customer ID in your database

        # Return the user ID and Stripe customer ID
        return {"user_id": firebase_user.uid, "stripe_customer_id": stripe_customer.id}     
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/async_text_fact_breakdown/") 
async def async_text_fact_breakdown(request : Request, user_id : str = Header(None, alias="User-ID")) : 

    userPerms = checkUserPerms(user_id)
    print(userPerms)
    if userPerms == False : 
        return "Nothing"
    incrementRedisRequestCount(user_id)
    
    text = await request.body()
    text = text.decode("utf-8")
    

    if len(text) > 1000000000 : 
        return "too long"
    else : 
        text_facts = await text_fact_transformer_V1(text) # NEED TO FIX THIS
        return (text_facts)

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


@app.post('/file_input') 
async def handleFileInput(file : UploadFile = File(...)) : 
    if file :
        path = file_processor.process_file(file)
        print("this is the file name : ", file.filename)
        fileType = file.filename.split('.')[-1] 
        print("this is the file type :  ", fileType)
        process_method = file_processor.choose_file_process_type(fileType)
        data = process_method(path)

        data_processed = await text_fact_transformer_V1(data)
        print(data_processed)
        return (data_processed)
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
    return num
