#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

#Models
class Person(BaseModel):
    firts_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None
    


@app.get("/")
def home():
    return {"message": "Hello World"}

##rquest and response body

@app.post('/person/new')
def create_person(person: Person = Body(...)): #El triple punto indica que es oblicatorio el body
    return person