from fastapi import FastAPI
import json
from pydantic import BaseModel
from random import randint
from fastapi.encoders import jsonable_encoder
import logging

logging.basicConfig(filename="api.log",
                    format='%(asctime)s %(message)s',
                    filemode='w',
                    level=logging.INFO)
logger = logging.getLogger()

class Person(BaseModel):
    name: str

def isNameInDict(name, dict):
    for val in dict.values():
        if isinstance(val, int):
            continue
        if name in val.values():
            return True
        else:
            continue
    return False

app = FastAPI()

@app.get("/")
async def hello():
    return {"hello":"world"}

@app.get("/get")
async def get(id: str):
    with open('data.json', 'r') as read_file:
        data = json.load(read_file)
        if id in data and not id == 'max':
            logger.info(f'get person id: {id}')
            return data[id]
        else:
            logger.warning(f'attempt to get invalid id: {id}')
            return "INVALID ID"


@app.post("/add")
async def add(person: Person):
    with open('data.json', 'r+') as file:
        file_data = json.load(file)
        print(person.name)
        print(file_data.values())
        if not isNameInDict(person.name, file_data):
            ind = file_data["max"] + 1
            file_data["max"] = file_data["max"] + 1
            file_data[ind] = jsonable_encoder(person)
            file.seek(0)
            json.dump(file_data, file)
            logger.info(f'added new person {ind}: {person.name}')
            return person
        else:
            logger.info(f'tried to add existing person: {person.name}')
            return "person already exist"

@app.post("/del")
async def delete(id:str):
    with open('data.json', 'r+') as file:
        file_data = json.load(file)
        deleted = "NULL"
        if id in file_data:
            deleted = file_data.pop(id)
            logger.info(f"deleted person {id}: {deleted['name']}")
        else:
            logger.warning(f'attempt to delete invalid id: {id}')
        file.seek(0)
        json.dump(file_data, file)
        file.truncate()
        return deleted
