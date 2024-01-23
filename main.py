from fastapi import FastAPI
import json
from pydantic import BaseModel
from random import randint
from fastapi.encoders import jsonable_encoder

class Person(BaseModel):
    name: str

app = FastAPI()

@app.get("/")
async def hello():
    return {"hello":"world"}

@app.get("/get")
async def get(id: str):
    with open('data.json', 'r') as read_file:
        data = json.load(read_file)
        if id in data and not id == 'max':
            return data[id]
        else:
            return "INVALID ID"


@app.post("/add")
async def add(person: Person):
    with open('data.json', 'r+') as file:
        file_data = json.load(file)
        ind = file_data["max"] + 1
        file_data["max"] = file_data["max"] + 1
        file_data[ind] = jsonable_encoder(person)
        file.seek(0)
        json.dump(file_data, file)
        return person

@app.post("/del")
async def delete(id:str):
    with open('data.json', 'r+') as file:
        file_data = json.load(file)
        deleted = file_data.pop(id)
        file.seek(0)
        json.dump(file_data, file)
        file.truncate()
        return deleted
