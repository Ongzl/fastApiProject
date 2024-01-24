from fastapi import FastAPI
import json
from pydantic import BaseModel
from random import randint
from fastapi.encoders import jsonable_encoder
import logging
from typing import Union

logging.basicConfig(filename="api.log",
                    format='%(asctime)s %(message)s',
                    filemode='a',
                    level=logging.INFO)
logger = logging.getLogger()

class Person(BaseModel):
    id: Union[str,None] = None
    name: str
    number: str

def isValueInDict(value, dict):
    for val in dict.values():
        if isinstance(val, int):
            continue
        if value in val.values():
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
        #check that user not trying to get extra info(number of person in db), and that id exists
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
        #name and number validation
        if not (all(name.isalpha() or name.isspace() for name in person.name) and person.number.isnumeric()):
            logger.warning(f'failed name/number regex, attempted to add existing person: {person.name}, {person.number}')
            return "invalid name or phone number. only alphabets in name and numbers in number"
        #check for repeated name
        if not isValueInDict(person.name, file_data) and not isValueInDict(person.number, file_data):
            ind = file_data["max"] + 1
            file_data["max"] = file_data["max"] + 1
            #set optional id of person to be same as dict index
            person.id = ind
            file_data[ind] = jsonable_encoder(person)
            file.seek(0)
            json.dump(file_data, file)
            logger.info(f'added new person {ind}: {person.name}, {person.number}')
            return person
        else:
            logger.warning(f'attempted to add existing person: {person.name}, {person.number}')
            return "person already exist"

@app.post("/del")
async def delete(id:str, name:str):
    with open('data.json', 'r+') as file:
        file_data = json.load(file)
        deleted = "NULL"
        if id in file_data:
            #check that name supplied is same as name in db
            if isValueInDict(name, file_data):
                deleted = file_data.pop(id)
                logger.info(f"deleted person {id}: {deleted['name']}")
            else:
                logger.warning(f'attempted to delete id: {id}, but name mismatch')
                return "name and id mismatch"
        else:
            logger.warning(f'attempted to delete invalid id: {id}')
        file.seek(0)
        json.dump(file_data, file)
        file.truncate()
        return deleted
