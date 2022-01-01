#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, Header

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
def show_person(name: Optional[str] = Query(
                default=None, 
                min_length=1, 
                max_length=50,
                title="person name",
                description= "this is the person name, between 1 and 50 characters",
                ), ##Asi cuando es opcional, y le colocas un valor por defecto
                age: str = Query(
                            ..., 
                            title="Person age",
                            description="this is the person age",
                            )): ##Se coloca asi cuando quieres que sea obligatorio, los tres puntos
    return {name, age}


##NOTA: se va a tomar este path, porque python lee de arriba hacia abajo, por ende se va a quedar con el ultimo path que se haya definido
#validation path parameters
@app.get("/person/detail/{person_id}")
def show_person(person_id: int = Path(
                                    ..., 
                                    gt=0,
                                    title="person id",
                                    description="this is the person id, greater than 0",
                                    )): ##Obligatorio
    return {"person_id": person_id}
