from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime


client = AsyncIOMotorClient('mongodb://127.0.0.1:27017')

databases = client.scheduler_doctor

collection = databases.agenda

user_id = ''

async def check_date(date, time):
    user = await collection.find_one({'date': date, 'time': time})
    if user:
        return True
    return False

async def check_patient(name):
    user = await collection.find_one({'name': name})
    if user:
        if user.get('date') > str(datetime.now().date()):
            return True
        await collection.delete_one({'_id': user.get('_id')})
        return False
    return False


async def create_patient(user):
    global user_id
    user = await collection.insert_one(user)
    user_created = await collection.find_one({'_id': ObjectId(user.inserted_id)})
    user_id = str(user.inserted_id)
    return user_created, user_id

async def get_patient():
    global user_id
    if user_id:
        user = await collection.find_one({'_id': ObjectId(user_id)})
        return user
    return None

async def update_patient(data):
    global user_id
    if user_id:
        data = dict(data)
        temp = {k:v for k, v in data.items() if v not in ("string", 0)}
        await collection.update_one({'_id': ObjectId(user_id)}, {'$set': temp})
        new_user = await collection.find_one({'_id': ObjectId(user_id)})
        return new_user
    return None

async def delete_patient():
    global user_id
    if user_id:
        await collection.delete_one({'_id': ObjectId(user_id)})
        return True
    return False