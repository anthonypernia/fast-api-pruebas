#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query

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

#Validation query paramns
@app.get("/person/detail/" )
def show_person(name: Optional[str] = Query(default=None, min_length=1, max_length=50), ##Asi cuando es opcional, y le colocas un valor por defecto
                age: str = Query(...)): ##Se coloca asi cuando quieres que sea obligatorio, los tres puntos
    return {name, age}