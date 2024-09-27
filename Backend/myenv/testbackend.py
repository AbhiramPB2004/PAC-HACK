import base64
import os
from fastapi import FastAPI, HTTPException,Request
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import pymongo
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
import jwt
from fastapi import Cookie
import uvicorn
from bson import ObjectId

#port 4000
# from decouple import config


JWT_SECRET="pleab'48dd399f84ca765a0e555b1275ebc69d9f2c95c2bb03d4be'"
JWT_ALGORITHM="HS256"

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:5173"
]

client = AsyncIOMotorClient("mongodb+srv://aman17272706:lTIDEDz77aGKynCy@credentials.baws4.mongodb.net/?retryWrites=true&w=majority")
db = client.agriculture_db
collection = db.sensor_data 

MONGO_DETAILS = "mongodb+srv://aman17272706:lTIDEDz77aGKynCy@credentials.baws4.mongodb.net/?retryWrites=true&w=majority" 
client_2 = AsyncIOMotorClient(MONGO_DETAILS)
database = client_2.Product_database # Replace with your database name
collection_2 =  database.product 
 

mongo_uri = "mongodb+srv://aman17272706:lTIDEDz77aGKynCy@credentials.baws4.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongo_uri) 
db = client["Product_database"] 
product_collection = db["product"] 
cart_collection = db["cart"]
users_collection = db["users"]


class User(BaseModel):
    username: str
    mobile_number: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str


class Catalogue(BaseModel):
    _id: str
    Image_Url: str
    name: str
    Offer: str
    price: int
    uniqueID: str
        

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


IMAGE_DIR = "images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)


class Product(BaseModel):
    productName: str
    productDescription: str
    productPrice: float
    stockQuantity: int
    offer: int
    category: str
    productImage: Optional[str] = None  

def object_id_to_str(item):
    item["_id"] = str(item["_id"])
    return item

def save_base64_image(base64_str, filename):
    try:
        
        image_data = base64.b64decode(base64_str.split(",")[1])
        
        with open(os.path.join(IMAGE_DIR, filename), "wb") as file:
            file.write(image_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")


@app.post("/api/products")
async def create_product(product: Product):
    
    print("Received product data:", product.dict())
    product_name = product.productName
    product_description = product.productDescription
    product_price = product.productPrice
    stock_quantity = product.stockQuantity
    product_image = product.productImage
    catefory = product.category
    offer = product.offer
    
    print(product_name)
    print(product_description)
    print(product_price)
    print(stock_quantity)
    
    product_collection.insert_one({
        "name": product_name,
        "description": product_description,
        "price": product_price,
        "quantity": stock_quantity,
        "image": product_image,
        "category": catefory,
        "offer": offer
          
    })
    
    if product.productImage:
        image_filename = f"{product.productName.replace(' ', '_').lower()}.png"
        try:
            save_base64_image(product.productImage, image_filename)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    
    return {"message": "Product created successfully", "product": product.dict()}

@app.get("/products_find/{id}")
async def get_product(id: str):
    try:
        # Convert the string item_id to ObjectId
        obj_id = ObjectId(id)
    except Exception:
        # If item_id is not a valid ObjectId
        raise HTTPException(status_code=400, detail="Invalid item ID format")
    
    # Query MongoDB for the item
    item =  product_collection.find_one({"_id": obj_id})
    
    if item:
        # Convert the ObjectId to string before returning the response
        return object_id_to_str(item)
    else:
        # Return 404 if the item is not found
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/items")
async def get_all_items():
    items = []
    data  = await collection_2.find().to_list(length=40)
    for item in data:
        items.append(object_id_to_str(item))
    return items


@app.get("/api/sensor-data")
async def get_sensor_data():
    try:
        # Retrieve the latest data from MongoDB
        cursor = collection.find().sort("timestamp", -1).limit(100)  # Limit to the latest 100 records
        data = await cursor.to_list(length=100)

        # Convert MongoDB documents to a list of dictionaries
        result = [
            {
                "date": d["timestamp"].strftime("%Y/%m/%d"),
                "time": d["timestamp"].strftime("%H:%M:%S"),
                "temperature": d["temperature"],
                "humidity": d["humidity"],
                "ldr": d["ldr"],
                "soilMoisture": d["soil_moisture"]
            }
            for d in data
        ]
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving data")
    

@app.get('/catalogue')
async def get_catalogue():
    try:
        # Fetch all products from the MongoDB collection
        items = product_collection.find().limit(4)
        product_list  = []
        
    

        # Iterate through the MongoDB documents and format them
        for item in items:
            # print(item.get("_id", ""))
            product_obj_id = ObjectId(item.get("_id"))
            
            product = Catalogue(   
            uniqueID=item.get("UniqueID", ""),
            Image_Url=item.get("Image_Url", ""),
            name=item.get("name", ""),
            Offer=item.get("Offers", ""),  # Fixed from "Offers" to "Offer" if that was a typo
            price=item.get("price", 0)
            )
            
            product_list.append(product)
        
        # print(product_list)
        return product_list

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch products from the database.")
    

@app.get('/cart')
async def get_cart():
    try:
        # Fetch all products from the MongoDB collection
        items = product_collection.find().limit(4)
        product_list = []

        for item in items:
            product_obj_id = str(item.get("_id"))
            product = Catalogue(
            _id=product_obj_id,
            Image_Url=item.get("Image_Url", ""),
            name=item.get("name", ""),
            Offer=item.get("Offer", ""),
            price=item.get("price", 0),
            uniqueID=item.get("UniqueID", "")
            )
            product_list.append(product)

        return product_list
        
        
        
        
    
        
        # print(product_list)
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch products from the database.")

@app.post("/register")
async def register(user: User):
    
    
    
    user_data = {
        "username": user.username,
        "mobile_number": user.mobile_number,
        "email": user.email,
        "password": user.password
    }
    
    payload = {
        "user_id": user_data["email"],
        "mobile_number": user_data["mobile_number"],
    }
    # token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    # response.set_cookie(
    #     key="token",    
    #     value=token_response(token), 
    #     httponly=False,   
    #     )

    # Check if user already exists
    existing_user = users_collection.find_one({"email": user_data["email"]})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    # Hash password
    # hashed_password = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt())

    # Insert new user
    users_collection.insert_one({
        "username": user_data["username"],
        "mobile_number": user_data["mobile_number"],
        "email": user_data["email"],
        "password": user_data["password"]
    })
    return {"response": "User registered successfully"}



