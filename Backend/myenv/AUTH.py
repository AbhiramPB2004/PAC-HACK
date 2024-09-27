from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import Request
from fastapi import Response
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi import Response
import jwt
from pymongo import MongoClient 
# from decouple import config
# from dotenv import load_dotenv
import time
import json
from fastapi import Cookie

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)




client = AsyncIOMotorClient("mongodb+srv://aman17272706:lTIDEDz77aGKynCy@credentials.baws4.mongodb.net/?retryWrites=true&w=majority")
db = client.agriculture_db
collection = db.sensor_data


client = MongoClient("mongodb+srv://aman17272706:lTIDEDz77aGKynCy@credentials.baws4.mongodb.net/?retryWrites=true&w=majority") 
db = client["user_database"] 
users_collection = db["users"]

JWT_SECRET="pleab'48dd399f84ca765a0e555b1275ebc69d9f2c95c2bb03d4be'"
JWT_ALGORITHM="HS256"

class Register(BaseModel):
    username: str
    mobile_number: int
    email: str
    password: str   


@app.post("/Register")
async def register_user(user: Register, response: Response):
    user = user.dict()
    print(user)
    # return "helloworld"
    if(users_collection.find_one({"email": user["email"]})):
        return {"error": "User with this email already exists"}
    else:
        users_collection.insert_one({"email": user["email"], "password": user["password"], "username": user["username"], "mobile_number": user["mobile_number"]})
        jwt_token = jwt.encode({"email": user["email"]}, JWT_SECRET, algorithm=JWT_ALGORITHM)
        response.set_cookie(
        key="token",    
        value=jwt_token, 
        httponly=False,   
        )
        return "User registered successfully"

# Endpoint to receive sensor data from ESP32 and store in MongoDB

@app.get("/validateJWT" )
def validate_jwt(response: Response,request: Request, token: str = Cookie(None)):
    headers = request.headers  # Access the headers
    # Print or log the headers
    # print(headers)
    
    try:
        print(token)
        token_res = token.split(":")[1].split("'}")[0].split("'")[1] 
        print(token_res)
        if token != None:    
            payload = jwt.decode(token_res, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            
            return payload
        else:
            return {"error": "Token not found"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except:
        return {"error": "An error occurred"}


@app.get("/")
def read_root():
    return {"message": "FastAPI MongoDB server is running"}
